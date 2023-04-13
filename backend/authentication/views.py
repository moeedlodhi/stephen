# Create your views here.
import requests
from rest_framework.generics import GenericAPIView
from rest_framework import status
from infrastructure.response import CustomResponse
import time
from .tasks import long_running_task
from .utils import encode_audio_file

class WrapperApiView(GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        try:
            temp_file = encode_audio_file(request.FILES['audio'])
            long_running_task.delay({"temp_file": str(temp_file)})
            return CustomResponse(data=None, message="success", status=status.HTTP_200_OK)
        except Exception as e:
            return CustomResponse(data=None, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MockApi(GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        try:
            """This is a dummy api to mock a system upload"""
            time.sleep(5)
            audio_files_received = request.FILES['file']
            return CustomResponse(data=audio_files_received, message="success", status=status.HTTP_201_CREATED)
        except Exception as e:
            return CustomResponse(data=None, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)