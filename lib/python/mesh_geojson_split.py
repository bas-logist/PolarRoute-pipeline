import os
import sys
import json
import logging
import argparse

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_NAME_NORTH = "north"
OUTPUT_NAME_SOUTH = "south"
MAX_LAT = 90.0
MIN_LAT = -90.0
DESCRIPTION = "Split geojson mesh file at a line of constant latitude into a north mesh and south mesh"
VERSION = "0.0.2"


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


def split_geojson(latitude, filename):
    """
    Split file at specified latitude and write out as North and South hemisphere files.
    """
    logger.info("Splitting geojson mesh file(s) at %s degrees latitude", latitude)
    logger.info("Splitting %s", str(filename))

    with open(filename, 'r') as f:
        file_contents = f.read()
        parsed_json = json.loads(file_contents)
    
    north_data = {'type':'FeatureCollection'}
    north_data['features'] = []
    south_data = {'type':'FeatureCollection'}
    south_data['features'] = []

    try:
        spatial = parsed_json['features']

        # for each feature, if all the latitudes are below the specified latitude then
        # append to the south data features. If all features are above or equal to the
        # specified latitude then append to the north data features. If latitudes are above
        # and below the specified latitude then append to the north data features.

        for a_feature in spatial:
            sub = a_feature['geometry']['coordinates']

            halves = []

            for a_sub in sub:

                # Account for format differences
                if len(a_sub) > 2:
                    coords = a_sub[0]
                else:
                    coords = a_sub
                
                try:
                    if float(coords[1]) < latitude:
                        halves.append(OUTPUT_NAME_SOUTH)
                    if float(coords[1]) >= latitude:
                        halves.append(OUTPUT_NAME_NORTH)

                except Exception as e:
                    logger.error("Value(s) missing for Lat/Long: %s", e)
            
            if OUTPUT_NAME_SOUTH in halves and OUTPUT_NAME_NORTH not in halves:
                south_data['features'].append(a_feature)
            if OUTPUT_NAME_NORTH in halves and OUTPUT_NAME_SOUTH not in halves:
                north_data['features'].append(a_feature)
            if OUTPUT_NAME_NORTH in halves and OUTPUT_NAME_SOUTH in halves:
                north_data['features'].append(a_feature)


    except Exception as e:
        logger.info("No Lat/Long boundaries found in %s", filename)

    north_json_data = json.dumps(north_data, indent=4)
    south_json_data = json.dumps(south_data, indent=4)

    outfilename_north = os.path.splitext(filename)[0].replace('_SDA.vessel', OUTPUT_NAME_NORTH + '_SDA.vessel') + os.path.splitext(filename)[1]
    outfilename_south = os.path.splitext(filename)[0].replace('_SDA.vessel', OUTPUT_NAME_SOUTH + '_SDA.vessel') + os.path.splitext(filename)[1]

    with open(outfilename_north, "w") as outfile:
        outfile.write(north_json_data)
    
    with open(outfilename_south, "w") as outfile:
        outfile.write(south_json_data)


def main():
    """Split geojson mesh file at specified constant latitude"""
        
    # Get environment variables provided from flow.cylc
    MOST_RECENT = os.environ.get("MOST_RECENT")
    LATITUDE = float(os.environ.get("LATITUDE"))
    MESH_GEOJSON = os.environ.get("MESH_GEOJSON")


    if LATITUDE < float(MIN_LAT) or LATITUDE > float(MAX_LAT):
        logger.error("Latitude value out of range, %s:%s", str(MIN_LAT), str(MAX_LAT))
        sys.exit(1)

    input_filenames = check_input_filenames(MESH_GEOJSON)
    split_geojson(LATITUDE, input_filenames, MOST_RECENT)


if __name__ == "__main__":
    main()