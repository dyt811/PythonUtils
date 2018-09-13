import os
from datetime import datetime
import logging
import shutil
from tqdm import tqdm


def flatcopy(file_list, destination_path, check_function):
    """
    Takes in a list of files and flatten them to the desintation path while ensure they are guarnteed to be unique files.
    :param file_list: the list of files from different path.
    :param destination_path:
    :param check_function: the function used to validate every single file.
    """
    logger = logging.getLogger(__name__)
    logger.info("Copying checking and checking files to destination: " + destination_path)

    from shutil import copyfile

    for file in tqdm(file_list):

        # find if the file is DICOM, if not, skip this file.
        if check_function is not None:
            is_DICOM_file, _ = check_function(file)
            if not is_DICOM_file:
                continue

        # get the final path name.
        file_name = os.path.basename(file)
        destination_path_name = os.path.join(destination_path, file_name)

        # check if the final path is unique.
        unique, new_name = is_name_unique(destination_path_name)

        # append date time microsecond string if the file is not unique.
        if not unique:
            destination_path_name = new_name

        copyfile(file, destination_path_name)

def unique_name():
    timestamp = datetime.now().isoformat(sep='T', timespec='auto')
    name = timestamp.replace(":", "_")
    return name

def is_name_unique(path):
    """
    Determine if the proposed file exist and suggest alternative name.
    :param path:
    :return:
    """
    if os.path.exists(path):
        timestamp = datetime.datetime.now().isoformat()
        timestamp = timestamp.replace(':', '')  # Remove : which are not compatible with string

        file, ext = os.path.splitext(path)

        return False, file + "_" + timestamp + "_" + ext
    else:
        return True, path

def zip_with_name(folder_path, output_filename):
    shutil.make_archive(output_filename, 'zip', folder_path)