import io
import os
import re
import tarfile
import time
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# Define variables
WORLD = os.getenv('WORLD', 'world')
SERVICE_ACCOUNT = 'tora.json'
DRIVE_BACKUP_DIR = os.getenv('DRIVE_BACKUP_DIR', '1pBX-Lt3upeb519D17_XK4PH-Mbzbmbud')
BACKUP_INTERVAL = os.getenv('BACKUP_INTERVAL', '1d')


def sleep(duration: str):
    # Dictionary to convert units to seconds
    unit_to_seconds = {
        's': 1,
        'h': 3600,
        'd': 86400,
        'm': 30 * 86400,  # Assuming 30 days per month
        'y': 365 * 86400  # Assuming 365 days per year
    }

    # Regular expression to match the duration string (number followed by a unit)
    pattern = re.compile(r'(\d+)([shdmy])')

    # Find all matches in the input string
    matches = pattern.findall(duration)

    if not matches:
        raise ValueError("Invalid duration string format")

    total_seconds = 0

    # Calculate total seconds
    for value, unit in matches:
        total_seconds += int(value) * unit_to_seconds[unit]

    time.sleep(total_seconds)


def create_backup(directory: str = WORLD) -> io.BytesIO:
    archive = io.BytesIO()
    with tarfile.open(fileobj=archive, mode='w:gz') as tar:
        tar.add(f'/data/{directory}', arcname=f'/')

    archive.seek(0)

    return archive


def upload_to_gdrive(archive: io.BytesIO):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT,
        scopes=['https://www.googleapis.com/auth/drive.file']
    )
    service = build('drive', 'v3', credentials=creds)

    file_name = f'minecraft_backup_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.tar.gz'

    file_metadata = {
        'name': file_name,
        'parents': [DRIVE_BACKUP_DIR]
    }
    media = MediaIoBaseUpload(archive, mimetype='application/gzip')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return f'https://drive.google.com/file/d/{file["id"]}'


def backup():
    print('Creating backup...')

    archive = create_backup()
    file_url = upload_to_gdrive(archive)
    archive.close()

    print(f'Backup created successfully! {file_url}')
    print(f'Next backup in {BACKUP_INTERVAL}')


if __name__ == '__main__':
    print('Starting backup process...')
    while True:
        backup()
        sleep(BACKUP_INTERVAL)
