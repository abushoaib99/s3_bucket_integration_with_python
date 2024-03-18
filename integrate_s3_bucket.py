import boto3
import environ

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env('.env')

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


class S3Bucket:

    def __init__(self, file_path: str, bucket_name: str, object_name: str):
        self.file_path = file_path
        self.bucket_name = bucket_name
        self.object_name = object_name

    # Function to upload a file to S3 bucket
    def upload_file_to_s3(self):
        try:
            s3_client.upload_file(self.file_path, self.bucket_name, self.object_name)
            print(f"File uploaded successfully to s3://{self.bucket_name}/{self.object_name}")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def generate_signed_url_for_get(self, expiration=3600):
        try:
            signed_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': self.object_name},
                ExpiresIn=expiration
            )
            return signed_url
        except Exception as e:
            print(f"Error generating URL: {e}")

    def generate_signed_url_for_put(self, expiration=3600):
        try:
            signed_url = s3_client.generate_presigned_url(
                'put_object',
                Params={'Bucket': self.bucket_name, 'Key': self.object_name},
                ExpiresIn=expiration,
                HttpMethod='PUT'
            )
            return signed_url
        except Exception as e:
            print(f"Error generating URL: {e}")


def main():
    file_path = ''
    bucket_name = 'boineer-dev-bucket'
    object_name = 'media/avatar/image.jpg'

    s3_bucket = S3Bucket(
        bucket_name=bucket_name,
        object_name=object_name,
        file_path=file_path
    )

    signed_url = s3_bucket.generate_signed_url_for_get()
    # signed_url = s3_bucket.generate_signed_url_for_put()
    print(f"URL for the file: {signed_url}")


if __name__ == "__main__":
    main()
