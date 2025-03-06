import io
import os
import tarfile
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# Define variables
DIRECTORY = os.getenv('BACKUP_DIRECTORY').strip('"\'')
SERVICE_ACCOUNT = '/service-account.json'
DRIVE_BACKUP_DIR = os.getenv('GDRIVE_BACKUP_FOLDER_ID').strip('"\'')
BACKUP_FILE_NAME_PREFIX = os.getenv('FILE_PREFIX', 'backup').strip('"\'')
COPIES_TO_KEEP = int(os.getenv('COPIES_TO_KEEP', 5))


def create_backup(directory: str = DIRECTORY) -> io.BytesIO:
    archive = io.BytesIO()
    with tarfile.open(fileobj=archive, mode='w:gz') as tar:
        tar.add(f'{directory}', arcname=f'/')

    archive.seek(0)

    return archive


def upload_to_gdrive(archive: io.BytesIO):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT,
        scopes=['https://www.googleapis.com/auth/drive.file']
    )
    service = build('drive', 'v3', credentials=creds)

    # Delete old backups
    files = service.files().list(q=f"'{DRIVE_BACKUP_DIR}' in parents").execute()
    files = files.get('files', [])
    files.sort(key=lambda x: datetime.fromisoformat(x['createdTime'].rstrip('Z')))

    if len(files) >= COPIES_TO_KEEP:
        for file in files[COPIES_TO_KEEP:]:
            service.files().delete(fileId=file['id']).execute()

        print(f'{len(files) - COPIES_TO_KEEP} old backups deleted')

    file_name = f'{BACKUP_FILE_NAME_PREFIX}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.tar.gz'

    file_metadata = {
        'name': file_name,
        'parents': [DRIVE_BACKUP_DIR]
    }
    media = MediaIoBaseUpload(archive, mimetype='application/gzip')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return f'https://drive.google.com/file/d/{file["id"]}'


def main():
    print(f'Creating backup for {DIRECTORY}...')

    archive = create_backup()
    file_url = upload_to_gdrive(archive)
    archive.close()

    print(f'Backup {datetime.now()} successful! {file_url}')


if __name__ == '__main__':
    main()
