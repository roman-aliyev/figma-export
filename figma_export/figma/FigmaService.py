import json
from typing import List
from .FigmaClient import FigmaClient
from .FigmaDocument import FigmaDocument
from .FigmaNode import FigmaNode
from .FigmaRenderingResult import FigmaRenderingResult


class FigmaService:
    def __init__(self):
        self.__client = FigmaClient()

    def load_document(
        self,
        document_id: str
    ):
        data = json.loads(
            self.__client.request_document_data(document_id)
        )

        current_path = []
        paths = {}

        def find_components(current_data):
            if current_data.get("type") == "COMPONENT":
                paths[current_data.get('id')] = "/" + "/".join(current_path)
                return
            current_path.append(current_data.get("name"))
            for k, v in current_data.items():
                if isinstance(v, list) and k == "children":
                    for node in v:
                        find_components(node)
            current_path.pop()

        find_components(data["document"])

        return FigmaDocument(
            document_id,
            data["name"],
            list(
                map(
                    lambda kv: FigmaNode(
                        kv[0],
                        kv[1]["name"],
                        paths[kv[0]]
                    ),
                    data["components"].items()
                )
            )
        )

    def render_components(
            self,
            document: FigmaDocument,
            rendering_format: str,
            scale: float = 1,
            select_expression: str = None
    ) -> List[FigmaRenderingResult]:
        rendering_results = []
        if select_expression is None:
            components = document.components
        else:
            components = list(filter(
                lambda component:
                component.path.startswith(select_expression),
                document.components
            ))
        if len(components) == 0:
            return rendering_results
        image_urls = json.loads(
            self.__client.request_image_urls(
                document.id,
                list(map(lambda node: node.id, components)),
                scale,
                rendering_format)
        )
        for component in components:
            rendering_results.append(
                FigmaRenderingResult(
                    component,
                    rendering_format,
                    scale,
                    self.__client.request_data(image_urls["images"][component.id])
                )
            )
        return rendering_results
