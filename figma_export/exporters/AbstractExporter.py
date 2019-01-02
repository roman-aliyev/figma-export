

class AbstractExporter:
    supported_formats = []

    class AbstractArgument:
        pass

    class ScaleArgument(float, AbstractArgument):
        """image scale. >=0.01, <=4, default=1"""
        default = 1

    class SelectorArgument(str, AbstractArgument):
        """path to specific components in the document (for example '/Documents/Page 1/Frame 1').
        By default, selects all components."""
        default = "/"

    def __init__(self, export_format, document_id):
        self.export_format = export_format
        self.document_id = document_id
