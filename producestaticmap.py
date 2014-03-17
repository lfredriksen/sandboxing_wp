from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

#comment to see if something happens

def convert_to_float(crazy_gps):
	#in order to convert GPS data in meta data to float numbers
	#each appears to represent a fraction, both degrees and minutes
	#appear to all by a number divided by 1 seconds appear to be divided by 1000
	#include division anyway in case we encounter something else
	
	#first number cluster is whole number degrees
	deg_to_number = float(crazy_gps[0][0])/float(crazy_gps[0][1])
	
	#second number cluster is in minutes, which are 1/60th of whole degrees
	min_to_number = (float(crazy_gps[1][0])/float(crazy_gps[1][1]))/60.0
	
	#third number cluster is in seconds, which are 1/3600th of whole degrees
	sec_to_number = (float(crazy_gps[2][0])/float(crazy_gps[2][1]))/3600.0
	
	float_gps = deg_to_number + min_to_number + sec_to_number
	return float_gps
	
def get_field(exif, field):
	#function allows for calling exif data by field name
	for (k, v) in exif.iteritems():
		if TAGS.get(k) == field:
			return v
			
def get_field_gps(exif, field):
	#function allows for calling exif gps data by field name
	for (k, v) in exif.iteritems():
		if GPSTAGS.get(k) == field:
			return v

def get_meta_data(filename):
	#given a filename, gets gps coords and time created
	#also converts lat, long to float numbers
	file = Image.open(filename)
	time_created = get_field(file._getexif(), 'DateTimeOriginal') 
	coords = get_field(file._getexif(), 'GPSInfo')
	lat_basic = get_field_gps(coords, "GPSLatitude")
	long_basic = get_field_gps(coords, "GPSLongitude")
	latitude = convert_to_float(lat_basic)
	longitude = convert_to_float(long_basic)
	return [time_created, latitude, longitude]
	
def make_map_hyper(lat, long, API_key):
	#takes lat and long coord and outputs a googlemaps static map hyperlink
	#if no API key exists, enter string value '0'.
	#lat and long should also be strings, but there is backup conversion in case
	front_end = 'http://maps.googleapis.com/maps/api/staticmap?markers='
	if API_key == '0':
		#check if API key was put in, if null then return empty string
		key_key = ''
	else:
		#generate string for API key existing
		key_key = '&key={' + str(API_key) + '}'
	hyper_link = front_end + str(lat) + "," + str(long) +  key_key
	# put it together
	return hyper_link

#here be the testing graveyard		
meta_data = get_meta_data('IMG_0554.JPG')
print make_map_hyper(meta_data[1],meta_data[2],'FAGDS21432532')
