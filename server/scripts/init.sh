#!/bin/bash

cp shell.py /home/test/shell.py
chmod o+rx /home/test/problems/
chmod o+rx '/home/test/problems/'$1'/'
chmod o+r '/home/test/problems/'$1'/classes.py'
chmod o+rx '/home/test/problems/'$1'/strategies/'
chmod o-r '/home/test/problems/'$1'/strategies/'*
