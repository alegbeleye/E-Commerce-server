from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from commerce.models import Customer, Product
from commerce.serializers import CustomerSerializer, ProductSerializer
from commerce.controllers import generate_token

from rest_framework import status

# Create your views here.

class CustomerView(APIView):

    def get(self, request, id) -> Response:
        try:
            data = Customer.objects.get(pk=id)
        except Customer.DoesNotExist:
            return Response("User not found!", status=status.HTTP_404_NOT_FOUND)
        serialized = CustomerSerializer(data)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id) -> Response:
        try:
            data = Customer.objects.get(pk = id)
            data.delete()
        except Customer.DoesNotExist:
            return Response("User not found!", status=status.HTTP_404_NOT_FOUND)
        return Response("deleted user", status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serialized = CustomerSerializer(data=data)
        if serialized.is_valid():
            customer_instance = serialized.save()
            customer_instance.hash_password(customer_instance.hashed_password)
            customer_instance.save()
        else:
            print(data, serialized.data)
            return Response("Invalid Request.", status=status.HTTP_400_BAD_REQUEST)
        return Response("Created User.", status=status.HTTP_201_CREATED)
    


class ProductView(APIView):
    def get(self, request, id):
        try:
            data = Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return Response("This product does not exist.", status=status.HTTP_404_NOT_FOUND)
        serialized_product = ProductSerializer(data)
        return Response(serialized_product.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        data = request.data
        image = request.FILES['product_image']
        print(image)
        serialized = ProductSerializer(data=data)
        if serialized.is_valid():
            product_instance = serialized.save()
            product_instance.apply_percentage_cut_to_price()
            if image: product_instance.apply_url_to_image(image)
            product_instance.save()
        else:
            return Response("Sorry an issue Occured saving the product.", status=status.HTTP_400_BAD_REQUEST)
        return Response("Created product", status=status.HTTP_201_CREATED)
    
    def delete(self, request, id):
        try:
            data = Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return Response('The product does not exist', status=status.HTTP_404_NOT_FOUND)
        data.delete()
        return Response("Deleted Product", status=status.HTTP_200_OK)



class SignInView(APIView):

    def post(self, request) -> None:
        sign_in_details = request.data

        try:
            customer = Customer.objects.get(email = sign_in_details['email'])
        except Customer.DoesNotExist:
            return Response("Email or Password is incorrect", status=status.HTTP_404_NOT_FOUND)
        
        if customer.compare_password(sign_in_details['password']):
            token  = generate_token(customer.id)
            return Response({"token":token}, status=status.HTTP_200_OK)
        else:
            return Response("Email or Password is incorrect", status=status.HTTP_400_BAD_REQUEST)
        

