import sys
import argparse
from nsvision import classifier

description = """
This script renames the files in the folder.
Rename format is as follow- {fix_name}_{number}.{extension}
There will be a fix or common name for all the files in the folder followed
by a unique number and with the orignal file extension.
The folder should contain only files (like images,txt).
"""

parser = argparse.ArgumentParser(
    description=description,
    usage="Rename the files in the given folder",
    formatter_class=argparse.RawTextHelpFormatter,
)

required_args = parser.add_argument_group("required arguments")

required_args.add_argument(
    "-n", "--name", required=True, help="Common name for all the files to be rename"
)

required_args.add_argument(
    "-f",
    "--folder_path",
    required=True,
    help='Path of the folder in which files to be rename"',
)

parser.add_argument(
    "-i", "--number", default=1, help="Number from which renaming is to start"
)


def main():
    args = parser.parse_args()
    print(
        "Renaming files in the folder", f"folder path: {args.folder_path}\n", sep="\n"
    )
    classifier.rename_files(
        name=args.name, folder_path=args.folder_path, number=int(args.number)
    )


if __name__ == "__main__":
    sys.exit(main())
