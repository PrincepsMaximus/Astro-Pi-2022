'''
This project contains all the code for our Mission Space Lab (Life on Earth) experiment.
First of all we want to see if we can (succesfully) detect cloud types autonomosly from space.
That would make the exploration of our hypothesis concerning the cloud coverage of Earth a lot easier:
"There is a notable difference in cloud types and density above the oceans/seas and land."

Team: JVS_HYP
Author: JVS Hyperion (Youth association for Astronomy)
Version: 0.1
'''

# Import statements
import csv
from datetime import date, datetime, timedelta
from pathlib import Path
from skyfield.api import load
from picamera import PiCamera
from orbit import ISS
from time import sleep

# Record the start time
START_TIME = datetime.now()

# Working directory for data recording
BASE_FOLDER = Path(__file__).parent.resolve()
DATA_FILE = BASE_FOLDER/'data.csv'

# Set up Pi Camera
CAMERA = PiCamera()
CAMERA.resolution(4056,3040) # Approx. 6 MB / pic or 170 pics / GB

# CSV functions (from Astro Pi Phase 2 Guide)
def create_csv(data_file, header):
    '''
    This function creates an csv file in the designated dir with the given header.

    Parameters:
    data_file (file): The directory and name of the csv file that needs to be created.
    header (tuple): A tuple with the header string for the csv file.
    '''
    with open(data_file, 'w', buffering=1) as file:
        writer = csv.writer(file)
        writer.writerow(header)

def add_csv_data(data_file, data):
    '''
    This function adds gathered data to the designated data file (csv file).

    Parameters:
    data_file (file): The csv file to which the data should be added.
    data (iterable): The data (tuple) that will be added to the designated file.
    '''
    with open(data_file, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Camera functions (from Astro Pi Phase 2 Guide)
def convert(angle):
    """
    Convert a `skyfield` Angle to an EXIF-appropriate
    representation (rationals)
    e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    Return a tuple containing a boolean and the converted angle,
    with the boolean indicating if the angle is negative.
    """
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'

    return sign < 0, exif_angle

def capture(camera, image):
    """Use `camera` to capture an `image` file with lat/long EXIF data."""
    point = ISS.coordinates()

    # Convert the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = convert(point.latitude)
    west, exif_longitude = convert(point.longitude)

    # Set the EXIF tags specifying the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    # Capture the image
    camera.capture(image)

# Create CSV file
create_csv(DATA_FILE, ("Date/Time", "Filename"))

# Record the current time
current_time = datetime.now()

# Experiment Loop
while current_time < START_TIME + timedelta(minutes=5):

    current_time = datetime.now()

# End / Clear Phase