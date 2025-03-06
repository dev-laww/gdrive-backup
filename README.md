Below is a complete README file for your GDrive Backup Docker Image:

---

# GDrive Backup Docker Image

This Docker image provides an automated solution for backing up a specified directory to a Google Drive folder. It
leverages a service account for secure authentication and uses a cron schedule to perform regular backups. With volume
support, your backup data remains persistent even if the container is restarted or recreated.

## Features

- **Automated Backups:**  
  Configurable backup schedule using cron syntax (default is every day at midnight).

- **Google Drive Integration:**  
  Uploads backup files to a specified Google Drive folder using a service account.

- **Customizable File Naming:**  
  Optionally add a prefix to your backup file names for easy identification.

- **Persistent Storage:**  
  Attach a Docker volume to keep backup data safe between container restarts.

## Prerequisites

- Docker installed on your system.
- A valid Google Cloud service account with permissions to access Google Drive.
- The Google Drive folder ID where you want to store backups.

## Usage

Run the container with the following command. In this example, you mount the directory you want to back up to
`/path/in/container`:

Docker Command:
```bash
docker run --name gdrive-backup \
  -e GDRIVE_BACKUP_FOLDER_ID=<folder_id> \
  -e BACKUP_DIRECTORY=<directory-to-backup> \
  -v /local/backup-directory:/path/in/container \
  -v /path/to/service-account.json:/service-account.json \
  -d gdrive-backup
```

Docker Compose:
```yaml
services:
  gdrive-backup:
    image: gdrive-backup:latest
    volumes:
      - /local/backup-directory:/path/in/container
      - /path/to/service-account.json:/service-account.json
    environment:
      BACKUP_DIRECTORY: "<directory-to-backup>"
      GDRIVE_BACKUP_DIR_ID: "<folder_id>"
      BACKUP_SCHEDULE: "0 0 * * *"
    restart: always
```

**Notes:**

- Replace `<folder_id>` with your Google Drive folder ID.
- Replace `<directory-to-backup>` with the internal directory path that the container will back up. This should match
  the mount point (`/path/in/container` or `/path/in/container/subfolder`).
- Replace `/local/backup-directory` with the path on your host where the data is stored.

## Environment Variables

- **`GDRIVE_BACKUP_FOLDER_ID`**  
  *Description:* Google Drive folder ID where the backup will be stored.
- **`BACKUP_DIRECTORY`**  
  *Description:* Directory to back up. This should match the directory mounted to `/path/in/container` in the container.
- **`BACKUP_SCHEDULE`**  
  *Description:* Interval for performing backups in cron format.  
  *Default:* `0 0 * * *` (every day at midnight)
- **`BACKUP_FILE_NAME_PREFIX`**  
  *Description:* Prefix for the backup file name for easy identification.  
  *Default:* `backup`

## How It Works

1. **Backup Execution:**  
   The container uses the specified `BACKUP_DIRECTORY` to create a backup archive at intervals defined by
   `BACKUP_SCHEDULE`.

2. **Uploading to Google Drive:**  
   The backup file is uploaded to the Google Drive folder specified by `GDRIVE_BACKUP_FOLDER_ID` using credentials
   provided in the `SERVICE_ACCOUNT_FILE`.

3. **Persistent Storage:**  
   By mounting a local directory to `/path/in/container`, your backup data is stored persistently, ensuring it remains
   available even if the container is restarted.

## Customization

- **Changing the Backup Schedule:**  
  Modify the `BACKUP_SCHEDULE` environment variable to suit your desired backup frequency.

- **Adjusting File Naming:**  
  Update the `BACKUP_FILE_NAME_PREFIX` variable to change how backup files are named.

## Contributing

Contributions are welcome! Feel free to fork this repository and submit a pull request with any enhancements, bug fixes,
or improvements.

## License

This project is licensed under the [MIT License](LICENSE).
