import argparse
import fnmatch
import os
import shutil
from typing import Tuple


EXTENSION_DEFAULT = ["*.*"]
FILTER_STRING_DEFAULT = ""


def copy_files(source, output, filter_str, extensions, dry_run):
    files_list = []

    if source is None:
        source = os.getcwd()
    for dirpath, dirnames, file_names in os.walk(source):
        files = filter_extension(file_names, extensions)
        files, ignored_files = filter_substr(files, filter_str)
        for f in files:
            abs_path = os.path.join(dirpath, f)
            print("Marking %s" % abs_path)
            files_list.append(abs_path)

        for f in ignored_files:
            abs_path = os.path.join(dirpath, f)
            print("Skipping %s" % abs_path)

    if dry_run is False:
        if output is None:
            output = os.path.join(os.getcwd(), "output")
            if os.path.exists(output) is False:
                os.mkdir(output)

        if os.path.exists(output) is False:
            output = os.path.join(os.getcwd(), output)
            if os.path.exists(output) is False:
                os.mkdir(output)

    file_list_length = len(files_list)
    for i in range(0, file_list_length):
        f = files_list[i]
        correct_filename = check_existence_and_rename(os.path.basename(f), output, suffix=files_list.index(f))
        percent = ((i + 1) / file_list_length) * 100
        if dry_run is False:
            print("Copying files %.2f%%" % percent, end="\r")
            shutil.copy2(f, os.path.join(output, correct_filename))
        else:
            print("Fake copying files %.2f%%" % percent, end="\r")


def filter_extension(file_names: list, extensions: list) -> list:
    return [f for f in file_names for file_extension in extensions if fnmatch.fnmatch(f, file_extension)]


def filter_substr(file_list: list, filter_str: str) -> Tuple[list, list]:
    files_to_add = set()
    files_to_ignore = set()
    for f in file_list:
        files_to_add.add(f)
        if filter_str and filter_str in f:
            f_duplicate = f.replace(filter_str, "")
            if f_duplicate in file_list:
                files_to_ignore.add(f_duplicate)

    filtered = list(files_to_add.difference(files_to_ignore))
    files_to_ignore = list(files_to_ignore)

    filtered.sort()
    files_to_ignore.sort()
    return filtered, files_to_ignore


def check_existence_and_rename(file_name: str, dest_dir: str, suffix: int) -> str:
    new_name = file_name
    if os.path.exists(os.path.join(dest_dir, file_name)):
        name, extension = os.path.splitext(new_name)
        new_name = name + "_%s%s" % (str(suffix), extension)
        return check_existence_and_rename(dest_dir, new_name, suffix+1)
    return new_name


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Filter and copy files by file extension and substrings")
    parser.add_argument("-d", "--dry", dest="dry", action="store_false", help="Dry run. Affected files will be logged, "
                                                                              "but no files will be copied")
    parser.add_argument("-e", "--extensions", action="store", dest="extension", default=EXTENSION_DEFAULT, nargs="*",
                        help="The file extension to filter with, e.g. -e *.jpg. Default is .* for all file extensions. "
                             "Can also be a list, e.g. -e *.jpg *.png")
    parser.add_argument("-f", "--filter", dest="filterstring", action="store", default=FILTER_STRING_DEFAULT,
                        help="Filter string to search for if duplicates are to be expected. For example A.pdf will be "
                             "ignored and A_edited.pdf will be kept if -f _edited")
    parser.add_argument("-o", "--output", dest="output", action="store",
                        help="Output folder to copy files to. Either absolute or relative.")
    parser.add_argument("-s", "--source", dest="source", action="store", help="Source folder to check. ""Either "
                                                                              "absolute or relative.")

    args = parser.parse_args()
    if args.extension == EXTENSION_DEFAULT and args.filterstring == FILTER_STRING_DEFAULT:
        parser.error("No target option was given. Add either --extensions or --filter. Use --help for help.")

    copy_files(args.source, args.output, args.filterstring, args.extension, args.dry)
