from libsys_file_downloads import LibsysFileDownloads
from pathlib import Path
import os

def download_test_file(folder):
  LibsysFileDownloads(['libsys_file_downloads', folder])

def cleanup_downloaded_files(file):
  os.remove(file)

def test_files_exist(
    folder = 'Test', # the name of the established test folder
    file = 'LibsysFilesDownloadTest', # the name of the established test file
    id = '1MmRVzwtNDeoONlNUlEQjKp8hxE-TMxbDyc9KBUr95jM' # the ID of the established test file
  ):

  download_test_file(folder)
  p = Path(file)

  assert p.is_file()
  assert p.stat().st_size == 18 # the size of the established test file

  cleanup_downloaded_files(file)
  cleanup_downloaded_files(id)
