#!/bin/bash

docker rm backup --force
docker build . -t gdrive-backup:latest
docker run --name backup --env-file ./.env -v ./data:/data -v ./credentials.json:/service-account.json -d gdrive-backup
docker exec -it backup tail -f /var/log/backup.log
