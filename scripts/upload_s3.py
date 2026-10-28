import logging
import os

# handle s3fs as an optional dependency
try:
    import s3fs
except ImportError:
    s3fs = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

S3_ENV_VAR_NAME = "S3_UPLOAD"
UPLOAD_DIR = os.path.join(os.getenv("PIPELINE_DIRECTORY"), "upload")
TARGET_EXTENSIONS = (".json.gz", ".yaml.gz", ".json")
BUCKET_NAME = os.getenv("S3_BUCKET", None)
S3_ENDPOINT = os.getenv("S3_ENDPOINT", None)
S3_KEY = os.getenv("S3_KEY", None)
S3_SECRET = os.getenv("S3_SECRET", None)
S3_REGION = os.getenv("S3_REGION", None) # TODO sensible default for this?

def main():
    # check optional dependency is available
    if not s3fs:
        raise ImportError("Python s3fs package required but not found")

    fs = s3fs.S3FileSystem(
        endpoint_url=S3_ENDPOINT,
        key=S3_KEY,
        secret=S3_SECRET,
        client_kwargs={"region_name": S3_REGION}
    )

    logger.info(f"Starting upload using s3fs from '{UPLOAD_DIR}'...\n")

    for root, dirs, files in os.walk(UPLOAD_DIR):
        for filename in files:
            # Check if the file ends with any of the required extensions
            if filename.lower().endswith(TARGET_EXTENSIONS):
                local_path = os.path.join(root, filename)
                
                # Build the target S3 path
                relative_path = os.path.relpath(local_path, UPLOAD_DIR)
                s3_key = relative_path.replace(os.sep, "/")
                s3_path = f"{BUCKET_NAME}/{s3_key}"
                
                try:
                    print(f"Uploading: {filename} -> s3://{s3_path}")
                    fs.put(local_path, s3_path)
                except Exception as e:
                    print(f"Failed to upload {filename}: {e}")

    logger.info("\nScan and upload complete!")


if __name__ == "__main__":
    # proceed if allowed by environment variable
    if str(os.getenv(S3_ENV_VAR_NAME, None)).lower() == "true":
        main()