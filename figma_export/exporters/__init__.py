from inspect import signature
from .ImageExporter import ImageExporter
from .ImagesetExporter import ImagesetExporter
from .FontExporter import FontExporter
from .AbstractExporter import AbstractExporter

exporters_by_format = {
    "png": ImageExporter,
    "jpg": ImageExporter,
    "svg": ImageExporter,
    "imageset": ImagesetExporter,
    "otf": FontExporter,
    "ttf": FontExporter,
    "woff": FontExporter
}

# validation of exporters_by_format
for export_format, exporter_type in exporters_by_format.items():
    if not issubclass(exporter_type, AbstractExporter) or exporter_type is AbstractExporter:
        raise Exception(f"'{exporter_type.__name__}' is invalid type for exporter."
                        f"Only subclass of AbstractExporter excepted")
    if export_format not in exporter_type.supported_formats:
        raise Exception(f"'{exporter_type.__name__}' does not support '{export_format}' format.")
    for k, v in signature(exporter_type.__call__).parameters.items():
        if k == "self":
            continue
        if not issubclass(v.annotation, AbstractExporter.AbstractArgument)\
                or v.annotation is AbstractExporter.AbstractArgument:
            raise Exception(f"'{v.name}' in the '{exporter_type.__name__}.__call__' has invalid type."
                            f"Only subclass of AbstractArgument excepted")
