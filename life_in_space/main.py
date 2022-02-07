'''
This project contains all the code for our Mission Space Lab (Life in Space) experiment.
We'd like to explore our hypothesis concerning the magnetic field of the Earth:
"If the ISS is on the day side of the Earth, the magnetic field will be slightly stronger."

In addition, we want to observe other effects of the sun. We'll collect data about temperature, 
humidity, etc. to determine whether these fluctuate due to the sun(light).

Team: Hyperion
Author: JVS Hyperion (Youth association for Astronomy)
Version: 0.1
'''

# Import statements
import csv
from datetime import date, datetime, timedelta
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

# Set up Sense Hat
SENSE = SenseHat()

# Set up the correct ephemeris
EPHEMERIS = load('de421.bsp')

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
    if ISS.at(load.timescale.now()).is_sunlit(EPHEMERIS):
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
    return round(SENSE.get_temperature(), 4) + "°C"

def get_humidity():
    '''This function returns (string) the current humidity.'''
    return round(SENSE.get_humidity(), 4) + "%"

def get_luminosity():
    '''This function returns (string) the current luminosity.'''
    return round((SENSE.clear() / 256) * 100, 3) + "%"

SENSE.colour.integration_cycles = 64
SENSE.colour.gain = 60

# Create CSV file
create_csv(DATA_FILE, ("Date/Time", "Location", "Sunlight", "Magnetic field strength", "Temperature", "Humidity", "Luminosity"))

# Record the current time
current_time = datetime.now()

# Experiment Loop
while current_time < START_TIME + timedelta(minutes=5):

    current_time = datetime.now()

# End / Clear Phase
