import os
import base64
from PIL import Image
from fastapi import status, HTTPException


MEDIA_DIRECTORY = "/vol/media"


def get_response(done: bool, success_message: str, error_message: str):
    if not done:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message
        )
    return success_message


async def rise_http_exception(result, message: str):
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)


def save_img(file, folder_name: str = "", file_name: str = None):
    img_name = file_name.lower().replace(" ", "")
    path = os.path.join(MEDIA_DIRECTORY, folder_name)
    img_path = os.path.join(path, img_name)
    output_size = (250, 250)
    img = Image.open(file.file)
    img.thumbnail(output_size)
    img.save(img_path)
    return img_path


def encode_image(content):
    return base64.b64encode(content).decode("utf-8")
