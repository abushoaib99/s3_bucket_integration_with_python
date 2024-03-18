import os

import boto3
import environ

BASE_DIR_DEV = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR_DEV, '.env'))

# AWS credentials and region
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = env('AWS_REGION_NAME')

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)


# Function to upload a file to S3 bucket
def upload_file_to_s3(file_path, bucket_name, object_name):
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File uploaded successfully to s3://{bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error uploading file: {e}")


# Function to read a file from S3 bucket
def read_file_from_s3(bucket_name, object_name):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
        data = response['Body'].read()
        print("Data::: ", response)
        # print(f"Content of file {object_name}:\n{data.decode('utf-8')}")
    except Exception as e:
        print(f"Error reading file: {e}")


def get_signed_url_for_get(bucket_name, object_name, expiration=3600):
    try:
        signed_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )
        return signed_url
    except Exception as e:
        print(f"Error generating URL: {e}")


def get_signed_url_for_put(bucket_name, object_name, expiration=3600):
    try:
        signed_url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration,
            HttpMethod='PUT'
        )
        return signed_url
    except Exception as e:
        print(f"Error generating URL: {e}")


# Example usage
if __name__ == "__main__":
    # Replace these with your own values
    file_path = 'path/to/your/local/file.txt'
    bucket_name = 'boineer-dev-bucket'
    object_name = 'media/avatar/image.jpg'

    # Upload file to S3
    # upload_file_to_s3(file_path, bucket_name, object_name)

    # Read file from S3
    # read_file_from_s3(bucket_name, object_name)
    # signed_url = get_signed_url_for_get(bucket_name, object_name)
    signed_url = get_signed_url_for_put(bucket_name, object_name)
    print(f"URL for the file: {signed_url}")
