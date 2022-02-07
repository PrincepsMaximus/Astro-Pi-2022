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
from time import sleep

# Constants / Objects
BASE_FOLDER = Path(__file__).parent.resolve()
DATA_FILE = BASE_FOLDER/'data.csv'

# CSV functions (from Astro Pi Phase 2 Guidelines)
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

# Initialisation Phase

# Experiment Loop

# End / Clear Phase