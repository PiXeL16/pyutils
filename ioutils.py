import os
import io
import unicodedata
import re

def check_or_create_folder(folder_name):
	"""
	Check if folder exists and if not creates it
	"""
	#Create folder
	if not os.path.exists(folder_name):
   		 os.makedirs(folder_name)

def delete_file(file_path):
	if os.path.exists(file_path):
		os.remove(file_path)

def slugify_text(value):
	"""
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
	if not isinstance(value, unicode):
		value = unicode(value)

	slug=unicodedata.normalize('NFKD', value)
	slug=slug.encode('ascii', 'ignore').lower()
	slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
	slug = re.sub(r'[-]+', '_', slug)

	return slug
