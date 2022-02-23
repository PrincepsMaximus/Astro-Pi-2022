'''
This project contains all the code for our Mission Space Lab (Life in Space) experiment.
We'd like to explore our hypothesis concerning the magnetic field of the Earth:
"If the ISS is on the day side of the Earth, the magnetic field will be slightly stronger."

In addition, we want to observe other effects of the sun. We'll collect data about temperature, 
humidity, etc. to determine whether these fluctuate due to the sun(light).

Team: Hyperion
Author: JVS Hyperion (Youth association for Astronomy)
Version: 1.0
'''

# Import statements
import csv
from datetime import date, datetime, timedelta
from logzero import logger, logfile
from pathlib import Path
from orbit import ISS
from sense_hat import SenseHat
from skyfield.api import load
from time import sleep

# Record the start time
START_TIME = datetime.now()

# Working directory for data recording
BASE_FOLDER = Path(__file__).parent.resolve()
DATA_FILE = BASE_FOLDER/'data.csv'
LOGFILE = logfile(BASE_FOLDER/"events.log")

# Set up Sense Hat
SENSE = SenseHat()

# Set up the correct ephemeris
EPHEMERIS = load('de421.bsp')

# Colours (for matrix)
hyperion = [147, 18, 222] # Our 'official' colour
d = [0, 0, 0] # Black (dark)
w = [255, 255, 255] # White
y = [247, 227, 5] # Yellow
b = [10, 172, 242] # Blue
o = [242, 80, 10] # Orange
g = [105, 95, 91] # Grey

# LED matrix presets
smiley = [
    d, d, o, o, o, o, d, d,
    d, o, d, d, d, d, o, d,
    o, d, o, d, d, o, d, o,
    o, d, d, d, d, d, d, o,
    o, d, o, d, d, o, d, o,
    o, d, d, o, o, d, d, o,
    d, o, d, d, d, d, o, d,
    d, d, o, o, o, o, d, d,
]

sun = [
    y, b, b, b, b, b, b, y,
    b, y, b, y, y, b, y, b,
    b, b, y, y, y, y, b, b,
    b, y, y, y, y, y, y, b,
    b, y, y, y, y, y, y, b,
    b, b, y, y, y, y, b, b,
    b, y, b, y, y, b, y, b,
    y, b, b, b, b, b, b, y,    
]

moon = [
    g, g, g, g, g, g, g, g,
    g, g, g, g, w, w, g, g,
    g, g, w, w, g, w, g, g,
    g, w, w, g, g, g, g, g,
    g, w, w, g, g, g, g, g,
    g, g, w, w, g, g, w, g,
    g, g, g, w, w, w, w, g,
    g, g, g, g, g, g, g, g,    
]

presets = [smiley, sun, moon]

# Methods / Functions
def create_csv(data_file, header):
    '''
    This function creates an csv file in the designated dir with the given header.

    Parameters:
    data_file (file): The directory and name of the csv file that needs to be created.
    header (iterable): A tuple with the header string for the csv file.
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

def get_location():
    '''This function returns the (geographic) coordinates of the ISS at the current time.'''
    return ISS.coordinates()

def get_sunlight():
    '''This function returns (string) whether the ISS is currently lit by the sun or not.'''
    status = "In "
    if ISS.at(load.timescale().now()).is_sunlit(EPHEMERIS):
        status += "sunlight"
    else:
        status += "darkness"
    return status

def get_magnetic_field():
    '''This function returns (string) the raw magnetometer data.'''
    raw = SENSE.get_compass_raw()
    return "x: {x}, y: {y}, z: {z}".format(**raw)

def get_temperature():
    '''This function returns (string) the current temperature.'''
    return str(round(SENSE.get_temperature(), 4)) + "°C"

def get_humidity():
    '''This function returns (string) the current humidity.'''
    return str(round(SENSE.get_humidity(), 4)) + "%"

# LED Matrix handler
counter = 0     # Periodic change of display (making sure program isn't freezed)

def update_matrix():
    if counter % 5:
        SENSE.set_pixels(presets[0])
    else:
        if get_sunlight() == "In sunlight":
            SENSE.set_pixels(presets[1])
        else:
            SENSE.set_pixels(presets[2])

# Create CSV file
create_csv(DATA_FILE, ("Date/Time", "Location", "Sunlight", "Magnetic field strength", "Temperature", "Humidity"))

# Record the current time
current_time = datetime.now()

# Welcome message
SENSE.show_message("Greetings from the children at JVS Hyperion.", text_colour=hyperion)

# Experiment Loop
while current_time < START_TIME + timedelta(minutes=175):
    try:
        # Update matrix
        update_matrix()

        # Data management
        data = (
            datetime.now(),
            get_location(),
            get_sunlight(),
            get_magnetic_field(),
            get_temperature(),
            get_humidity(),
        )
        add_csv_data(DATA_FILE, data)

        # Time management
        sleep(15)
        
        # Update condition
        current_time = datetime.now()
        counter += 1

    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e}')

# End
