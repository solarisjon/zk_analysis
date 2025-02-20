import os
import shutil

def clean_and_recreate_directory(directory_path) -> None: 
    """
    Removes the specified directory and all its contents, then recreates the directory.

    Args:
        directory_path (str): The path to the directory to be cleaned and recreated.

    Returns:
        None
    """
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    os.makedirs(directory_path)