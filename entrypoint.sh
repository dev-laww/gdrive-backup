#!/bin/sh
set -e  # Exit on error

# List of required environment variables
required_env_vars="DIRECTORY DRIVE_BACKUP_DIR"
missing_vars=""

# Check for missing environment variables
for var in $required_env_vars; do
    if [ -z "$(eval echo \$$var)" ]; then
        missing_vars="$missing_vars $var"
    fi
done

# Exit with error if any required variables are missing
if [ -n "$missing_vars" ]; then
    echo "Missing required environment variables:$missing_vars" >&2
    echo "- If you are using docker-compose, you can set these in the .env file." >&2
    echo "- If you are using docker run, you can set these with the -e flag. i.e docker run --name gdrive-backup -e DIRECTORY=/path/to/backup -e DRIVE_BACKUP_DIR=/path/to/drive/backup gdrive-backup" >&2
    echo "  or you can use the --env-file flag to specify a file with the environment variables." >&2
    exit 1
fi

exec "$@"
