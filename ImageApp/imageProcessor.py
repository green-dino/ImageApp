import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from prettytable import PrettyTable
import folium
import base64

class ImageSearcher:
    SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

    def __init__(self, directory):
        self.directory = directory

    @staticmethod
    def is_image(file_path):
        try:
            ext = os.path.splitext(file_path)[1].lower()
            return ext in ImageSearcher.SUPPORTED_FORMATS
        except Exception as e:
            print(f"Error checking image: {str(e)}")
            return False

class ImageProcessor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.exif_data = None

    def extract_exif_data(self):
        try:
            pil_image = Image.open(self.file_name)
            self.exif_data = pil_image._getexif()
        except Exception as e:
            print(f"Error extracting EXIF data: {str(e)}")
            self.exif_data = None

    def get_exif_data(self):
        return self.exif_data

class GPSExtractor:
    @staticmethod
    def extract_gps_data(exif_data):
        gps_data = {}
        if exif_data:
            for tag, the_value in exif_data.items():
                tag_value = TAGS.get(tag, tag)
                if tag_value == "GPSInfo":
                    for cur_tag in the_value:
                        gps_tag = GPSTAGS.get(cur_tag, cur_tag)
                        gps_data[gps_tag] = the_value[cur_tag]
        return gps_data

    @staticmethod
    def extract_lat_lon(gps_data):
        latitude = gps_data.get("GPSLatitude")
        latitude_ref = gps_data.get("GPSLatitudeRef")
        longitude = gps_data.get("GPSLongitude")
        longitude_ref = gps_data.get("GPSLongitudeRef")
        # Conversion to degrees here
        return latitude, latitude_ref, longitude, longitude_ref

    @staticmethod
    def convert_coordinate(coord):
        if isinstance(coord, tuple):
            degrees, minutes, seconds = coord
            coord = degrees + minutes / 60.0 + seconds / 3600.0
        return str(coord)

class ImageDataProcessor:
    @staticmethod
    def process_images(directory):
        result_table = PrettyTable(['File-Name', 'Lat', 'Lon', 'TimeStamp', 'Make', 'Model'])
        map_center = None

        for target_file in os.listdir(directory):
            file_path = os.path.join(directory, target_file)
            if ImageSearcher.is_image(file_path):
                image_processor = ImageProcessor(file_path)
                image_processor.extract_exif_data()
                exif_data = image_processor.get_exif_data()
                if exif_data:
                    gps_data = GPSExtractor.extract_gps_data(exif_data)
                    if gps_data:
                        latitude, latitude_ref, longitude, longitude_ref = GPSExtractor.extract_lat_lon(gps_data)
                        if latitude and longitude:
                            try:
                                lat_str = GPSExtractor.convert_coordinate(latitude)
                                lon_str = GPSExtractor.convert_coordinate(longitude)
                                image_time_stamp = exif_data.get(306, "NA")  # Assuming the tag for timestamp is 306
                                camera_make = exif_data.get(271, "NA")       # Assuming the tag for camera make is 271
                                camera_model = exif_data.get(272, "NA")      # Assuming the tag for camera model is 272
                                result_table.add_row([target_file, lat_str, lon_str, image_time_stamp, camera_make, camera_model])

                                if map_center is None:
                                    map_center = [float(latitude), float(longitude)]
                            except ValueError as ve:
                                print(f"Error converting coordinates for {target_file}: {str(ve)}")

        return result_table, map_center

class MarkerPlotter:
    @staticmethod
    def plot_markers(result_table, map_center):
        if map_center is not None:
            map_obj = folium.Map(location=map_center, zoom_start=10)
            # Add markers to map_obj based on result_table

if __name__ == "__main__":
    print("\nExtract EXIF Data from Image Files")
    print("Script Started", str(datetime.now()))
    print()

    directory = input("Enter the directory containing the image files: ")
    result_table, map_center = ImageDataProcessor.process_images(directory)
    print(result_table)
    MarkerPlotter.plot_markers(result_table, map_center)
