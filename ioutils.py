import os
import io

def check_or_create_folder(folder_name):
	"""
	Check if folder exists and if not creates it
	"""
	#Create folder
	if not os.path.exists(folder_name):
   		 os.makedirs(folder_name)


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))
    return value
