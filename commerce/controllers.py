import bcrypt
import jwt
import datetime
from PIL import Image
from io import BytesIO
import boto3
from botocore.exceptions import ClientError
from commerce_server.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME, AWS_STORAGE_BUCKET_NAME

secret_key:str = "alegbeleye"

def generate_token(customer_id) -> dict:
    payload = {
            "user_id": customer_id,
            "exp" : datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
    }

    #Generate the JWT
    token = jwt.encode(payload, secret_key, algorithm = 'HS256')

    return token

def upload_image_to_s3(uploaded_image, id: str, name:str) -> str:
    
    boto_3_Client = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
  
    #compressing the image
    image = Image.open(uploaded_image)
    compressed_image = BytesIO()
    image.save(compressed_image, format='JPEG', quality=50)
    
    compressed_image.seek(0)
        
    image_key = f"products/{name}/{id}/{id}.jpg"

    #if the name has any spaces join them together with a plus -> '+'
    splitted_key = image_key.split(' ')
    url_key = '+'.join(splitted_key)


    try:
        response = boto_3_Client.upload_fileobj(compressed_image, AWS_STORAGE_BUCKET_NAME, image_key)
    except ClientError:
        print(f'could not upload {name} to {AWS_STORAGE_BUCKET_NAME}')

    url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/{url_key}"

    return url