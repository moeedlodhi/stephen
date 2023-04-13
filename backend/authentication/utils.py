import base64
import tempfile

def create_temp_file(encoded_file):
    decoded_data = base64.b64decode(encoded_file)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    # write decoded data to temporary file
        temp_file.write(decoded_data)

        # print path of temporary file
        return temp_file

def encode_audio_file(audio_file):
    audio_content = audio_file.read()
    encoded_audio = base64.b64encode(audio_content)
    return encoded_audio

def encode_audio(audio_bytes):
    encoded_audio = base64.b64encode(audio_bytes)
    return encoded_audio
