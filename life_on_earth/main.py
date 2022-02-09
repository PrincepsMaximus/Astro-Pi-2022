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

from PIL import Image
from pycoral.adapters import common
from pycoral.adapters import classify
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.dataset import read_label_file

# Record the start time and initiate counter
START_TIME = datetime.now()
counter = 1

# Working directory for data recording
BASE_FOLDER = Path(__file__).parent.resolve()
DATA_FILE = BASE_FOLDER/'data.csv'

# Set up Pi Camera
CAMERA = PiCamera()
CAMERA.resolution(4056, 3040) # Approx. 6 MB / pic or 170 pics / GB

# Set up ML (PyCoral)
MODEL_FILE = BASE_FOLDER/'astropi-cloud-model.tflite'
LABEL_FILE = BASE_FOLDER/'labels.txt'
INTERPRETER = make_interpreter(f"{MODEL_FILE}")
INTERPRETER.allocate_tensors()

SIZE = common.input_size(INTERPRETER)
LABELS = read_label_file(LABEL_FILE)

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

# Camera functions
def convert(angle):
    '''
    Convert a `skyfield` Angle to an EXIF-appropriate
    representation (rationals)
    e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    Return a tuple containing a boolean and the converted angle,
    with the boolean indicating if the angle is negative.
    (Source: Astro Pi Phase 2 Guide)
    '''
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'

    return sign < 0, exif_angle

def capture(camera, image):
    '''
    This function will capture an image, add all required EXIF-data and save it as JPEG.

    Parameters:
    camera (PiCamera): The camera object to take the image.
    image (String): The filename for saving.
    (Source: Astro Pi Phase 2 Guide)
    '''
    coordinates = ISS.coordinates()

    # Convert the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = convert(coordinates.latitude)
    west, exif_longitude = convert(coordinates.longitude)

    # Set the EXIF tags specifying the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    # Capture the image
    camera.capture(image)

# Create CSV file
create_csv(DATA_FILE, ("No.", "Time", "Predicted cloud type", "Certainty"))

# Record the current time
current_time = datetime.now()

# Experiment Loop
while current_time < START_TIME + timedelta(minutes=175):
    # Start variables
    predicted_cloud = ""
    certainty = ""

    # Capture an image
    image_file = f"{BASE_FOLDER}/image_{counter:03d}.jpg"
    capture(CAMERA, image_file)

    # Predict cloud type
    image = Image.open(image_file).convert('RGB').resize(SIZE, Image.ANTIALIAS)
    common.set_input(INTERPRETER, image)

    INTERPRETER.invoke()
    classes = classify.get_classes(INTERPRETER, top_k=1)
    for c in classes:
        predicted_cloud = f"{LABELS.get(c.id, c.id)}"  
        certainty = f"{c.score:.5f}"

    # Data management
    data = (
        counter,
        datetime.now(),
        predicted_cloud,
        certainty,
    )
    add_csv_data(DATA_FILE, data)

    # Time management
    sleep(240)

    # Increment counter variable and update stop condition
    counter += 1
    current_time = datetime.now()

# End