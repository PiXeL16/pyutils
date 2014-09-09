import requests
import io
from PIL import Image
import ioutils

def search_images_in_google_with_text(search_text, ipaddress):
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
	params = {'v': '1.0', 'userip': ipaddress,'q':search_text}

	json_response = requests.get(url, params=params).json();
	
	json_images = list(json_response['responseData']['results'])

	return json_images


def get_image_from_url(image_url):
	'''
	Return a Pillow image objet form the imageUrl
	'''
	image = None

	try:
		request_image = requests.get(image_url)
		image_file = io.BytesIO(request_image.content)
		image = Image.open(image_file)
		
	except IOError as ex:
		logging.error("cannot get image from url"+ image_url)
		logging.exception(ex)
	
	return image

def create_thumbnail(image, thumbnail_size=(250,250)):

	image.thumbnail(thumbnail_size)
	return image

	
def save_image_thumbnail(image,thumbnail_size,image_name,folder_name):
	'''
	creates a thumbnail for the image with the name and in the folder path
	'''
	check_or_create_folder(folder_name)
	
	try:
		image_thumbnail = create_thumbnail(thumbnail_size)
		image_thumbnail.save('%s/%s'%(folder_name,image_name), "JPEG")
	except IOError as ex:
		logging.error("cannot create thumbnail for "+ image)
		logging.exception(ex)
		
