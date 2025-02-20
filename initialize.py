import os
import shutil

# Function to clean and recreate the uploads directory
def clean_and_recreate_directory(directory_path) -> None: 
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    os.makedirs(directory_path)