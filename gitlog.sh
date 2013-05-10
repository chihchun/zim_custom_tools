#!/bin/sh

# This script help you to track your note history with git.
# You can manage your zim notes with SparkShare, which auto-sync the nodes 
# into git repository.
# 
# Usage: terminator -x gitlog.sh %n %s

set -e

cd $1

git log \
    --pretty=format:'%Cred%h%Creset %ci %Cgreen(%cr)%Creset' --abbrev-commit \
    --stat --summary  \
    --full-history \
    --date-order \
    --no-decorate \
    --follow \
    -- $2
