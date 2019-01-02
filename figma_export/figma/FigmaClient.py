import os
from urllib.parse import urlencode
from urllib.request import (Request, urlopen)
from typing import List


class FigmaClient:
    """Makes requests to Figma API. For more info follow https://www.figma.com/developers/docs"""
    def __init__(self):
        self.__personal_token = os.environ["FIGMA_ACCESS_TOKEN"]

    def request_document_data(self, document_id: str) -> bytes:
        """Makes request to 'GET file' endpoint."""
        return self.request_data(
            f"https://api.figma.com/v1/files/{document_id}"
        )

    def request_image_urls(self, key: str, ids: List[str], scale: float, _format: str) -> bytes:
        """Makes request to 'GET image' endpoint."""
        parameters = {
            "ids": ",".join(ids),
            "scale": scale,
            "format": _format
        }
        return self.request_data(
            f"https://api.figma.com/v1/images/{key}?%s" % urlencode(parameters)
        )

    def request_data(self, url: str) -> bytes:
        request = Request(url)
        request.headers["x-figma-token"] = self.__personal_token
        response = urlopen(request)
        data = response.read()
        return data
