import os

DIRECTORY = os.getenv("DIRECTORY")
REGION = os.getenv("REGION")
VESSEL = os.getenv("VESSEL")
COMPRESSED = os.getenv("COMPRESSED").upper()
OUTPUT_FULLPATH = os.getenv("OUTPUT_FULLPATH")

def create_expected_output_filelist(directory: str, 
                                    region: str,
                                    vessel: str,
                                    compressed: str):
    """
    Create a list of expected output files,
    which we want to gather metadata from.
    Parses a list-of-dictionaries and expects the dictionaries to be in 
    the format: {"region": "A", "vessel": "B"}
    """
    expected_files = []
    expected_files.append(f"{directory}/amsr_{region}_{vessel}.vessel.json")
    expected_files.append(f"{directory}/amsr_{region}.mesh.json")

    # chuck out region mesh duplicated filenames
    expected_files = list(set(expected_files))

    # make compressed if option set
    # cylc doesn't do well with providing booleans from environment, hence string comparison
    if compressed == "TRUE":
        expected_files = [i + ".gz" for i in expected_files]
    return expected_files


def main():
    files_for_metadata = create_expected_output_filelist(DIRECTORY, REGION, VESSEL, COMPRESSED)
    with open(OUTPUT_FULLPATH, "w") as output_file:
        output_file.writelines(line + "\n" for line in files_for_metadata)

if __name__ == "__main__":
    main()
