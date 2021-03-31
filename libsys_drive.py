from __future__ import print_function
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_EMAIL = 'libsys@sul-libsys-files.iam.gserviceaccount.com'
SERVICE_ACCOUNT_PKCS12_FILE_PATH = 'sul-libsys-files-7c74e969a1ee.p12'

def main():
    credentials = ServiceAccountCredentials.from_p12_keyfile(
        SERVICE_ACCOUNT_EMAIL,
        SERVICE_ACCOUNT_PKCS12_FILE_PATH,
        'notasecret',
        scopes=SCOPES)

    # credentials = credentials.create_delegated('jgreben@stanford.edu')

    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build("drive", "v3", http=http)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    main()