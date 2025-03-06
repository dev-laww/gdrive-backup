#!/bin/sh
set -e  # Exit on error

# Check for required files
required_files="service-account.json"
missing_files=""

for file in $required_files; do
    if [ ! -f "$file" ]; then
        missing_files="$missing_files $file"
    fi
done

# Check for required environment variables
required_env_vars="BACKUP_DIRECTORY GDRIVE_BACKUP_FOLDER_ID"
missing_vars=""

for var in $required_env_vars; do
    if [ -z "$(eval echo \$$var)" ]; then
        missing_vars="$missing_vars $var"
    fi
done

if [ -n "$missing_vars" ]; then
    echo "Missing required environment variables:$missing_vars" >&2
    echo "- If you are using docker-compose, you can set these in the .env file." >&2
    echo "- If you are using docker run, you can set these with the -e flag. i.e docker run --name gdrive-backup -e DIRECTORY=/path/to/backup -e DRIVE_BACKUP_DIR=/path/to/drive/backup gdrive-backup" >&2
    echo "  or you can use the --env-file flag to specify a file with the environment variables." >&2
    exit 1
fi

# setup cron job
BACKUP_SCHEDULE=${BACKUP_SCHEDULE:-"0 0 * * *"}
CLEAN_SCHEDULE=$(echo "$BACKUP_SCHEDULE" | sed -E "s/^['\"]+//; s/['\"]+$//")

touch /var/log/backup.log

echo "Setting up cron job with schedule: $CLEAN_SCHEDULE"
cat <<EOF > /etc/cron.d/backup
SHELL=/bin/sh
VIRTUAL_ENV=/app/.venv
PATH=/app/.venv/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

$CLEAN_SCHEDULE root python -u /app/main.py >> /var/log/backup.log 2>&1
EOF

chmod 0644 /etc/cron.d/backup
printenv > /etc/environment

echo "Starting cron..."

cron & tail -f /var/log/backup.log