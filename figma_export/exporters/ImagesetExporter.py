import os
import json
from figma_export.figma import FigmaService
from .AbstractExporter import AbstractExporter


_contents_data = {
    "images": [
        {
            "idiom": "universal",
            "filename": "1.png",
            "scale": "1x"
        },
        {
            "idiom": "universal",
            "filename": "2.png",
            "scale": "2x"
        },
        {
            "idiom": "universal",
            "filename": "3.png",
            "scale": "3x"
        }
    ],
    "info": {
        "version": 1,
        "author": "xcode"
    }
}


class ImagesetExporter(AbstractExporter):
    """Exports Figma document and saves the result to Xcode Asset Catalog"""
    supported_formats = ["imageset"]

    def __call__(
            self,
            selector: AbstractExporter.SelectorArgument
    ):
        figma_service = FigmaService()
        document = figma_service.load_document(self.document_id)
        if not os.path.isdir(document.name):
            os.mkdir(document.name)
        os.chdir(document.name)

        rendering_results = []

        for scale in [1, 2, 3]:
            rendering_results.extend(
                figma_service.render_components(
                    document,
                    "png",
                    scale,
                    selector
                )
            )

        for result in rendering_results:
            dir_name = result.node.name + ".imageset"
            if not os.path.isdir(dir_name):
                os.mkdir(dir_name)
                with open(os.path.join(dir_name, "Contents.json"), "w") as f:
                    json.dump(_contents_data, f)
            path = os.path.join(dir_name, f"{result.scale}.png")
            with open(path, "wb") as f:
                f.write(result.data)
