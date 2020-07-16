import os
import shutil
import xml.etree.ElementTree as xmlParser
try:
	from natsort import natsorted
except:
	natsorted = None
from shutil import copy2
import numpy as np
# import argparse
# import logging

img_folder = ['train_images','test_images','qa_images','val_images']
xml_folder = ['train_xml','test_xml','qa_xml','val_xml']


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

	def create_lst_name_ext(self, directory):
		"""This file will return two list - one is of filename and other is file extensions"""
		#creating a list of name of all files by removing their extension
		file_name = [os.path.splitext(filename)[0] for filename in os.listdir(directory)]
		#creating a list of name of all extensions by removing their name
		file_ext = [os.path.splitext(filename)[1] for filename in os.listdir(directory)]
		return file_name,file_ext


	def check_data(self):
		"""This function cross-check both the given directories
		It removes any image for which xml is not available and vice-cvrsa. 
		All removed images/xmls will be stored in a different folder in the given directory
		"""
		#creating a list of name of all images and their extension
		img_name, img_ext = self.create_lst_name_ext(self.image_dir)
		#creating a list of name of all xmls and their extension
		xml_name, xml_ext = self.create_lst_name_ext(self.xml_dir)
		# directory where all remove images to be save
		remove_img_dir = self.remove_files(self.image_dir)
		# directory where all remove xml to be save
		remove_xml_dir = self.remove_files(self.xml_dir)

		#if the file from img_name is not in xml_name then remove it from img_name and vice-versa
		self.compare_directory(self.image_dir,remove_img_dir,img_name,xml_name,img_ext)
		self.compare_directory(self.xml_dir,remove_xml_dir,xml_name,img_name,xml_ext)

	def rename_files(self,name,folder_path,number):
		"""
		Rename the files in the given folder path
		Parameter
		---------
		path - folder path
		name - common name for renaming
		number - number from which renaming is to start
		"""
		if natsorted is None:
			raise ImportError("natsorted is required"
				"Install it using `pip install natsort`")


		folder_name = os.path.splitext(os.path.basename(folder_path))[0]
		new_folder = folder_name + "_renamed"
		dst_path = os.path.join(os.path.dirname(folder_path),new_folder)
		os.makedirs(dst_path,exist_ok = True)
		for i,filename in enumerate(natsorted(os.listdir(folder_path)),number):
			old_path = os.path.join(folder_path,filename)
			try:
				extension = os.path.splitext(os.path.basename(old_path))[1]
				if extension != '':
					new_name = f"{name}_{i}{extension}"
					new_path = os.path.join(dst_path,new_name)
					copy2(old_path,new_path)
			except:
				raise Exception("Failed to rename the files in the given folder please check the folder structure or os permission")
		print("Renaming completed",f"Renamed files are stored at {dst_path}",sep='\n')
		return dst_path

	def rename_in_xml(self,dir_img,dir_xml):
		#creating a list of name of all images and their extension
		img_name, img_ext = self.create_lst_name_ext(dir_img)
		#creating a list of name of all xmls and their extension
		xml_name, xml_ext = self.create_lst_name_ext(dir_xml)

		for i,file in enumerate(img_name):
			if file  in xml_name:
				try:
					xmlDoc = xmlParser.parse(os.path.join(dir_xml,file +'.xml'))
					rootElement = xmlDoc.getroot()
					for element in rootElement.iter('filename'):
						if element.text != file + img_ext[i]:
							element.text = file + img_ext[i] 
					xmlDoc.write(os.path.join(dir_xml, file + '.xml'))
				except:
					raise Exception("Failed to rename in xml")


	def rename_img_xml(self, name, number):
		"""This function will rename images and their corresponding xml, including the filename in xml"""
		self.check_data()
		for img,xml in zip(natsorted(os.listdir(self.image_dir)),natsorted(os.listdir(self.xml_dir))):
			try:
				if os.path.splitext(img)[0] == os.path.splitext(xml)[0]:
					new_img_dir = self.rename_files(name,self.image_dir,number)
					new_xml_dir = self.rename_files(name,self.xml_dir,number)
				else:
					pass
			except:
				raise Exception("Failed to rename both image and XML")
		self.rename_in_xml(new_img_dir,new_xml_dir)
		print("Renaming completed for both image and XML")

	def divide_data(self,total_images, train = 70, test = 5, val = 20, qa = 5):
		"This function divide a interger into fourt parts as 70:20:5:5"
		train_img = round((train/100)*total_images)
		test_img= round((test/100) * total_images)
		val_img = round((val/100) * total_images) 
		qa_img = round((qa/100) * total_images)


		if (train_img + test_img + val_img + qa_img) < total_images:
			diff = total_images - (train_img + test_img + val_img + qa_img)
			train_img = train_img + diff
		elif  (train_img + test_img + val_img + qa_img) > total_images:
			diff = (train_img + test_img + val_img + qa_img) - total_images
			train_img = train_img - diff
		else:
			pass
		return [train_img ,test_img , qa_img, val_img]

	def create_training_data(self):
		random_no_list = self.divide_data(len(os.listdir(self.image_dir)))
		print("Data will be divided in ratio=====",{"train":random_no_list[0], "test":random_no_list[1],
			"qa":random_no_list[2],"val":random_no_list[3]})

		file_list = os.listdir(self.image_dir)
		for i,x in enumerate(zip(img_folder,xml_folder)):
			dst_dir = os.path.split(self.image_dir)[0] + "/" + "training_data" + "/"  + x[0]
			dst_xml = os.path.split(self.xml_dir)[0] + "/" + "training_data" + "/"  + x[1]
	

			if not os.path.exists(dst_dir):
				os.makedirs(dst_dir)

			if not os.path.exists(dst_xml):
				os.makedirs(dst_xml)

	
			random_images = np.random.choice(file_list,int(random_no_list[i]),replace = False)
			for file in list(random_images):
				if not os.path.exists(os.path.join(dst_dir, file)):
					shutil.copy2(os.path.join(self.image_dir, file), os.path.join(dst_dir, file))
					file_list.remove(file)
				else:
					pass


			#list of files without extension from xml dir
			list_dir1 = [os.path.splitext(filename)[0] for filename in os.listdir(self.xml_dir)]
			#list of files without extension from image dir
			list_dir2 = [os.path.splitext(filename)[0] for filename in os.listdir(dst_dir)]

			try:
				for file in list_dir1:
				    if file in list_dir2:
				        move_file = file + ".xml"
				        if not os.path.exists(os.path.join(dst_xml, move_file)):
				            shutil.copy2(os.path.join(self.xml_dir,move_file), os.path.join(dst_xml,move_file))
				        else:
				            pass
				    else:
				        pass
			except:
				raise Exception("Could not split the data")










