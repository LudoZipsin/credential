# CREDENTIAL

## Purpose

There are two purpose for this tool:

* avoid putting credential in clear inside script (pretty useful for security reason and to avoid mistake
  such as putting credential in services like GitHub or other remote git)
* avoid the pain to manage to much script with credential in each. If you change the password for one
  service, you have to edit each individual script

Those are two issues that really bother me. Hence, I wrote **credential**

Credential is written in 300 lines of python 2 (with help of some module)


## Features

A credential is composed of a unique alias (see it as a primary key), a service (like google, yahoo or other
web site), an account (typically your mail address but can be whatever you want) and finally a passphrase.

### Add

basic:
```
credential add
```
it will ask you for the alias, the service, the account and the passphrase.

no-format:
```
credential add -n
credential add --noformat
```
by default, credential will store service in lower case string and will trim away the unnecessary part
 of an url. I you don't want this behaviour, use `-n` or `--noformat`

other arguments:
* `-a, --acount`: give the account name. It will not ask you to ad it since you gave it in arguments
* `-s, --service`: same as previous but for service
* `-A, --alias`: same as previous but for alias
* there is no way to directly add the passphrase. Credential will ask you for it and you'll have to type
it


### List

There is two way to use it. Or with nothing, or with the service name.

Nothing:
```
credential list
```
will list the service and the number of account associated

With service:
```
credential list -s <my service>
```
will list the account and alias of the service `<my service>`

### Get

get need at least one argument : the alias of the account you want to get credential.
```
credential get <alias>
```
will get the service (default) associated with `<alias>`. For security reason, it is the default behaviour

If you want other field:
* `credential get -s account <alias>`: will get you the account for the alias `<alias>`
* `credential get -s passphrase <alias>`: will get you the passphrase for the alias `<alias>`

By default, nothing will be prompt in your terminal. The result will be store inside you clipboard
(press Ctrl+V to print it). If you want to prompt it directly, will have to ask it to prompt with `-p` or
`--prompt`:

```
credential get -p <alias>
credential get --prompt <alias>
```

### Edit

to edit an existing credential.

Basic:
```
credential edit <alias>
```
will ask you if you want to change the account then will ask you if you want to change the passphrase.

specify:
```
credential edit -a <alias>
```
will ask you the new name for the account. Will not ask anything for the passphrase

```
credential edit -p <alias>
```
will ask you the new passphrase for the account. Will not ask anything for the account

```
credential edit -p -a <alias>
```
will ask you the new passphrase and the name for the account. Same as `credential edit <alias>`

### Remove

```
credential remove <alias>
```
will ask you if you want to delete the credential with alias `<alias>`.

```
credential remove -f <alias>
```
will delete the credential with alias `<alias>` without asking for it.

## Install

Just run:

```bash
git clone https://github.com/LudoZipsin/credential.git
cd credential
sudo ./setup.sh
```

Next you'll have to edit the passphrase to encrypt the database used to store the credential.

```bash
sudo vim /etc/credential/config.yml
```

and replace the `passphrase` in field `db_passphrase:` into whatever you want.

That's it, credential is installed in your system. You can remove the cloned repo if you want

## How to

Assume you want to write a bash script `my_script.sh` that will use the credential tool to get the passphrase associated
with the alias `test`:

```bash
#! /usr/bin/env bash
echo "my pass : $(credential get -p -s passphrase test)"
```

```
chmod +x my_script.sh
```

Technically, credential won't run without root privilege. So you have to launch `my_script.sh` with `sudo`.
So:

```bash
chmod +x my_script.sh
sudo my_script.sh
```

If you don't want to put your password, you'll have to give `my_script.sh` the right to be launched with
sudo without password. To do so, you'll use `sudo visudo`.

Assuming you username is `user`, your hostname is `host` and the script is located in
`/home/user/my_script.sh`, add the line:

```
user host = (root) NOPASSWD: /home/usr/my_script.sh
```

Save and close. Now you can use `sudo ./my_script.sh` without password needed.

However, since everybody can access the script and modify it without root access, they can edit it to prompt
the credential they want. To avoid it, I  highly recommend to put those script in a root folder and use:

```
sudo chmod 600 <your_script_in_root_folder>
```


## Possible issues

Since **credential** is written in python 2, there may be issue if using unicode character (for username,
alias, service and passphrase)

## Improvement for the future

### Make it a package

For this moment, the only option to use this tool inside another python script is with `subprocess`

```python
#! /usr/bin/env python
from subprocess import check_output

p = check_output("credential get -p -s passphrase test")
print "my pass : ", p
```
which is not convenient for a tool written in python. (unless using it for python3 application since
current dependencies force the use of python 2).

In the future, I'll may modify it to be used as a package

### Select the database

Adding functionality to select the database to use. May be useful for team remotely working on the same
project.

### Moving it python 3

I rather like to use python 3 than python 2. However, limitation in psqcipher binding forced the use of
python 2. Since there is work in progress to port this binding to python 3, once it's done, I'll move it
to python 3 too.
