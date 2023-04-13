# Create your views here.
import requests
from rest_framework.generics import GenericAPIView
from rest_framework import status
from infrastructure.response import CustomResponse
from django.conf import settings
import time
from .utils import encode_audio_file, encode_audio
from django.db import transaction

class WrapperApiView(GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        with transaction.atomic():
            try:
                temp_file = encode_audio_file(request.FILES['audio'])
                audio_file = {"file":temp_file}
                
                """Send data to system A"""
                r1 = requests.post(f"{settings.HOST}/wrapper/mock_api", files=audio_file)
                if r1.status_code != 201:
                    return CustomResponse(data=None, message="failue", status=status.HTTP_400_BAD_REQUEST)
                
                """Send data to system B"""
                encoded_file = encode_audio(r1.json()['data'][0].encode('utf-8'))
                audio_file = {"file":encoded_file}
                r2 = requests.post(f"{settings.HOST}/wrapper/mock_api", files=audio_file)
                if r2.status_code != 201:
                    return CustomResponse(data=None, message="failue", status=status.HTTP_400_BAD_REQUEST)
                
                """Send data to system C"""
                encoded_file = encode_audio(r2.json()['data'][0].encode('utf-8'))
                audio_file = {"file":encoded_file}
                r3 = requests.post(f"{settings.HOST}/wrapper/mock_api", files=audio_file)
                if r3.status_code != 201:
                    return CustomResponse(data=None, message="failue", status=status.HTTP_400_BAD_REQUEST)
                return CustomResponse(data=None, message="success", status=status.HTTP_201_CREATED)
            except Exception as e:
                return CustomResponse(data=None, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MockApi(GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        try:
            time.sleep(5)
            audio_files_received = request.FILES['file']
            data=audio_files_received
            return CustomResponse(data=audio_files_received, message="success", status=status.HTTP_201_CREATED)
        except Exception as e:
            return CustomResponse(data=None, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)