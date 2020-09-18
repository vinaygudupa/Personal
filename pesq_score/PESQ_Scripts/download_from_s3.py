import boto3
import sys

if len(sys.argv) != 4:
    	print("Usage : pyton3 download_from_s3.py  <S3_bucket_Name> <File_to_be_downlaoded_from_s3> <Local_file_name>")
else:
	BUCKET_NAME = str(sys.argv[1])
	BUCKET_FILE_NAME = str(sys.argv[2])
	LOCAL_FILE_NAME = str(sys.argv[3])
	
	try:
		s3 = boto3.client('s3')
		s3.download_file(BUCKET_NAME, BUCKET_FILE_NAME, LOCAL_FILE_NAME)
		print("File download success")
	except Exception as e:
		print("File cannot be downlaoded. Error : " + str(e))
