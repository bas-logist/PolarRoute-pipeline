import os
import meshiphi
import csv
import gzip
import json
import logging
import argparse
import hashlib
import yaml
from datetime import datetime

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get relevant environment variables from parent pipeline process
DESCRIPTION = "Metadata file used for data transfer of files in Operational PolarRoute project"


VERSION = os.getenv("METADATA_VERSION")
TARGET_FILE = os.getenv("TARGET_FILE_FULLPATH")
OUTPUT_DIRECTORY = os.getenv("OUTPUT_DIRECTORY")
OUTPUT_FILENAME = os.getenv("OUTPUT_FILENAME")
# this will be string not bool
ECHO_SHELL = os.getenv("ECHO_SHELL").upper()

USER = os.getenv("CYLC_WORKFLOW_OWNER")
MESHIPHI_VERSION = meshiphi.__version__


def md5(filename):
    """
    create md5sum checksum for any file
    """
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_meshiphi_version(filename):
    """
    Get meshiphi version from file. At present the
    version isn't in the file so we just use the
    environment's meshiphi version.
    """
    return MESHIPHI_VERSION


def make_parameter_list(arguments: dict, valid_date):
    "from the cli options create a list of which metadata variables to generate."
    list_of_parameters = ["filepath", ]

    if valid_date != 'null':
        list_of_parameters.append("valid_date")
    
    for argument_key, argument_value in arguments.items():
        if argument_value == True:
            list_of_parameters.append(argument_key)
    
    logger.info("Including metadata parameters: %s", ' '.join(list_of_parameters))

    return list_of_parameters


def lat_long_json(filename, blank_latlong):
    "Determine Lat/Long boundaries from a json file."
    latlong = blank_latlong
    with open(filename, 'r') as f:
        file_contents = f.read()
        parsed_json = json.loads(file_contents)
    
    try:
        spatial = parsed_json['config']['mesh_info']['region']
        latlong['latmax'] = float(spatial['lat_max'])
        latlong['latmin'] = float(spatial['lat_min'])
        latlong['lonmax'] = float(spatial['long_max'])
        latlong['lonmin'] = float(spatial['long_min'])

    except Exception as e:
        logger.error("Value(s) missing for Lat/Long: %s", e)

    return latlong


def lat_long_csv(filename, blank_latlong):
    "Determine Lat/Long boundaries from a csv file."
    latlong = blank_latlong
    latlong['latmin']  = latlong['lonmin'] = 180.0
    latlong['latmax']  = latlong['lonmax'] = -180.0
    with open(filename, 'r') as f:
        csvreader = csv.DictReader(f, delimiter=',')

        if 'Lat' in csvreader.fieldnames and 'Long' in csvreader.fieldnames:
            for row in csvreader:
                try:
                    if float(row['Lat']) > latlong['latmax']:
                        latlong['latmax'] = float(row['Lat'])
                    if float(row['Lat']) < latlong['latmin']:
                        latlong['latmin'] = float(row['Lat'])
                    if float(row['Long']) > latlong['lonmax']:
                        latlong['lonmax'] = float(row['Long'])
                    if float(row['Long']) < latlong['lonmin']:
                        latlong['lonmin'] = float(row['Long'])

                except Exception as e:
                    logger.error("Value(s) missing for Lat/Long: %s", e)
        else:
            logger.info("No Lat/Long boundaries found in %s", filename)
            latlong = blank_latlong
    
    return latlong

def get_lat_long(filename):
    """decompress and open the file then find out if it has lat, long boundaries,
    this needs to handle csv and json(mesh and route) which have been zipped with gz"""
    blank_latlong = {'latmin': 'null',
                     'latmax': 'null',
                     'lonmin': 'null',
                     'lonmax': 'null'}
    lat_long = blank_latlong
    file_unzipped = False

    if filename.endswith('.gz'):
        outfile = filename.strip('.gz') 
        with open(filename, 'rb') as inf, open(outfile, 'w', encoding='utf8') as tof:
            decom_str = gzip.decompress(inf.read()).decode('utf-8')
            tof.write(decom_str)
        file_unzipped = True

    if file_unzipped:
        new_filename = outfile
    else:
        new_filename = filename

    if new_filename.endswith('.csv'):
        lat_long = lat_long_csv(new_filename, blank_latlong)
    if new_filename.endswith('.json'):
        lat_long = lat_long_json(new_filename, blank_latlong)

    if file_unzipped:
        os.remove(filename.strip('.gz'))

    return lat_long

def build_records(filenames, parameters, valid_date):
    "iterate over files and build record entries in dictionary format"
    blank_params = [ (param, 'null') for param in parameters ]
    record_content = []

    for a_file in filenames:
        param_dict = dict(blank_params)

        for a_param in parameters:
            if a_param == 'filepath':
                param_dict[a_param] = a_file
            
            elif a_param == 'valid':
                if valid_date == 'null':
                    param_dict[a_param] = datetime.strftime \
                        (datetime.fromtimestamp \
                        (os.path.getctime(a_file)), "%Y%m%dT%H%M%S")
                else:
                    param_dict[a_param] = valid_date

            elif a_param == 'created':
                param_dict[a_param] = datetime.strftime \
                    (datetime.fromtimestamp \
                     (os.path.getctime(a_file)), "%Y%m%dT%H%M%S")
            
            elif a_param == 'size':
                param_dict[a_param] = os.path.getsize(a_file)
            
            elif a_param == 'md5':
                param_dict[a_param] = md5(a_file)
            
            elif a_param == 'meshiphi':
                param_dict[a_param] = get_meshiphi_version(a_file)
            
            elif a_param == 'latlong':
                param_dict[a_param] = get_lat_long(a_file)

        record_content.append(param_dict)
    return record_content


def generate_output(filenames: list, parameters: tuple, is_echoed: str, valid_date: str,
                    output_directory: str, outfilename: str):
    "for each file in the list generate the metadata and write to outfile or shell"
    logger.info("Generating metadata output")

    # create the file contents as a single yaml construct
    created = datetime.strftime(datetime.now(), "%Y%m%dT%H%M%S")
    records = build_records(filenames, parameters, valid_date)
    yaml_content = {'info': {'description': DESCRIPTION,
                               'version': VERSION,
                               'created': created,
                               'user': USER},
                    'filepaths': filenames,
                    'parameters': parameters,
                    'records': records
                   }
    
    #print(yaml.dump(yaml_content, sort_keys=False, width=4000))

    if is_echoed == "TRUE":
        # only output to shell
        print(yaml.dump(yaml_content, sort_keys=False, width=4000, indent=4))
    else:
        outfile = output_directory + "/" + outfilename
        logger.info("Creating file: %s", str(outfile))
        try:
            with open(outfile, "w") as f:
                yaml.dump(yaml_content, f, sort_keys=False, width=4000, indent=4)
            logger.info("Metadata file created")
        except Exception as e:
            logger.error("Unable to create metadata file due to %s", str(e))


def read_input_list_to_file(file_name: str):
    """
    Read an input list file, and return the contents as a list-of-filepaths.
    """
    lines = []
    with open(file_name) as f:
        for line in f:
            lines.append(line.strip())
    return lines

def main():
    """
    Metadata creation entry point
    """
    # set the valid_date to the current date for now
    valid_date = datetime.strftime(datetime.now(), "%Y%m%dT%H%M%S")

    if ECHO_SHELL == "TRUE":
        # If the purpose is to send the yaml to the shell then dont
        # pollute the shell with logger information
        logger.disabled = True
        logger.info("Echo to shell is enabled, no file will be created")
    
    if valid_date:
        logger.info("Supplied valid date is %s", valid_date)
    else:
        # use null instead of None for the YAML
        valid_date = 'null'

    target_file_list = read_input_list_to_file(TARGET_FILE)
    parameter_list = make_parameter_list(
        {
            "created": True,
            "size": True,
            "md5": md5,
            "meshiphi": meshiphi,
            "latlong": True
        }, valid_date)
    generate_output(target_file_list, parameter_list, ECHO_SHELL, valid_date,
                    OUTPUT_DIRECTORY, OUTPUT_FILENAME)
