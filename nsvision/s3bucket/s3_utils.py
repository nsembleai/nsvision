#imports
import os
import random
import datetime
import argparse
import boto3


class S3Bucket:
	def __init__(self,s3_resource):
		self.s3_resource = s3_resource

	def download_s3_data(self,bucket_name,prefix,no_samples,dest_path):
		"""This function download files from s3 bucket from the given s3 path 
		and save it in the given dest path
		Args:
		s3_resource - Connection to s3 bucket
		bucket_name - Name of the bucket (str)
		prefix - Subdir from where files to be downloaded (str)
		no_samples - Number of files o be download (int) 
		dest_path - Destination path where files downloaded 
					will be save with the same name as in bucket (str)
		"""
		my_bucket = self.s3_resource.Bucket(bucket_name)
		objects = my_bucket.objects.filter(Prefix=f'{prefix}/')
		file_list = [obj.key for obj in objects]
		if file_list == []:
			raise Exception ("Incorrect prefix path")
		samples = random.sample(file_list,int(no_samples))
		print("Downloading Started...")
		for i,j in enumerate(samples):
			dest_path = f'/{dest_path}'
			os.makedirs(dest_path,exist_ok=True)
			start_time = datetime.datetime.now()
			my_bucket.download_file(samples[i], os.path.join(dest_path,os.path.split(samples[i])[1]))
			elapsedTime = datetime.datetime.now() - start_time
			total_time = divmod(elapsedTime.total_seconds(), 60)
		print(f'Total time taken to download all files is {total_time[0]} minutes and {total_time[1]} seconds')