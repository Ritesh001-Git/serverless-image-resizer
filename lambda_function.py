import boto3
from PIL import Image
import io

# Define S3 client outside the handler (good practice)
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        print("Event received:", event)
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        print(f"Processing file: {key} from bucket: {bucket}")

        # Download original image
        img_obj = s3.get_object(Bucket=bucket, Key=key)
        img_data = img_obj['Body'].read()
        image = Image.open(io.BytesIO(img_data))
        print("Original image size:", image.size)

        # Resize
        image = image.resize((300, 300))
        buffer = io.BytesIO()
        image.save(buffer, 'JPEG')
        buffer.seek(0)

        # Upload to resized-images bucket
        output_bucket = "resizedimg-bucket-lpu"  # Replace with your destination bucket
        s3.put_object(Bucket=output_bucket, Key=key, Body=buffer, ContentType='image/jpeg')
        print(f"Image uploaded to {output_bucket} as {key}")

        return {
            'statusCode': 200,
            'body': f"Resized image uploaded to {output_bucket}"
        }

    except Exception as e:
        print("Error:", str(e))
        raise e
