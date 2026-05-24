# V0IDPH4GE
Retrieve informations about a github username/email

<img src="https://img.shields.io/github/v/release/xyphoscyber/v0idph4ge_osgint?style=flat-square">

## Features
- Find github username from an email
- Find email from github username (not working all the time)
- Find informations about a profile (account creation date, public gists, id, public pgp, public ssh ...)

## Requirements
```bash
pip3 install -r requirements.txt
```

## Usage
```bash
$ python3 v0idph4ge_osgint.py -h

██╗   ██╗   ██████╗   ██╗  ██████╗   ██████╗   ██╗  ██╗  ██╗  ██╗   ██████╗   ███████╗
██║   ██║  ██╔═╗██║  ██║  ██╔══██╗  ██╔══██╗  ██║  ██║  ██║  ██║  ██╔════╝   ██╔════╝
╚██╗ ██╔╝  ██║║║██║  ██║  ██║  ██║  ██████╔╝  ███████║  ███████║  ██║  ███╗  █████╗
 ╚████╔╝   ██║║║██║  ██║  ██║  ██║  ██╔═══╝   ██╔══██║  ╚════██║  ██║   ██║  ██╔══╝
  ╚██╔╝    ╚█████╔╝  ██║  ██████╔╝  ██║       ██║  ██║       ██║  ╚██████╔╝  ███████╗
   ╚═╝      ╚════╝   ╚═╝  ╚═════╝   ╚═╝       ╚═╝  ╚═╝       ╚═╝   ╚═════╝   ╚══════╝
        D I G I T A L   O S I N T   F R A M E W O R K
By xyphoscyber | https://github.com/xyphoscyber

usage: v0idph4ge_osgint.py [-h] [-u USERNAME] [-e EMAIL] [--json]

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Github username of the account to search for (default: None)
  -e EMAIL, --email EMAIL
                        Email of the account to search for github username (default: None)
  --json                Return a json output (default: False)
```

## Example output

### username
```bash
$ ./v0idph4ge_osgint.py -u hippiiee
[+] login : hippiiee
[+] id : 41185722
[+] avatar_url : https://avatars.githubusercontent.com/u/41185722?v=4
[+] name : Hippie
[+] blog : https://hippie.cat
[+] bio : Hi !
[+] public_repos : 10
[+] public_gists : 0
[+] followers : 8
[+] following : 9
[+] created_at : 2018-07-13T08:28:00Z
[+] updated_at : 2022-08-21T13:11:36Z
[+] public_gists : https://gist.github.com/hippiiee
[+] GPG_keys : https://github.com/hippiiee.gpg
[+] GPG_key_id : 27cbb171ff857c58
[+] email : hquere@e3r4p3.42.fr hippolyte.q@gmail.com
```

```bash
$ ./v0idph4ge_osgint.py -u hippiiee --json
{
    "GPG_key_id": "27cbb171ff857c58",
    "GPG_keys": "https://github.com/hippiiee.gpg",
    "avatar_url": "https://avatars.githubusercontent.com/u/41185722?v=4",
    "bio": "Hi !",
    "blog": "https://hippie.cat",
    "created_at": "2018-07-13T08:28:00Z",
    "email": [
        "hquere@e3r4p3.42.fr",
        "hippolyte.q@gmail.com"
    ],
    "followers": 8,
    "following": 9,
    "id": 41185722,
    "login": "hippiiee",
    "name": "Hippie",
    "public_gists": "https://gist.github.com/hippiiee",
    "public_repos": 10,
    "updated_at": "2022-08-21T13:11:36Z"
}
```

### Email
```bash
$ ./v0idph4ge_osgint.py -e chrisadr@gentoo.org
[+] username : ChrisADR
```

```bash
$ ./v0idph4ge_osgint.py -e chrisadr@gentoo.org --json
{
    "username": "ChrisADR"
}
```

## How does it works ?

To get a user email, v0idph4ge is checking :

- all the public commits of the user, if the email is not hidden in one of the commit it will be added to the list
- if the user have a GPG key, if he has one, it's getting the email from the content of the GPG after a base64 decode
- github user API

To get a user email, v0idph4ge is checking :

- github user API
- 🚧 spoofing a commit with the email, then checking the name in the commit history (working every time) 🚧 (Work In Progress)
