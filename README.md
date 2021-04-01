# libsys-drive

## Sharing Google Drive with Service Account
In order for the libsys service to process files that are added to a Google drive, 
the file uploader must do the following:

1. Create a new folder in their Google drive named "Libsys-{projectName}"
1. Share the folder with the libsys service account 
    - Right-click on folder
    - Select Share
    - Add people or groups: `libsys@sul-libsys-files.iam.gserviceaccount.com`
    - Uncheck "Notify people"
    - Click Share
    - When prompted to "Share outside of organization?" click Share anyway
1. Upload files into the shared folder to be processed by libsys services. It is possible to 
create sub-folders in this shared drive as appropriate to the specific project.

## Running the script
From the command line, or in a shell script, or via the crontab, call the python script as follows:
```
python libsys_drive.py {Google-Drive-shared-folder-name} {files-download-directory}
```
e.g.
```
python libsys_drive.py MapScan /tmp/storage/dir
```
In this example if there are any files shared with the service account with the folder named `MapScan`, they will be
downloaded to the local folder `/tmp/storage/dir`.

## Development
### Setup
1. Clone this repository
1. Enter directory and install dependencies:
```
cd libsys-sdrive && pip install -r requirements.txt
```  
