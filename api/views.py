from django.core.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers.create import RegistrationSerializer
from .serializers.login import LoginSerializer
from .serializers.scrape import ScrapeSerializer, ScrapeDetailSerializer
from .models import User
import requests
from bs4 import BeautifulSoup
from .models import ScrapeModel, User

class CreateUserView(APIView):
    
    permission_classes = (AllowAny,)
    
    def post(self, request):
        try:
            print(request.data)
            serializer = RegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return JsonResponse({
                "status":"error",
                "message":e.message
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return JsonResponse({
                "status":"error",
                "message":"Bad gateway cannot register user"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    
    permission_classes =  (AllowAny,)
    
    def post(self, request):
        try:
            print(request.data)
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return JsonResponse({
                "status":"error",
                "message":e.message
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return JsonResponse({
                "status":"error",
                "message":"Bad gateway cannot login user"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

class ScrapeView(APIView):
    
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            serializer = ScrapeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            url = serializer.validated_data.pop('url')
            page = requests.get(url)
            
            soup = BeautifulSoup(page.content, 'html.parser')
            
            data = {}
            
            
            try:
                data["title"] = soup.find("span", class_="B_NuCI").text
            except Exception as e:
                print("cannot get title")
            try:
                data["price"] = soup.find("div", class_="_30jeq3 _16Jk6d").text
            except Exception as e:
                print("cannot get price")
            try:
                data["description"] = soup.find("div", class_="_1mXcCf RmoJUa").findChild("p").text
            except Exception as e:
                print("cannot get description")
            try:
                data["ratings"] = soup.find("span", class_="_2_R_DZ").findChild("span").text
            except Exception as e:
                print("cannot get rating")
            try:
                data["media_count"] = len(soup.find("ul", class_="_3GnUWp").find_all("li"))
            except Exception as e:
                print("cannot get media count")

            scrape_data = ScrapeModel.objects.create(user=request.user, url=url, **data)
            scrape_serializer = ScrapeDetailSerializer(scrape_data)
            
            return JsonResponse(scrape_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return JsonResponse({
                "status":"error",
                "message":e.message
            }, status=status.HTTP_400_BAD_REQUEST)
        except (IntegrityError, DatabaseError) as e:
            return JsonResponse({
                "status":"error",
                "message":"URL already parsed"
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(str(e))
            return JsonResponse({
                "status":"error",
                "message":"Bad gateway cannot login user"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ScrapeDetailView(APIView):
    
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            serializer = ScrapeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            url = serializer.validated_data.pop('url')
            
            scrape_data =  ScrapeModel.objects.get(url=url)
            
            scrape_serializer = ScrapeDetailSerializer(scrape_data)
            
            return JsonResponse(scrape_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return JsonResponse({
                "status":"error",
                "message":e.message
            }, status=status.HTTP_400_BAD_REQUEST)
        except ScrapeModel.DoesNotExist as e:
            return JsonResponse({
                "status":"error",
                "message":"Given URL has not been scraped yet"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(str(e))
            return JsonResponse({
                "status":"error",
                "message":"Bad gateway cannot login user"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)