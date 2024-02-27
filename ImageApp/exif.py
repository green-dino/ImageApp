import pickle
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


class ExifProcessor:
    @staticmethod
    def extract_gps_dictionary(file_name, pickle_file):
        try:
            pil_image = Image.open(file_name)
            exif_data = pil_image._getexif()
        except Exception:
            return None, None

        gps_data, gps_dictionary = ExifProcessor._extract_gps_info(exif_data)
        basic_exif_data = ExifProcessor._extract_basic_exif_info(exif_data)

        if gps_data:
            with open(pickle_file, 'wb') as f:
                pickle.dump(gps_dictionary, f)

        return gps_dictionary if gps_data else None, basic_exif_data

    @staticmethod
    def _extract_gps_info(exif_data):
        if not exif_data:
            return False, {}

        gps_data = False
        gps_dictionary = {}
        for tag, the_value in exif_data.items():
            tag_value = TAGS.get(tag, tag)
            if tag_value == "GPSInfo":
                gps_data = True
                for cur_tag in the_value:
                    gps_tag = GPSTAGS.get(cur_tag, cur_tag)
                    gps_dictionary[gps_tag] = the_value[cur_tag]
        return gps_data, gps_dictionary

    @staticmethod
    def _extract_basic_exif_info(exif_data):
        image_time_stamp = "NA"
        camera_make = "NA"
        camera_model = "NA"
        if exif_data:
            for tag, the_value in exif_data.items():
                tag_value = TAGS.get(tag, tag)
                if tag_value == 'DateTimeOriginal':
                    image_time_stamp = exif_data.get(tag).strip()
                if tag_value == "Make":
                    camera_make = exif_data.get(tag).strip()
                if tag_value == 'Model':
                    camera_model = exif_data.get(tag).strip()
        return [image_time_stamp, camera_make, camera_model]
