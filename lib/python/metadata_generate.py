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
REGIONS_VESSELS = os.getenv("REGIONS_VESSELS")
OUTPUT_DIRECTORY = os.getenv("OUTPUT_DIRECTORY")
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

def check_input_filenames(input_filenames: list):
    """from the cli arguments create a list of which files require inclusion in the YAML metadata file.
    then make sure all the files exist"""
    list_of_filenames_that_actually_exist = []

    for a_filename in input_filenames:
        if not os.path.isfile(a_filename):
            logger.warning("Filename %s is not a file (or doesn't exist): Ignoring", a_filename)
        else:
            list_of_filenames_that_actually_exist.append(os.path.abspath(a_filename))
            logger.info("Including filename: %s", a_filename)

    return list_of_filenames_that_actually_exist

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


def lat_long_geojson(filename, blank_latlong):
    "Determine Lat/Long boundaries from a geojson file."
    latlong = blank_latlong
    latlong['latmin']  = latlong['lonmin'] = 180.0
    latlong['latmax']  = latlong['lonmax'] = -180.0

    with open(filename, 'r') as f:
        file_contents = f.read()
        parsed_json = json.loads(file_contents)
    
    try:
        spatial = parsed_json['features']
        for a_feature in spatial:
            sub = a_feature['geometry']['coordinates']
            for a_sub in sub:

                # Account for format differences
                if len(a_sub) > 2:
                    coords = a_sub[0]
                else:
                    coords = a_sub

                try:
                    if float(coords[0]) > latlong['lonmax']:
                        latlong['lonmax'] = float(coords[0])
                    if float(coords[0]) < latlong['lonmin']:
                        latlong['lonmin'] = float(coords[0])
                    if float(coords[1]) > latlong['latmax']:
                        latlong['latmax'] = float(coords[1])
                    if float(coords[1]) < latlong['latmin']:
                        latlong['latmin'] = float(coords[1])

                except Exception as e:
                    logger.error("Value(s) missing for Lat/Long: %s", e)

    except Exception as e:
        logger.info("No Lat/Long boundaries found in %s", filename)
        latlong = blank_latlong
    
    return latlong


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
    this needs to handle csv, json(mesh and route), geojson(mesh and route) which have been zipped with gz"""
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
    if new_filename.endswith('.geojson'):
        lat_long = lat_long_geojson(new_filename, blank_latlong)

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


def generate_output(filenames, parameters, is_echoed, valid_date, outfilename):
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

    if is_echoed:
        # only output to shell
        print(yaml.dump(yaml_content, sort_keys=False, width=4000, indent=4))
    else:
        outfile = OUTPUT_DIRECTORY + outfilename
        logger.info("Creating file: %s", str(outfile))
        try:
            with open(outfile, "w") as f:
                yaml.dump(yaml_content, f, sort_keys=False, width=4000, indent=4)
            logger.info("Metadata file created")
        except Exception as e:
            logger.error("Unable to create metadata file due to %s", str(e))


def read_input_list_to_file(file_name: str):
    """
    Just open an input list file,
    and return the contents as a list-of-lines.
    """
    lines = []
    with open(file_name) as f:
        for line in f:
            lines.append(line.strip())
    return lines


def get_args():
    """
    Argument parsing
    """
    parser = argparse.ArgumentParser(description='Create metadata file for specified file(s)')
    parser.add_argument("-t", help="Text file containing the fullpaths to "
                        "files we want metadata for, each on its own line",
                        action="store", dest="target_file_list", default=None)
    parser.add_argument("-d", help="Include file created date and time",
                        action="store_true", dest='created', default=False)
    parser.add_argument("-s", help="Include file size", action="store_true",
                        dest='size', default=False)
    parser.add_argument("-m", help="Include file md5sum", action="store_true",
                        dest='md5', default=False)
    parser.add_argument("-i", help="Include file meshiphi version", action="store_true",
                        dest='meshiphi', default=False)
    parser.add_argument("-l", help="Include lat/long boundaries", action="store_true",
                        dest='latlong', default=False)
    parser.add_argument("-e", help="Echo the metadata to shell rather than saving to file",
                        action="store_true", dest='echo_shell', default=False)
    parser.add_argument("--outfile", help="Override default and specify output filename",
                        action="store", dest='outfile', default="upload_metadata.yaml")
    parser.add_argument("--valid_date", help="Supply, for inclusion datetime (string) for " \
                        "which the data is valid.", action="store", dest='valid')
    return parser.parse_args()


def main(target_file_list, created, size, md5, meshiphi, latlong, echo_shell,
         outfile, files, **kwargs):
    """
    Metadata creation entry point
    """
    valid_date = kwargs.get("valid_date", None)

    if echo_shell:
        # If the purpose is to send the yaml to the shell then dont
        # pollute the shell with logger information
        logger.disabled = True
        logger.info("Echo to shell is enabled, no file will be created")
    
    if valid_date:
        logger.info("Supplied valid date is %s", valid_date)
    else:
        # use null instead of None for the YAML
        valid_date = 'null'

    target_file_list = read_input_list_to_file(target_file_list)
    checked_files = check_input_filenames(target_file_list)
    parameter_list = make_parameter_list(
        {
            "created": created,
            "size": size,
            "md5": md5,
            "meshiphi": meshiphi,
            "latlong": latlong
        }, valid_date)
    generate_output(checked_files, parameter_list, echo_shell, valid_date,
                    outfile)  


if __name__ == "__main__":
    """
    If the script is being called with command line arguments, rather than
    via cylc, use argparse to get the contents.
    """
    args = get_args()
    # note that args.files are passed before args.output and args.valid_date
    # because it's a bit of a mess with optionals/mandatories/infinite lists
    # down here
    main(args.created, args.size, args.md5, args.meshiphi, args.latlong,
         args.echo_shell, args.target_file_list, args.outfile, args.valid_date)