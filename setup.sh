#!/usr/bin/env bash

PROG="credential"


if [ -d "/opt/${PROG}" ]
then
    echo "Directory /opt/${PROG} already exist, aborting..."
    exit 1
fi

if [ -d "/etc/${PROG}" ]
then
    echo "Directory /etc/${PROG} already exist, aborting..."
    exit 1
fi


sudo mkdir /opt/${PROG}
sudo mkdir /etc/${PROG}

sudo cp ./src/account.py ./src/credential.py /opt/${PROG}
sudo cp ./src/config.yml /etc/${PROG}

sudo chmod +x /opt/${PROG}/credential.py
sudo chmod 600 /etc/${PROG}/config.yml

sudo ln -s /opt/${PROG}/credential.py /usr/local/sbin/credential

sudo apt-get install sqlcipher \
                     xclip

sudo pip install -r ./src/requirements/pip_requirements