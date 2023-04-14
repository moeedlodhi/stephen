from django.conf import settings
from .utils import encode_audio_file, encode_audio
from django.db import transaction
import requests
from celery import shared_task
from time import sleep
from .models import Notifications



@shared_task(name="hello_task")
def new_task(request):
    sleep(10)
    print('sleep completed')


@shared_task
def long_running_task(data):
    with transaction.atomic():
        try:
            audio_file = {"file": bytes(data['temp_file'], 'utf-8')}
            
            """Send data to system A"""
            r1 = requests.post(f"{settings.HOST}/wrapper/mock_api", files=audio_file)
            if r1.status_code != 201:
                raise Exception('failure')
            
            """Send data to system B"""
            encoded_file = encode_audio(r1.json()['data'][0].encode('utf-8'))
            audio_file = {"file":encoded_file}
            r2 = requests.post(f"{settings.HOST}/wrapper/mock_api", files=audio_file)
            if r2.status_code != 201:
                raise Exception('failure')
            
            """Send data to system C"""
            encoded_file = encode_audio(r2.json()['data'][0].encode('utf-8'))
            audio_file = {"file":encoded_file}
            r3 = requests.post(f"{settings.HOST}/wrapper/mock_api", files=audio_file)
            if r3.status_code != 201:
                raise Exception('failure')
            Notifications.objects.create(message="put message here", is_read=False)
            return (r1, r2, r3)
        except Exception as e:
            raise Exception(str(e))
