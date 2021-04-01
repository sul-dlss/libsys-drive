from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import io
import sys

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_EMAIL = 'libsys@sul-libsys-files.iam.gserviceaccount.com'
SERVICE_ACCOUNT_PKCS12_FILE_PATH = 'cert/sul-libsys-files-7c74e969a1ee.p12'

def main(folder_name, download_directory):
    credentials = ServiceAccountCredentials.from_p12_keyfile(
        SERVICE_ACCOUNT_EMAIL,
        SERVICE_ACCOUNT_PKCS12_FILE_PATH,
        'notasecret',
        scopes=SCOPES)

    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build("drive", "v3", http=http)

    # Find all the shared folders of the service account
    folder_results = service.files().list(
        fields="nextPageToken, files(id, name)",
        q = "mimeType = 'application/vnd.google-apps.folder'",
    ).execute()

    """
    Loop through all the folders and find the folder id 
        of the folder name provided from the command line
    """
    folders = folder_results.get('files', [])
    folder_id = None

    if not folders:
        sys.exit(f'No folders found.')
    else:
        for folder in folders:
            if folder['name'] == folder_name:
                # print("Found: %s " % folder_name, ": %s" % folder_id)
                folder_id = folder['id']

    if folder_id is None:
        sys.exit(f'No folders found named {folder_name}.')

    """
    Find all the files stored in the found folder id
    """
    file_results = service.files().list(
        fields="nextPageToken, files(id, name, parents)",
        q = f'\'{folder_id}\' in parents'
    ).execute()

    items = file_results.get('files', [])

    if not items:
        sys.exit(f'No files found in Google drive folder {folder_name}.')
    else:
        for item in items:
            try:
                # print("Name: %s, " % item['name'], "File ID: %s, " % item['id'], "Folder ID: %a" % item['parents'])
                request = service.files().export_media(fileId=item['id'], mimeType="text/plain")
                fh = io.FileIO(f'{download_directory}/{item["name"]}', 'wb')
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    # print("Download %d%%." % int(status.progress() * 100))
            except Exception as error:
                sys.exit(f'Name: {item["name"]} File ID: {item["id"]}')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])