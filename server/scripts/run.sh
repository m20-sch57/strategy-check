#!/bin/bash

chmod o+r '/home/test/problems/'$1'/strategies/'$2
su - test -c "ulimit -t $3 -v 262144 ; unshare -rn python3 shell.py"
retcode=$?
chmod o-r '/home/test/problems/'$1'/strategies/'$2
exit $retcode
