#!/bin/bash

ROOT_UID=0

id $1
ret=$?
if [[ $ret -ne 0 || $1 = "" ]]; then
    echo "usage: setup <USER>"
    echo IMPORTANT: USER is a user that will run the main process
    echo 'suggested usage: sudo setup $USER'
    exit 1
fi
echo This script will create user 'test' \(if not exist\) remove it\'s password and block password changing for a long time and make some changes in test\'s home catalog, so this script must be executed with root privileges.
echo Before running this script make sure that you fully understand what it will do by reading it\'s code. Author of this script is not responsible for any consequenses.
echo Is this OK \(run the script\)? \(Y/n\) 
read ans
if [ $ans != 'Y' ]; then
    exit 1
fi
# checking that run with root privileges
if [ "$UID" -ne "$ROOT_UID" ]; then
    echo Script needs root privileges
    exit 1
fi

GROUP=`id -gn $1`

id test
ret=$?
if [ $ret -ne 0 ]; then
    echo setup: Creating user test...
    useradd test || exit 1
    echo setup: Created user test.
fi
chown $1 /home/test -R || exit 1
chgrp $GROUP /home/test -R || exit 1
passwd -d test || exit 1
passwd -n 256000 test || exit 1
echo setup: Success
exit 0
