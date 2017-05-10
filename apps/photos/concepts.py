# -*- coding: utf-8 -*-
import json
from io import BytesIO

from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from clarifai.rest.client import ApiError

from django.conf import settings


def photo_concepts(photo):
    """Concepts data returned by Clarifai API for given photo.
    """
    with open(settings.CLARIFAI_CREDENTIALS_FILE) as data_file:
        credentials = json.load(data_file)
    app_id = credentials['api_key']
    app_secret = credentials['api_secret']
    app = ClarifaiApp(app_id=app_id, app_secret=app_secret)
    model = app.models.get(settings.CLARIFAI_API_VERSION)
    image = ClImage(file_obj=BytesIO(photo.read()))
    try:
        result = model.predict([image])
    except ApiError:
        result = []
    return result
