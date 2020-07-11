import os
import shutil
# import argparse
# import logging
# import xml.etree.ElementTree as xmlparser

class XMLPipeline:
	def __init__(self,image_dir,xml_dir):
		self.image_dir = image_dir
		self.xml_dir = xml_dir

	def remove_files(self, directory):
		"""This function creates a remove_files foldder in the given directory 
		and return path of new removed_files directory"""
		folder_name = os.path.splitext(os.path.basename(directory))[0]
		new_folder = folder_name + "_removed_files"
		remove_dir = os.path.join(os.path.dirname(directory),new_folder)
		return remove_dir

	def compare_directory(self,directory,remove_dir,lst_1,lst_2,lst_3):
		"""This function moves the files in lst_1 which are not in lst_2 
		and paste the files in given remove_dir """
		try:
			for i,file in enumerate(lst_1):
				if file not in lst_2:
					remove_file = os.path.join(directory,file + lst_3[i])
					print("This file is being removed:",remove_file)
					os.makedirs(remove_dir,exist_ok = True)
					shutil.move(remove_file,remove_dir)
		except Exception as e:
			print(e)


	def check_data(self):
		"""This function cross-check both the given directories
		It removes any image for which xml is not available and vice-cvrsa. 
		All removed images/xmls will be stored in a different folder in the given directory
		"""
		#creating a list of name of all images by removing their extension
		img_name = [os.path.splitext(filename)[0] for filename in os.listdir(self.image_dir)]
		#creating a list of name of all xmls by removing their extension
		xml_name = [os.path.splitext(filename)[0] for filename in os.listdir(self.xml_dir)]
		#saving the extensions o images in a list
		img_ext = [os.path.splitext(filename)[1] for filename in os.listdir(self.image_dir)]
		#saving the extensions of xmls in a list
		xml_ext = [os.path.splitext(filename)[1] for filename in os.listdir(self.xml_dir)]
		# directory where all remove images to be save
		remove_img_dir = self.remove_files(self.image_dir)
		# directory where all remove xml to be save
		remove_xml_dir = self.remove_files(self.xml_dir)

		#if the file from img_name is not in xml_name then remove it from img_name and vice-versa
		self.compare_directory(self.image_dir,remove_img_dir,img_name,xml_name,img_ext)
		self.compare_directory(self.xml_dir,remove_xml_dir,xml_name,img_name,xml_ext)





