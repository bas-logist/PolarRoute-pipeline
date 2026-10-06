import os
import pathlib

# Get environment variables provided from flow.cylc
DIRECTORIES = os.environ.get("DIRECTORIES")

def main():
    directories_to_make = DIRECTORIES.split(",")
    for dir in directories_to_make:
        pathlib.Path(dir.strip()).mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    main()