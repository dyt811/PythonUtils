import os
from typing import List
import random
import re
from pathlib import Path
import shutil


def is_empty(input_folder):

    # when folder does not exist
    if not os.path.exists(input_folder):
        return True

    # the the folder is not empty.
    if len(os.listdir(input_folder)) > 0:
        return False

    # must be empty then
    return True


def recursive_list_re(root_dicom_path: str or Path, re_pattern: str):
    """
    load all the files, validate them against a regular expression in the FILE NAME and then pass it on as a file list.
    :param root_dicom_path:
    :return: ABSOLUTE PATH of all files in the folder.
    """
    global file_list
    file_list = []

    for root, directories, filenames in os.walk(root_dicom_path):
        for filename in filenames:
            # Compile the regular expression provided.
            pattern = re.compile(re_pattern)
            found = pattern.search(filename)

            # When any match is found
            if found is not None:
                file_list.append(os.path.join(root, filename))
    return file_list


def recursive_list(root_dicom_path: str or Path) -> List[str]:
    """
    load all the files, return a filelist with FULL PATH
    :param root_dicom_path:
    :return: ABSOLUTE PATH of all files in the folder.
    """
    global file_list
    file_list = []

    for root, directories, filenames in os.walk(root_dicom_path):
        # for directory in directories:
        # file_list.append(os.path.join(root, directory))
        for filename in filenames:
            file_list.append(os.path.join(root, filename))
    return file_list


def change(input_folder):
    """
    Change into a folder intellgently throw error if needed be.
    :param input_folder:
    :return:
    """
    if os.path.exists(input_folder) and os.path.isdir(input_folder):
        os.chdir(input_folder)
        return
    elif os.path.exists(input_folder) and os.path.isfile(input_folder):
        raise ValueError("Input is not a folder path but a file.")
    elif not os.path.exists(input_folder):
        os.makedirs(input_folder)
        os.chdir(input_folder)
    else:
        raise ValueError("Unanticipated input")


def create(input_folder, nuke_it=False, really_nuke_it=False):
    """
    Create a folder intellgently throw error if needed be.
    :param input_folder:
    :return:
    """
    if os.path.exists(input_folder) and is_empty(input_folder):
        return
    elif (
        os.path.exists(input_folder) and not is_empty(input_folder) and nuke_it is False
    ):
        raise ValueError(
            f"Folder {input_folder} exist and not empty, since you didn't want to nuke it, you go deal with it!"
        )
    elif (
        os.path.exists(input_folder)
        and not is_empty(input_folder)
        and nuke_it
        and really_nuke_it
    ):
        print("NUKING THAT DIRECTORY!!")
        shutil.rmtree(input_folder, ignore_errors=True)
        os.makedirs(input_folder)
    elif not os.path.exists(input_folder):
        os.makedirs(input_folder)
    else:
        raise ValueError


def create_batch(list_path_folders: List[Path] or List[str]):
    """
    Simple batch wrapper for
    :param list_path_folders:
    :return:
    """
    for folder in list_path_folders:
        create(folder)


def get_abspath(path, levels_above):
    """
    Thie function takes the path (contain the folder or the file given) given and provide relative path levels up.
    :type levels_above: object
    :param path: can be a folde or a path.
    :param levels_above:
    :return:
    """
    # assert levels_above >= 0
    if os.path.isfile(path):
        # since it is a FILE, dirname will only return the CURRENT dir of containing the file. Hence needs to increase the counter.
        levels_above = levels_above + 1
    elif os.path.isdir(path):
        # since it is a FOLDER, no need to look up furhter.
        pass

    returnPath = path

    counter = levels_above

    print(returnPath)

    while counter > 0:
        returnPath = os.path.dirname(returnPath)  # Directory of the Module directory
        counter = counter - 1
        print(returnPath)

    return returnPath


def flatcopy(folder, destination_path):
    from file import flatcopy as file_flatcopy

    filelist = recursive_list(folder)
    file_flatcopy(filelist, destination_path, None)


def random_draw(folder_path, numbers, repeat):
    """
    randomly explore a folder and return lists of files from there
    :param folder_path:
    :param numbers:
    :param repeat:
    :return: a file list of file names with aboslute path.
    """
    filelist = []

    total_files = recursive_list(folder_path)

    if repeat:
        for x in range(1, numbers):
            index = random.randint(0, len(total_files))
            filelist.append(total_files[index])
    else:
        for x in range(1, numbers):
            # Escape loop when out of files to choose from and cannot repeat choose.
            if len(total_files) == 0:
                continue

            # otherwise, randomly sample from the updated total files count
            index = random.randint(0, len(total_files))

            # and add that items to the filelist after popping it.
            filelist.append(total_files.pop(index))

    return filelist


if __name__ == "__main__":
    print(get_abspath(r"C:\ProgramData\Anaconda3\p\\", 1))
