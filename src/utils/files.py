import glob
import os


def get_all_files_glob(dir_root, list_extension=None):
    if list_extension is None:
        list_extension = ["jpg"]

    list_files = []
    for ext_index, ext in enumerate(list_extension):
        list_files.extend(glob.glob(os.path.join(dir_root, f"*.{ext}")))

    print(f"len_list_files: {len(list_files)}\n{list_files}")
    return list_files


def get_all_files_os_walk(dir_root, list_extension=None):
    if list_extension is None:
        list_extension = ["jpg"]

    list_files = []
    for ext_index, ext in enumerate(list_extension):

        for (dir_path, dir_names, filenames) in os.walk(dir_root):
            list_ext_filtered = [tmp_path for tmp_path in filenames if tmp_path.endswith(f".{ext}")]
            list_files.extend(list_ext_filtered)

    print(f"len_list_files: {len(list_files)}\n{list_files}")
    return list_files
