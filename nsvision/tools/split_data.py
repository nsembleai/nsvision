import sys
import argparse
from nsvision import classifier

description = """
This script is specifically design for image classification task
to do image classification we need data into a specific format
this script divide the data folder containing class folder  into train, validation, test and qa folders.
The input folder shoud have the following format:
data/
    class1/
        img1
        img2
        ....
    class2/
        img1
...........
In order to give output in this format
classified_data/
    train/
        class1/
            img1
            img11
            ....
        class2/
            img1
            img2
            ....
    test/
        class1/
            img1....
the order of splitting the data is train,validation,test and quality_assurance
if anyone wants to divide the data only in two or three category, then let other value be zero
this works on any file types.
"""

parser = argparse.ArgumentParser(
    description=description,
    usage="Divide image data folder into train, validation, test and qa for image classification",
    formatter_class=argparse.RawTextHelpFormatter,
)

required_args = parser.add_argument_group("required arguments:")

required_args.add_argument(
    "-d", "--data_dir", required=True, help="Path to folder containing images"
)

required_args.add_argument(
    "-r",
    "--ratio",
    required=True,
    help='Tuple of ratio in the order of (train,val,test,qa) for ex class_split -r "(70,10,10,10)"',
)

parser.add_argument(
    "-l",
    "--generate_labels_txt",
    default=False,
    help="Generate labels.txt containing class names",
)


def main():
    args = parser.parse_args()
    print("Image data splitting tool", f"data path: {args.data_dir}\n", sep="\n")
    classifier.split_image_data(
        data_dir=args.data_dir,
        ratio=tuple(eval(args.ratio)),
        generate_labels_txt=args.generate_labels_txt,
    )


if __name__ == "__main__":
    sys.exit(main())
