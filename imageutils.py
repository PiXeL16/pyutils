import requests
import io
import logging
from PIL import Image
import exif
import ioutils

def search_images_in_google_with_text(search_text, ip_address):
	'''
	Requires Request library
	Search images in google using google image rest services
	Returns a json array of images with example data
	"GsearchResultClass": "GimageSearch",
    "width": "640",
    "height": "427",
    "imageId": "ANd9GcTayODzvMnyAePNkIK5daFXxge6c3dhPP_UR1EdNknINDbH87K2Zb4w2bCS",
    "tbWidth": "137",
    "tbHeight": "91",
    "unescapedUrl": "https://c1.staticflickr.com/5/4133/5053211341_e2986d1392_z.jpg",
    "url": "https://c1.staticflickr.com/5/4133/5053211341_e2986d1392_z.jpg",
    "visibleUrl": "www.flickr.com",
    "title": "Tired <b>Tuco the Bulldog</b> | Flickr - Photo Sharing!",
    "titleNoFormatting": "Tired Tuco the Bulldog | Flickr - Photo Sharing!",
    "originalContextUrl": "https://www.flickr.com/photos/pixel1616/5053211341/",
    "content": "Tired <b>Tuco the Bulldog</b>",
    "contentNoFormatting": "Tired Tuco the Bulldog",
    "tbUrl": "http://t1.gstatic.com/images?q=tbn:ANd9GcTayODzvMnyAePNkIK5daFXxge6c3dhPP_UR1EdNknINDbH87K2Zb4w2bCS"
	'''

	url = 'https://ajax.googleapis.com/ajax/services/search/images'
	params = {'v': '1.0','imgsz':'xxlarge|xlarge|large','userip': ip_address,'q':search_text}

	json_response = requests.get(url, params=params).json();
	
	json_images = list(json_response['responseData']['results'])

	return json_images


def get_image_from_url(image_url):
	'''
	Return a Pillow image object from the imageUrl
	'''
	image = None

	try:
		request_image = requests.get(image_url)
		image_file = io.BytesIO(request_image.content)
		image = Image.open(image_file)
		
	except IOError as ex:
		logging.error("Error cannot get image from url "+ image_url)
		
	
	return image

def create_thumbnail(image, thumbnail_size=(250,250)):

	image.thumbnail(thumbnail_size,Image.ANTIALIAS)
	return image

def resize_down_image(image, size):
	"""
	resize the image down to a specific size if its larger
	"""
	current_size = image.size;
	if current_size > size:
		create_thumbnail(image,size)

	return image

def save_image(image,image_name, folder_name):
	"""
	save the image with that name to a specific folder
	returns the saved image name with its extension
	"""
	image_saved_name = None
	ioutils.check_or_create_folder(folder_name)
	try:
		save_name = '%s.jpg'%(image_name)
		path ='%s/%s'%(folder_name,save_name)
		image.save(path, "JPEG")
		return save_name
	except IOError as ex:
		logging.error("Error cannot save image %s"% image)
		ioutils.delete_file(path)
		

def save_image_and_resize_down(image, size, image_name, folder_name):
	"""
	save the image with that name to a specific folder and resize it down if needed
	"""
	try:
		resized_image = resize_down_image(image, size)
		image_saved_name = save_image(resized_image, image_name, folder_name)
		return image_saved_name
	except IOError as ex:
		logging.error("Error cannot save image for %s"% image)
		
	
def save_image_thumbnail(image,thumbnail_size,image_name,folder_name):
	'''
	creates a thumbnail for the image with the name and in the folder path
	'''
	try:
		image_thumbnail = create_thumbnail(image,thumbnail_size)
		image_saved_name = save_image(image_thumbnail,image_name,folder_name)
		return image_saved_name
	except IOError as ex:
		logging.error("Error cannot create thumbnail for %s"% image)
		

def get_exif_field_from_image(image, exif_field):
	"""
	Gets the exif field from an image
	"""
	exif_values = exif.getexif(image)
	k = list(exif_values.keys())
	if exif_field in exif_values:
		return exif_values[exif_field]