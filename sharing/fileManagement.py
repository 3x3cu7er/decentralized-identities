import shutil
import os

# When user upload a file a unique directory is created. (this fun is not used when sharing is done)
'''
In Django, when you specify a function as the upload_to parameter for a FileField, Django will call that function with two arguments:

The instance of the model to which the FileField is attached.
The filename of the file being uploaded.
'''
def user_directory_path(File, filename):
    return f'user_{File.owner.id}/file/{filename}'

def share_file_path(File):
    return f'media/user_{File.owner.id}/file'

def shareFile(source_path, destination_path):
   
    shutil.copy2(source_path, destination_path)

    print(f"File shared successfully from {source_path} to {destination_path}")

def file_exists_in_folder(folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    return os.path.exists(file_path)

