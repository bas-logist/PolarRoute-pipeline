import os

DIRECTORY = os.getenv("DIRECTORY")
REGIONS_VESSELS = os.getenv("REGIONS_VESSELS")
COMPRESSED = os.getenv("COMPRESSED")
OUTPUT_FULLPATH = os.getenv("OUTPUT_FULLPATH")

def create_expected_output_filelist(directory: str, 
                                    regions_vessels: list[dict],
                                    compressed: bool):
    """
    Create a list of expected output files,
    which we want to gather metadata from.
    Parses a list-of-dictionaries and expects the dictionaries to be in 
    the format: {"region": "A", "vessel": "B"}
    """
    expected_files = []
    for region_vessel in regions_vessels:
        expected_files.append(f"{directory}/amsr_{region_vessel["region"]}_\
                              {region_vessel["vessel"]}.vessel.geojson")
        expected_files.append(f"{directory}/amsr_{region_vessel["region"]}_\
                                {region_vessel["vessel"]}.vessel.json")
        expected_files.append(f"{directory}/amsr_{region_vessel["region"]}\
                              .mesh.json")

    # chuck out region mesh duplicated filenames
    expected_files = list(set(expected_files))

    # make compressed if option set
    if compressed:
        expected_files = [i + ".gz" for i in expected_files]
    return expected_files


def main():
    files_for_metadata = create_expected_output_filelist(DIRECTORY, REGIONS_VESSELS, COMPRESSED)
    with open(OUTPUT_FULLPATH, "w") as output_file:
        output_file.writelines(line + "\n" for line in files_for_metadata)

if __name__ == "__main__":
    main()
