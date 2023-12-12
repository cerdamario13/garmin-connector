# Google APIs
from googleapiclient.discovery import build as _build
from googleapiclient.http import MediaIoBaseDownload as _MediaIoBaseDownload
from googleapiclient.http import MediaIoBaseUpload as _MediaIoBaseUpload
from google.oauth2 import service_account as _service_account

from wrangles.connectors import file as _file
import io as _io
import pandas as _pd
import re as _re

_schema = {}

# More information regarding auth and keys
# https://developers.google.com/identity/protocols/oauth2/service-account
# be sure to also share the folder with the service account email address as Editor

def _get_id_from_path(service, path, type):
    """
    Get the file ID from the the path provided
    """
    path_list = path.split("/")
    folder_list = path_list[:-1]
    if type == 'read':
        file = _re.search(r'(\w+)\.(xlsx|csv|gsheet|json)', path)[0]
    
    # get the root folder id from the path
    query = f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder_list[0]}' and trashed = false"
    results = service.files().list(q=query, fields="files(id)", supportsAllDrives=True,  includeItemsFromAllDrives=True).execute()
    if results['files'] == []:
        raise ValueError(f"Folder '{folder_list[0]}' does not exist in Google Drive or does not have the correct Service Account permissions.""")
    root_id = results['files'][0]['id']
    
    # Build the id_stack to keep track of folder ids
    id_stack = root_id # initialize with the root folder id
    file_id = ""
    
    # iterate through the path
    for part in path_list[1:]:
        
        # Check if part is the last element in the list
        if part == path_list[-1] and type == 'read':
            # search for a file using the id_stack
            query = f"'{id_stack}' in parents and mimeType != 'application/vnd.google-apps.folder'"
            results = service.files().list(q=query, fields="files(id, name)", supportsAllDrives=True,  includeItemsFromAllDrives=True).execute()
            
            # check if the file exists in last folder in the path
            if [x['name'] for x in results['files'] if x['name'] == file]:
                file_id = [x['id'] for x in results['files'] if x['name'] == file][0]
                return file_id
            
        elif part == path_list[-1] and type == 'write':
            query = f"'{id_stack}' in parents and mimeType = 'application/vnd.google-apps.folder'"
            results = service.files().list(q=query, fields="files(id, name)", supportsAllDrives=True,  includeItemsFromAllDrives=True).execute()
            
            # check if the file exists in last folder in the path and get id
            if [x['name'] for x in results['files'] if x['name'] == part]:
                file_id = [x['id'] for x in results['files'] if x['name'] == part][0]
                return file_id
        
        else:
            # Keep iterating through the path/folders. using the folder id, check that the folder contains the sub folder
            query = f"'{id_stack}' in parents and mimeType = 'application/vnd.google-apps.folder'"
            results = service.files().list(q=query, fields="files(id, name)", supportsAllDrives=True,  includeItemsFromAllDrives=True).execute()
            
            # check if the sub folder exists in the current folder
        if [x['name'] for x in results['files'] if x['name'] == part]:
            # update the id_stack
            id_stack = [x['id'] for x in results['files'] if x['name'] == part][0]
    
    return None # if nothing is found


def read(
        file: str,
        project_id: str,
        private_key_id: str,
        private_key: str,
        client_email: str,
        client_id: str,
        **kwargs
        ) -> _pd.DataFrame:
    """
    Read a file from Google Drive using a Service Account
    
    :param file: ID of the file that contains the desired data or the sharable link or the file path
    :param project_id: ID of the Google project
    :param private_key_id: Private key identification of the Google project
    :param private_key: Private key of the Google Project
    :param client_email: Email of the Service account (Project)
    :param client_id: Client ID of the Google Project
    """
    # Remove extra back slashed from private key
    private_key = _re.sub("\\\\n", "\\n", private_key)
        
    # Credentials information
    creds_dict = {
        "type": "service_account",
        "project_id": project_id,
        "private_key_id": private_key_id,
        "private_key": private_key,
        "client_email": client_email,
        "client_id": client_id,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        }
    
    # Create the appropriate Google Service
    scope = ['https://www.googleapis.com/auth/drive']
    creds = _service_account.Credentials.from_service_account_info(
        info=creds_dict,
        scopes=scope,
        **kwargs
    )
    
    # Authenticate and construct service.
    service = _build(
       'drive',
        'v3',
        credentials=creds
        )
    
    # check if user provided sharable link or file id
    if 'drive.google.com' in file or 'docs.google.com' in file:
        parts = file.split('/')
        for i, part in enumerate(parts):
            if part == 'd':
                file_id = parts[i + 1]
                break
    
    # check if the share link is a path
    elif '/' in file and 'https://' not in file:
        file_id = _get_id_from_path(service, file, 'read')
        if file_id == None:
            raise ValueError(f"Invalid path: '{file}'")
        
    # this is just the model id
    else :
        file_id = file
    
    # Determine the mimeType based on file metadata
    file_data = service.files().get(
        fileId=file_id,
        fields='*',
        supportsAllDrives=True,
    ).execute()
    

    # For sheets files
    if file_data['mimeType'] == 'application/vnd.google-apps.spreadsheet':
        file_mimeType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        file_type = 'xlsx' # Only needed for sheets
    
        request = service.files().export_media(
            fileId=file_id,
            mimeType=file_mimeType,
            )
    
    # For Excel files
    elif file_data['mimeType'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        request = service.files().get_media(
            fileId=file_id,
        )
        
    # For csv files
    elif file_data['mimeType'] == 'text/csv' or file_data['mimeType'] == 'application/csv':
        request = service.files().get_media(
            fileId=file_id,
        )
    
    # For JSON files
    elif file_data['mimeType'] == 'application/json':
        file_mimeType = ''
        request = service.files().get_media(
            fileId=file_id,
        )
    
    else:
        raise ValueError('File type not supported. File type must be: Google Sheets, Excel, CSV, or JSON.')

    # Downloading the files
    fh = _io.BytesIO()
    downloader = _MediaIoBaseDownload(fd=fh, request=request)
    done = False
    while not done:
        done = downloader.next_chunk()
    fh.seek(0)
    
    # file to pandas dataFrame
    response = _io.BytesIO(fh.read())
    if file_data['mimeType'] == 'application/vnd.google-apps.spreadsheet':
        df = _file.read(f"{file_data['name']}.{file_type}", file_object=response)
    else:
        df = _file.read(f"{file_data['name']}", file_object=response)

    return df