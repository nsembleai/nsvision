# TODO: review s3scripts
# # imports
# import os
# import random
# import time
# import threading
# from datetime import datetime
# from botocore.exceptions import ClientError
# import sys

# try:
#     import boto3
# except ImportError:
#     raise ImportError("Required boto3 library for installation")


# class ProgressPercentage(object):
#     def __init__(self, filename):
#         self._filename = filename
#         self._size = float(os.path.getsize(filename))
#         self._seen_so_far = 0
#         self._lock = threading.Lock()

#     def __call__(self, bytes_amount):
#         # To simplify, assume this is hooked up to a single filename
#         with self._lock:
#             self._seen_so_far += bytes_amount
#             percentage = (self._seen_so_far / self._size) * 100
#             sys.stdout.write(
#                 "\r%s  %s / %s  (%.2f%%)"
#                 % (self._filename, self._seen_so_far, self._size, percentage)
#             )
#             sys.stdout.flush()


# class S3Bucket:
#     def __init__(self, s3_resource):
#         self.s3_resource = s3_resource

#     def download_s3_data(self, bucket_name, prefix, no_samples, dest_path):
#         """This function download files from s3 bucket from the given s3 path
#         and save it in the given dest path
#         Args:
#         s3_resource - Connection to s3 bucket
#         bucket_name - Name of the bucket (str)
#         prefix - Subdir from where files to be downloaded (str)
#         no_samples - Number of files o be download (int)
#         dest_path - Destination path where files downloaded
#                     will be save with the same name as in bucket (str)
#         """
#         my_bucket = self.s3_resource.Bucket(bucket_name)
#         objects = my_bucket.objects.filter(Prefix=f"{prefix}/")
#         file_list = [obj.key for obj in objects]
#         if file_list == []:
#             raise Exception("Incorrect prefix path")
#         samples = random.sample(file_list, int(no_samples))
#         print("Downloading Started...")
#         for i in range(len(samples)):
#             dest_path = f"/{dest_path}"
#             os.makedirs(dest_path, exist_ok=True)
#             start_time = datetime.now()
#             my_bucket.download_file(
#                 samples[i], os.path.join(dest_path, os.path.split(samples[i])[1])
#             )
#             elapsedTime = datetime.now() - start_time
#             total_time = divmod(elapsedTime.total_seconds(), 60)
#         print(
#             f"Total time taken to download all files is {total_time[0]} minutes and {total_time[1]} seconds"
#         )

#     def upload_file(self, file_name, bucket, object_name=None):
#         """Upload a file to an S3 bucket

#         :param file_name: File to upload
#         :param bucket: Bucket to upload to
#         :param object_name: S3 object name. If not specified then file_name is used
#         :return: True if file was uploaded, else False
#         """

#         # If S3 object_name was not specified, use file_name
#         if object_name is None:
#             object_name = file_name

#         # Upload the file
#         s3_client = boto3.client("s3")
#         try:
#             s3_client.upload_file(file_name, bucket, object_name)
#         except ClientError:
#             return False
#         return True

#     def split_s3_path(self, s3_path):
#         """This function splitt s3 path into bucket name and remain part"""
#         path_parts = s3_path.replace("s3://", "").split("/")
#         bucket = path_parts.pop(0)
#         key = "/".join(path_parts)
#         return bucket, key

#     def upload_data_to_s3(self, data_dir, s3_path):
#         imagePaths = [
#             path
#             for path in list(s3_path.list_images(data_dir))
#             if not path.endswith(".txt")
#         ]
#         ts = time.time()
#         for img in imagePaths:
#             img_lst = img.split("/")
#             img_lst.remove("")
#             file_path = "/".join(img_lst[-3:])
#             new_s3_path = os.path.join(s3_path, file_path)
#             bucket, key = self.split_s3_path(new_s3_path)
#             self.upload_file(img, bucket, key, Callback=ProgressPercentage(img))
