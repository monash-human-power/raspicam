#!/bin/sh

printf "\nGenerating ssh-keys....\n\n"
cat ~/.ssh/id_rsa.pub | ssh pi@PatPi.local "cat >> ~/.ssh/authorized_keys"
printf "\nSuccessfully generated ssh-keys\n\n"
