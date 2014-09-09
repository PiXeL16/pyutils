import os
import io

def check_or_create_folder(folder_name):
	'''
	Check if folder exists and if not creates it
	'''
	#Create folder
	if not os.path.exists(folderName):
   		 os.makedirs(folderName)