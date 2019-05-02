#!/bin/bash

curl -m 60 https://cronitor.link/UyZpG1/run
make backup-db
curl -m 60 https://cronitor.link/UyZpG1/complete
