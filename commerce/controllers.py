import bcrypt
import jwt
import datetime
from PIL import Image
from io import BytesIO
import boto3
from botocore.exceptions import ClientError
from commerce_server.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME, AWS_STORAGE_BUCKET_NAME
from rest_framework.response import Response
from rest_framework import status

secret_key:str = "alegbeleye"

def generate_token(customer_id:str) -> dict:
    payload = {
            "user_id": customer_id,
            "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
    }

    #Generate the JWT
    token = jwt.encode(payload, secret_key, algorithm = 'HS256')

    return token

def decode_token(encoded_token: str) -> Response:
    encoded_token = encoded_token[7:]
    print(encoded_token)
    try:
        decoded_token = jwt.decode(encoded_token, secret_key, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        return Response({"error":"Token Expired"}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({"error":"Token Invalid"}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({"message": "Token successfully validated"}, status=status.HTTP_200_OK)


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