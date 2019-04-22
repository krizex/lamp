#!/bin/bash

curl -m 10 https://cronitor.link/UyZpG1/run
make backup-db
curl -m 10 https://cronitor.link/UyZpG1/complete
