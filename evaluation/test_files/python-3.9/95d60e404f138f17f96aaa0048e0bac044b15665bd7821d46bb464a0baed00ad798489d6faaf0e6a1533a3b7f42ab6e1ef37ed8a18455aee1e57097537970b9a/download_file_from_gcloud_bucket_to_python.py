import google.cloud.storage

def download_file_from_gcloud_bucket_to_python(bucket_name: str, file_name: str) -> google.cloud.storage.blob.Blob:
    """
    Read a file from a google cloud bucket into python memory

    Parameters
    ----------
    bucket_name: str
        The name of the google cloud bucket
    file_name: str
        The name of the file to be downloaded

    Returns
    -------
    google.cloud.storage.blob.Blob
        A wrapper around Cloud Storage's concept of an Object
        See "Example Usage" (below) for examples of how to interact with this object

    Example Usage
    -------------
    >>>import json
    >>>import pandas as pd
    >>>import google.cloud.storage
    >>>with download_file_from_gcloud_bucket_to_python(
    ...         bucket_name="my-bucket-name", file_name="my_json_file.json"
    ...     ).open("r") as f:
    ...         my_json = json.load(f)
    >>>with download_file_from_gcloud_bucket_to_python(
    ...            bucket_name="my-bucket-name", file_name="my_text_file.txt"
    ...     ).open("r") as f:
    ...         my_text = f.read()
    >>>with download_file_from_gcloud_bucket_to_python(
    ...         bucket_name="my-bucket-name", file_name="my_table.csv"
    ...     ).open("r") as f:
    ...         my_table = pd.read_csv(f)
    """
    bucket = google.cloud.storage.Client().bucket(bucket_name)
    blob = bucket.blob(file_name)
    return blob