import os
from figma_export.figma import FigmaService
from .AbstractExporter import AbstractExporter


class ImageExporter(AbstractExporter):
    """Exporter description"""
    supported_formats = ["png", "jpg", "svg"]

    def __call__(
        self,
        scale: AbstractExporter.ScaleArgument,
        selector: AbstractExporter.SelectorArgument
    ):
        figma_service = FigmaService()
        document = figma_service.load_document(self.document_id)
        if not os.path.isdir(document.name):
            os.mkdir(document.name)
        os.chdir(document.name)

        rendering_results = figma_service.render_components(
            document,
            self.export_format,
            scale,
            selector
        )
        for result in rendering_results:
            path = os.path.join(f"{result.node.name}_x{result.scale}.{result.format}")
            with open(path, "wb") as f:
                f.write(result.data)
