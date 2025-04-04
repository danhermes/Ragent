import dropbox
from autocoder_agent.config import DROPBOX_TOKEN

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def file_exists(path):
    try:
        dbx.files_get_metadata(path)
        return True
    except dropbox.exceptions.ApiError:
        return False

def delete_file(path):
    try:
        dbx.files_delete_v2(path)
    except dropbox.exceptions.ApiError:
        pass
