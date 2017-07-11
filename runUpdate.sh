#!/bin/bash
cd /var/www/html/Manipulate/



git fetch origin master
git status
git reset --hard origin/master
