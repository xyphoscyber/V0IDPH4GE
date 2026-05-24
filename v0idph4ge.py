#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : v0idph4ge_osgint.py
# Author             : xyphoscyber 
# Date created       : 24 May 2026
# Rebranded by       : V0IDPH4GE
# Description        : Digital OSINT Framework - GitHub Intelligence Gatherer

import json
import requests
import binascii
import re
from requests.auth import HTTPBasicAuth
import sys
import base64
import argparse

version_number = '1.0.3'

banner = """[0;35m
██╗   ██╗   ██████╗   ██╗  ██████╗   ██████╗   ██╗  ██╗  ██╗  ██╗   ██████╗   ███████╗
██║   ██║  ██╔═╗██║  ██║  ██╔══██╗  ██╔══██╗  ██║  ██║  ██║  ██║  ██╔════╝   ██╔════╝
╚██╗ ██╔╝  ██║║║██║  ██║  ██║  ██║  ██████╔╝  ███████║  ███████║  ██║  ███╗  █████╗
 ╚████╔╝   ██║║║██║  ██║  ██║  ██║  ██╔═══╝   ██╔══██║  ╚════██║  ██║   ██║  ██╔══╝
  ╚██╔╝    ╚█████╔╝  ██║  ██████╔╝  ██║       ██║  ██║       ██║  ╚██████╔╝  ███████╗
   ╚═╝      ╚════╝   ╚═╝  ╚═════╝   ╚═╝       ╚═╝  ╚═╝       ╚═╝   ╚═════╝   ╚══════╝
[1;35m        D I G I T A L   O S I N T   F R A M E W O R K[0m
[0;1;3mBy Xeo Xyphos[0;35m | [0;1mhttps://github.com/xyphoscyber [0m
"""

jsonOutput = {}
output = []
email_out = []

def findReposFromUsername(username):
    response = requests.get('https://api.github.com/users/%s/repos?per_page=100&sort=pushed' % username).text
    repos = re.findall(r'"full_name":"%s/(.*?)",.*?"fork":(.*?),' % username, response)
    nonForkedRepos = []
    for repo in repos:
        if repo[1] == 'false':
            nonForkedRepos.append(repo[0])
    return nonForkedRepos


def findEmailFromContributor(username, repo, contributor):
    response = requests.get('https://github.com/%s/%s/commits?author=%s' % (username, repo, contributor), auth=HTTPBasicAuth(username, '')).text
    latestCommit = re.search(r'href="/%s/%s/commit/(.*?)"' % (username, repo), response)
    if latestCommit:
        latestCommit = latestCommit.group(1)
    else:
        latestCommit = 'dummy'
    commitDetails = requests.get('https://github.com/%s/%s/commit/%s.patch' % (username, repo, latestCommit), auth=HTTPBasicAuth(username, '')).text
    email = re.search(r'<(.*)>', commitDetails)
    if email:
        email = email.group(1)
        email_out.append(email)
    return

def findEmailFromUsername(username):
    repos = findReposFromUsername(username)
    for repo in repos:
        findEmailFromContributor(username, repo, username)

def findPublicKeysFromUsername(username):
    gpg_response = requests.get(f'https://github.com/{username}.gpg').text
    ssh_response = requests.get(f'https://github.com/{username}.keys').text
    if not "hasn't uploaded any GPG keys" in gpg_response:
        output.append(f'[+] GPG_keys : https://github.com/{username}.gpg')
        jsonOutput['GPG_keys'] = f'https://github.com/{username}.gpg'
        # extract email from gpg key
        regex_pgp = re.compile(r"-----BEGIN [^-]+-----([A-Za-z0-9+\/=\s]+)-----END [^-]+-----", re.MULTILINE)
        matches = regex_pgp.findall(gpg_response)
        if matches:
            try:
                # Clean base64 string: remove whitespace and fix padding
                b64_str = re.sub(r'\s+', '', matches[0])
                padding_needed = 4 - len(b64_str) % 4
                if padding_needed != 4:
                    b64_str += '=' * padding_needed
                # Base64 decode the signature block
                b64 = base64.b64decode(b64_str)
                # Convert the base64 to hex
                hx = binascii.hexlify(b64)
                # Get the offsets for the Key ID
                keyid = hx.decode()[48:64]
                output.append(f'[+] GPG_key_id : {keyid}')
                jsonOutput['GPG_key_id'] = keyid
                # find email adress
                emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", b64.decode('Latin-1'))
                if emails:
                    for email in emails:
                        email_out.append(email)
            except Exception as e:
                output.append(f'[-] GPG_key parsing error : {str(e)}')
    if ssh_response:
        output.append(f'[+] SSH_keys : https://github.com/{username}.keys')
        jsonOutput['SSH_keys'] = f'https://github.com/{username}.keys'

def findInfoFromUsername(username):
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url)
    if response.status_code == 200 and requests.codes.ok:
        data = response.json()
        for i in data:
            if i in ['login','id','avatar_url','name','blog','location','twitter_username','email','company','bio','public_gists','public_repos','followers','following','created_at','updated_at']:
                if data[i] != None and data[i] != '':
                    if i == 'email':
                        email_out.append(data[i])
                    jsonOutput[i] = data[i]
                    output.append(f'[+] {i} : {data[i]}')
        jsonOutput['public_gists'] = f'https://gist.github.com/{username}'
        output.append(f'[+] public_gists : https://gist.github.com/{username}')
        return True
    elif response.status_code == 404:
        jsonOutput['error'] = 'username does not exist'
        return False

def findUsernameFromEmail(email):
    response = requests.get('https://api.github.com/search/users?q=%s' % email).text
    username = re.findall(r'"login":"(.*?)"', response)
    if username:
        output.append(f'[+] username : {username[0]}')
        jsonOutput['username'] = username[0]
    else:
        output.append(f'[-] username : Not found')
        jsonOutput['username'] = 'Not found'

class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('Error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def parse_args():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-u", "--username", default=None, help="Github username of the account to search for")
    parser.add_argument("-e", "--email", default=None, help="Email of the account to search for github username")
    parser.add_argument("--json", default=False, action="store_true", help="Return a json output")
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    print(banner)
    args = parse_args()
    if(args.username):
        username_exists = findInfoFromUsername(args.username)
        if username_exists:
            findEmailFromUsername(args.username)
            findPublicKeysFromUsername(args.username)
            if(args.json):
                jsonOutput['email'] = list(set(email_out))
                print(json.dumps(jsonOutput, sort_keys=True, indent=4))
            else:
                for data in output:
                    print(data)
                if email_out != []:
                    print('[+] email :', end='')
                    for email in list(set(email_out)):
                        print(f' {email}', end='')
        else:
            if(args.json):
                print(json.dumps(jsonOutput, sort_keys=True, indent=4))
            else:
                print(f'Username does not exist')
    elif(args.email):
        findUsernameFromEmail(args.email)
        if(args.json):
            print(json.dumps(jsonOutput, sort_keys=True, indent=4))
        else:
            for data in output:
                print(data)
    else:
        print('Help: ./v0idph4ge_osgint.py -h')
        sys.exit(1)
