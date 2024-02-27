class GPSHandler:
    @staticmethod
    def extract_gps_data(exif_data):
        gps_data = {}
        try:
            if exif_data:
                for tag, the_value in exif_data.items():
                    tag_value = TAGS.get(tag, tag)
                    if tag_value == "GPSInfo":
                        for cur_tag in the_value:
                            gps_tag = GPSTAGS.get(cur_tag, cur_tag)
                            gps_data[gps_tag] = the_value[cur_tag]
        except Exception as e:
            raise RuntimeError("Error extracting GPS data:", e)
        return gps_data

    @staticmethod
    def extract_lat_lon(gps_data):
        latitude, latitude_ref, longitude, longitude_ref = None, None, None, None
        try:
            latitude = gps_data.get("GPSLatitude")
            latitude_ref = gps_data.get("GPSLatitudeRef")
            longitude = gps_data.get("GPSLongitude")
            longitude_ref = gps_data.get("GPSLongitudeRef")
        except Exception as e:
            raise RuntimeError("Error extracting latitude and longitude:", e)
        return latitude, latitude_ref, longitude, longitude_ref

    @staticmethod
    def convert_coordinate(coord):
        try:
            if isinstance(coord, tuple):
                degrees, minutes, seconds = coord
                coord = degrees + minutes / 60.0 + seconds / 3600.0
        except Exception as e:
            raise RuntimeError("Error converting coordinate:", e)
        return str(coord)
