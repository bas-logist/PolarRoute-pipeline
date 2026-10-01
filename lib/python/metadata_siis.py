import os
import re
import gzip
import json
import logging
import argparse
import hashlib
import shutil
import uuid
import shapely
from shapely import wkb
from datetime import datetime, timezone

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DESCRIPTION = "Generate a siis metadata file for each product uploaded via the siis-data-sync"
VERSION = "0.0.1"

def md5(filename):
    """
    create md5sum checksum for any file
    """
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def check_input_filenames(input_filenames: list):
    """
    from the cli arguments create a list of which files
    require inclusion in the siis metadata file.
    then make sure all the files exist
    """
    list_of_filenames_that_actually_exist = []

    for a_filename in input_filenames:
        if not os.path.isfile(a_filename):
            logger.warning("Filename %s is not a file (or doesn't exist): Ignoring", a_filename)
        else:
            list_of_filenames_that_actually_exist.append(os.path.abspath(a_filename))
            logger.info("Including filename: %s", a_filename)

    return list_of_filenames_that_actually_exist

def lat_long_geojson(filename):
    """
    Determine Lat/Long boundaries from a geojson file.
    """
    latlong = {'latmin': 180.0,
               'latmax': -180.0,
               'lonmin': 180.0,
               'lonmax': -180.0}

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
        latlong = {'latmin': 'null',
                   'latmax': 'null',
                   'lonmin': 'null',
                   'lonmax': 'null'}
    
    return latlong

def generate_output(filenames: list):
    """
    for each file in the list generate a siis metadata file
    """

    for file in filenames:
        zipped = False
        md5_dl = md5(file)
        uuid_v4 = uuid.uuid4()
        output_filepath = os.path.join(os.path.dirname(file), str(uuid_v4)+'.json')
        logger.info("Generating metadata file: %s", output_filepath)
        size_dl = os.path.getsize(file)
        lowres = False
        onrequest = False
        created_time = datetime.fromtimestamp(os.path.getctime(file))
        ts_acq = datetime.strftime(created_time, "%Y-%m-%dT%H:%M:%S.%f")
        ts_prov_granule = datetime.strftime(datetime.now(timezone.utc), "%Y-%m-%dT%H:%M:%S.%f")
        filename_dl = os.path.basename(file) # filename of file to upload

        # if the file is zipped then create an unzipped copy in place
        if os.path.splitext(file)[-1] == '.gz':
            zipped = True
            with gzip.open(file, 'rb') as f_in:
                with open(''.join(os.path.splitext(file)[:-1]), 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            # point to the unzipped file instead of zipped
            file = ''.join(os.path.splitext(file)[:-1])

        # The line below was modified to keep the unique datetime identifier as each
        # siis granulename is required to be uniquely named
        #granulename = re.sub('_[0-9]{8}T[0-9]{6}.geojson', '', os.path.basename(file))
        granulename = re.sub('.geojson', '', os.path.basename(file))

        # get the extents of the geojson mesh
        extents = lat_long_geojson(file)
        # express the extents as a geojson polygon
        shape = shapely.from_geojson('{"type": "Polygon", "coordinates": \
                  [[['+str(extents['lonmin'])+','+str(extents['latmax'])+'], \
                    ['+str(extents['lonmax'])+','+str(extents['latmax'])+'], \
                    ['+str(extents['lonmax'])+','+str(extents['latmin'])+'], \
                    ['+str(extents['lonmin'])+','+str(extents['latmin'])+'], \
                    ['+str(extents['lonmin'])+','+str(extents['latmax'])+'] ]] }')
        geom = wkb.dumps(shape, hex=True, srid=4326)

        hemi = ''
        if 'north' in os.path.basename(file).replace('.geojson', ''): hemi = 'N'
        if 'south' in os.path.basename(file).replace('.geojson', ''): hemi = 'S'
        
        if os.path.splitext(file)[-1] == '.geojson':
            productcode = "siis.meshiphi-geojson.s"
        else:
            raise Exception("File not recognised as geojson: %s", filename_dl)

        # if a file was unzipped then delete it
        if zipped == True:
            os.remove(file)
        
        ts_prov_md = datetime.strftime(datetime.now(timezone.utc), "%Y-%m-%dT%H:%M:%S.%f")

        # build the json metadata structure
        json_content = { \
                    "filename_dl": str(filename_dl),
                    "geom": str(geom),
                    "granulename": str(granulename),
                    "hemi": str(hemi),
                    "lowres": lowres,
                    "md5_dl": str(md5_dl),
                    "onrequest": onrequest,
                    "productcode": str(productcode),
                    "size_dl": str(size_dl),
                    "ts_acq": str(ts_acq),
                    "ts_prov_granule": str(ts_prov_granule),
                    "ts_prov_md": str(ts_prov_md),
                    "uuid": str(uuid_v4),
                    "zipped": zipped
                    }

        # write the metadata file to disk
        try:
            with open(output_filepath, 'w') as f:
                f.write(json.dumps(json_content, indent=4))
        except Exception as e:
            raise Exception("Unable to write metadata file: %s", e)



def main():
    """
    Metadata creation entry point
    """
        
    parser = argparse.ArgumentParser(description=DESCRIPTION+' v'+VERSION)
    parser.add_argument("files", help="Create siis metadata for one or more files", type=str, nargs='+')
    args = parser.parse_args()


    # Now kick off main
    checked_files = check_input_filenames(args.files)
    generate_output(checked_files)



if __name__ == "__main__":
    main()