import os
import sys
import argparse
from nsvision import classifier
try:
	from zipfile import ZipFile as zip_file
except:
	zip_file = None

description = """
This python file is for the Downloaded zip file from https://ndownloader.figshare.com/articles/1512427/versions/5
This file converts all the .mat file in the above zip folder into the given extension file format(default .jpg)
All the converted files will be save in separate folder named brain_tumor_data in their respective tumor name folder
Arguments - 
Input 
1. base_dir - Filepath of zip downloaded file
2. ext      - Extension in which mat files to be converted
"""


parser =  argparse.ArgumentParser(
		description = description,
        usage = "converts all the .mat file in the given zip folder into the given extension file format(default jpg)",
        formatter_class=argparse.RawTextHelpFormatter
)

required_args = parser.add_argument_group('required arguments')

required_args.add_argument(
		"-b",
		"--base_dir",
		required = True,
		help = "Folderpath of the zip folder downloaded from figshare"
)
	
parser.add_argument(
		"-e",
		"--extension",
		default = 'jpg',
		help='Extension of the converted image"'
)

def extract_zipfolder(zip_dir,unzip_dir):
	"""
	This function extract given zipfile"""
	if zip_file is None:
		raise ImportError("zipfile is required"
			"Install using `pip install zipfile`")

	try:
		zf = zip_file(zip_dir, 'r')
		zf.extractall(unzip_dir)
		zf.close()
		return unzip_dir
	except:
		print("Failed to unzip",zip_dir)


def make_tumor_folder(label,dst_dir,num,ext,ns_image):
	"""
	This function converts save oil image into given image extension format
	"""
	tumor_labels = {"1.0":"meningioma","2.0":"glioma","3.0":"pituitary"}
	tumor_name = tumor_labels[str(label)]
	tumor_folder = os.path.join(os.path.dirname(dst_dir),"brain_tumor_data/" + tumor_name)
	os.makedirs(tumor_folder,exist_ok=True)
	filename = f"{tumor_name}_{num}.{ext}"
	dstpath = os.path.join(tumor_folder,filename)
	ns_image.save(dstpath)



def convert_tumor_matdata_to_jpg(base_dir,extension):
	"""
	This function extract files from given zip folder, convert all files into jpg format
	and save all according to their respective classes in a dir named brain_tumor_data
	Arguments:
	base_dir - folderpath of zip folder (type - str) 
	"""

	
	if extension == 'jpg' or extension == 'JPEG' or extension == 'JPG' or extension == 'jpeg':
		print('jpg supports upto 3 channels only')
	

	
	dst_dir = os.path.join(os.path.dirname(base_dir),"tumor_mat_data")
	os.makedirs(dst_dir,exist_ok=True)
	print("Extracting files from",base_dir)
	base_folder = extract_zipfolder(base_dir,dst_dir)
	
	for folder in os.listdir(base_folder):
		folderpath = os.path.join(base_folder,folder)
		if folderpath.endswith('.zip'):
			folder_name= os.path.splitext(os.path.basename(folderpath))[0]
			new_path =  os.path.join(base_folder,folder_name)
			os.makedirs(new_path,exist_ok =True)
			subbase_folder = extract_zipfolder(folderpath,new_path)
			for file in os.listdir(subbase_folder):
				if file.endswith(".mat"):
					num = os.path.splitext(file)[0]
					filepath = os.path.join(subbase_folder,file)
					ns_image, label = classifier.get_image_from_mat(filepath)
					make_tumor_folder(label,dst_dir,num,extension,ns_image)

	print("Data has been saved in this directory",os.path.join(os.path.dirname(dst_dir),"brain_tumor_data"))

def main():
	args = parser.parse_args()
	print("Converting all the .mat file in the given",f"zip folder path: {args.base_dir}\n",sep='\n')
	convert_tumor_matdata_to_jpg(args.base_dir,args.extension)

if __name__ == '__main__':
	sys.exit(main())