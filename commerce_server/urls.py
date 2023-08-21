"""
URL configuration for commerce_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from commerce.views import CustomerView, ProductView, SignInView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/customers/<str:id>/', CustomerView.as_view()),
    path('api/customers/', CustomerView.as_view()),
    path('api/products/<str:id>/', ProductView.as_view()),
    path('api/products/', ProductView.as_view()),
    path('api/auth/signin/', SignInView.as_view())
]
