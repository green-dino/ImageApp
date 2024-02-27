import os
from datetime import datetime
import streamlit as st
from PIL import Image
from gps import GPSHandler
from exif import ExifProcessor
from imageProcessor import ImageDataProcessor, ImageSearcher, MarkerPlotter

SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.HEIC']

class PhotoGPSExtractor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.exif_data = None

    def extract_exif_data(self):
        try:
            pil_image = Image.open(self.file_name)
            self.exif_data = pil_image._getexif()
        except Exception as e:
            st.error(f"Error extracting EXIF data: {str(e)}")
            self.exif_data = None

    def get_exif_data(self):
        return self.exif_data

def main():
    st.title("Photo GPS Extractor")

    uploaded_file = st.file_uploader("Upload a photo", type=SUPPORTED_FORMATS, accept_multiple_files=False)

    if uploaded_file is not None:
        photo_gps_extractor = PhotoGPSExtractor(uploaded_file)
        photo_gps_extractor.extract_exif_data()
        exif_data = photo_gps_extractor.get_exif_data()

        if exif_data:
            try:
                gps_data = GPSHandler.extract_gps_data(exif_data)
                latitude, latitude_ref, longitude, longitude_ref = GPSHandler.extract_lat_lon(gps_data)

                if latitude and longitude:
                    latitude_str = GPSHandler.convert_coordinate(latitude)
                    longitude_str = GPSHandler.convert_coordinate(longitude)

                    st.write("Latitude:", latitude_str, latitude_ref)
                    st.write("Longitude:", longitude_str, longitude_ref)
                else:
                    st.warning("GPS coordinates not found in EXIF data.")
            except RuntimeError as e:
                st.error(str(e))
        else:
            st.warning("No EXIF data found in the uploaded photo.")

    st.write("\nExtract EXIF Data from Image Files")
    st.write("Script Started", str(datetime.now()))
    st.write()

    directory = st.text_input("Enter the directory containing the image files:")
    if st.button("Process Images"):
        result_table, map_center = ImageDataProcessor.process_images(directory)
        st.write(result_table)
        MarkerPlotter.plot_markers(result_table, map_center)

if __name__ == "__main__":
    main()
