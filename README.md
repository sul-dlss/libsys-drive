# libsys-drive

## Sharing Google Drive with Service Account
In order for the libsys service to process files that are added to a Google drive, 
the file uploader must do the following:

1. There is a shared google folder named `LibsysFileUploads`
1. Create a new folder in `LibsysFileUploads` named `{projectName}`
1. Share the `{projectName}` folder with the Staff user (the service account has access at the parent level): 
    - Right-click on folder
    - Select Share
    - Add the Staff users (or groups) who need to upload the files
    - Click Share
    - If prompted to "Share outside of organization?" click `Share anyway`
1. Upload files into the shared folder to be processed by libsys services. It is possible to 
create sub-folders in this shared drive as appropriate to the specific project.

## Running the script
From the command line, or in a shell script, or via the crontab, call the python script as follows:
```
python libsys_file_downloads.py {Google-Drive-shared-folder-name} {download-directory-for-files}
```
e.g.
```
python libsys_file_downloads.py MapScan /s/SUL/Dataload/MapScanning
```
In this example if there are any files shared with the service account with the folder named `MapScan`, they will be
downloaded to the local folder `/s/SUL/Dataload/MapScanning`. If no download folder is provided it will default to the 
current working directory.

The file id will be saved as regular file named `{file['id']}` in the DOWNLOADED_FILES_PATH location, or the default
current working directory.

## Development
### Setup
1. Clone this repository
1. Enter directory and install dependencies:
```
cd libsys-sdrive && pip install -r requirements.txt
```  
