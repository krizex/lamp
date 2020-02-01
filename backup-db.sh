#!/bin/bash

curl -m 60 https://cronitor.link/UyZpG1/run
make backup-db
if [ -f data/auto-commit.sh ];then
  cd data && ./auto-commit.sh
fi
curl -m 60 https://cronitor.link/UyZpG1/complete
