import logging
import os

# handle s3fs as an optional dependency
try:
    import s3fs
except ImportError:
    s3fs = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_blank_string_to_none(variable_name):
    """
    If the user enters blank strings for optional S3 variables in their
    environment.cylc file, return None.
    """
    var = os.getenv(variable_name, None)
    sanitised_result = var.strip() if var else None
    return sanitised_result

TARGET_EXTENSIONS = (".json.gz", ".yaml.gz", ".json")
UPLOAD_DIRECTORY = os.getenv("UPLOAD_DIRECTORY", None)
S3_BUCKET_NAME = convert_blank_string_to_none("S3_BUCKET")
S3_PREFIX = convert_blank_string_to_none("S3_PREFIX")
S3_ENDPOINT = convert_blank_string_to_none("S3_ENDPOINT")
S3_KEY = convert_blank_string_to_none("S3_KEY")
S3_SECRET = convert_blank_string_to_none("S3_SECRET")
S3_REGION = convert_blank_string_to_none("S3_REGION")

def main():
    # check optional dependency is available
    if not s3fs:
        raise ImportError("Python s3fs package required but not found")

    fs = s3fs.S3FileSystem(
        endpoint_url=S3_ENDPOINT,
        key=S3_KEY,
        secret=S3_SECRET,
        client_kwargs={"region_name": S3_REGION} if S3_REGION else None,
    )

    logger.info(f"Starting upload using s3fs from '{UPLOAD_DIRECTORY}'...\n")

    for root, dirs, files in os.walk(UPLOAD_DIRECTORY):
        for filename in files:
            # Check if the file ends with any of the required extensions
            if filename.lower().endswith(TARGET_EXTENSIONS):
                local_path = os.path.join(root, filename)

                # Build the target S3 path
                relative_path = os.path.relpath(local_path, UPLOAD_DIRECTORY)
                s3_key = relative_path.replace(os.sep, "/")

                if S3_PREFIX is None:
                    s3_path = f"{S3_BUCKET_NAME}/{s3_key}"
                else:
                    s3_path = f"{S3_BUCKET_NAME}/{S3_PREFIX}/{s3_key}"

                try:
                    print(f"Uploading: {filename} -> s3://{s3_path}")
                    fs.put(local_path, s3_path)
                except Exception as e: #noqa: BLE001
                    print(f"Failed to upload {filename}: {e}")

    logger.info("\nScan and upload complete!")


if __name__ == "__main__":
    main()
