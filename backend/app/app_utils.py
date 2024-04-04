import logging
import os
from typing import Optional
import urllib.parse
from flask import jsonify, make_response, Response

#logger set up
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)



def response(body: Optional[dict] = None, status_code: int = 200) -> Response:
    if not isinstance(body, dict):
        body = {'data': body}
    return make_response(jsonify(body), status_code)
