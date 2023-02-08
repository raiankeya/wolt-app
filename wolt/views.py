from flask import request
from marshmallow import ValidationError

from .constants import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .serializer import DaySerializer
from .utils import to_human_readable_times
from .response_serializer import WeekdaysEvent


def index():
    from .app import app

    app.logger.warning("Making %s request" % request.method)
    json_data = request.json
    if not json_data:
        return {"message": "No input data provided"}, HTTP_400_BAD_REQUEST
    try:
        serializer = DaySerializer()
        response = serializer.load(json_data)
        response = WeekdaysEvent(**response)
    except ValidationError as err:
        return err.messages, HTTP_400_BAD_REQUEST
    return to_human_readable_times(response.dict(exclude_none=True)), HTTP_200_OK
