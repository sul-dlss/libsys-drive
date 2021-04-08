from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import httplib2
import io
import os
import sys

DOWNLOADED_FILES_PATH = os.environ.get("DOWNLOADED_FILES_PATH") or "."
SERVICE_ACCOUNT_EMAIL = (
    os.environ.get("SERVICE_ACCOUNT_EMAIL")
    or "libsys@sul-libsys-files.iam.gserviceaccount.com"
)
SERVICE_ACCOUNT_PKCS12_FILE_PATH = (
    os.environ.get("SERVICE_ACCOUNT_PKCS12_FILE_PATH") or "cert/sul-libsys-files.p12"
)


class LibsysFileDownloads:
    def __init__(self, args):
        self.args = args
        folder_name = args[1]

        try:
            download_directory = args[2]
        except IndexError:
            download_directory = "."

        self.gDrive = self.service()

        self.download(folder_name, download_directory)

    @staticmethod
    def credentials():
        return ServiceAccountCredentials.from_p12_keyfile(
            SERVICE_ACCOUNT_EMAIL,
            SERVICE_ACCOUNT_PKCS12_FILE_PATH,
            "notasecret",
            scopes=[
                "https://www.googleapis.com/auth/drive",
            ],
        )

    def http(self):
        return self.credentials().authorize(httplib2.Http())

    def service(self):
        return build("drive", "v3", http=self.http())

    def service_results(self, query):
        return (
            self.gDrive.files()
            .list(
                supportsAllDrives="true",
                includeItemsFromAllDrives="true",
                corpora="allDrives",
                fields="nextPageToken, files(id, name, parents)",
                q=query,
            )
            .execute()
        )

    def folder_id(self, folder_name):
        """
        Loop through all the folders and find the folder id
        of the folder name provided from the command line
        """
        folder_id = None
        folders = self.service_results(
            "mimeType='application/vnd.google-apps.folder'"
        ).get("files", [])

        if not folders:
            sys.exit("No folders found.")
        else:
            for folder in folders:
                if folder["name"] == folder_name:
                    folder_id = folder["id"]
                    # print("Folder Name: %s " % folder_name, ": %s" % folder_id)

        if folder_id is None:
            sys.exit("No folders found named %s." % folder_name)

        return folder_id

    def file_ids(self, folder_name):
        """
        Find all the files stored in the found folder id
        """
        folder = self.folder_id(folder_name)

        files = self.service_results(f"'{folder}' in parents").get("files", [])

        if not files:
            sys.exit("No files found in Google drive folder %s." % folder_name)
        else:
            return files

    def download(self, folder_name, download_directory):
        items = self.file_ids(folder_name)
        for item in items:
            previously_downloaded = os.listdir(DOWNLOADED_FILES_PATH)
            if not item["id"] in previously_downloaded:
                try:
                    """
                    print(
                        "Name: %s," % item['name'],
                        "File ID: %s, " % item['id'],
                        "Folder ID: %a" % item['parents']
                    )
                    """

                    # TODO: determine if the text/plain mime type will work for MARC files
                    request = self.gDrive.files().export_media(
                        fileId=item["id"], mimeType="text/plain"
                    )
                    fh = io.FileIO("%s/%s" % (download_directory, item["name"]), "wb")
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        # print("Download %d%%." % int(status.progress() * 100))
                    Path("%s/%s" % (DOWNLOADED_FILES_PATH, item["id"])).touch()
                except Exception as error:
                    sys.exit(
                        "Name: %s, File ID: %s: %s" % (item["name"], item["id"], error)
                    )


if __name__ == "__main__":
    LibsysFileDownloads(sys.argv)
