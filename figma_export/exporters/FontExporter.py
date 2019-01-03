import os
import tempfile
from figma_export.figma import FigmaService, FigmaRenderingResult
from .AbstractExporter import AbstractExporter
from typing import List


class _FontForgeContext(object):
    def __init__(self):
        self.glyphs = {}
        self.temp_files = []

    def reset(self):
        self.glyphs.clear()
        for f in self.temp_files:
            f.close()
        self.temp_files.clear()

    def add_svg_glyph(self, char: str, data: bytes):
        code = hex(ord(char[0]))
        f = tempfile.NamedTemporaryFile(suffix=f".svg", dir=".")
        f.write(data)
        f.flush()
        self.glyphs[code] = os.path.basename(f.name)
        self.temp_files.append(f)

    def save(self, family_name: str, font_style: str, font_format: str, emboldening: float):
        with tempfile.NamedTemporaryFile(mode="w+t", dir=".") as f:
            f.write(self.__fontforge_script(family_name, font_style, font_format, emboldening))
            f.flush()
            if os.system(f"fontforge -script \"{os.path.basename(f.name)}\"") != 0:
                raise Exception("problem while running fontforge.")

    def __fontforge_script(self, family_name: str, font_style: str, font_format: str, emboldening: float):
        return f"""
familyname = '{family_name}'
style = '{font_style}'
glyphs = {str(self.glyphs)}
format = '{font_format}'
emboldening = {emboldening}

import psMat

if __name__ == '__main__':
    font = fontforge.font()
    font.familyname = familyname
    font.fontname = familyname + '-' + style
    font.fullname = familyname + ' ' + style
    font.encoding = 'UnicodeFull'

    for k, v in glyphs.items():
        g = font.createChar(int(k, 0))
        g.importOutlines(v)
        if emboldening is not 0:
            g.changeWeight(font.em * emboldening)
        g.transform(psMat.scale(font.em / g.boundingBox()[3]))

    font.generate(familyname + '-' + style + '.' + format)
    font.close()
            """


class FontExporter(AbstractExporter):
    """Exports Figma document and saves the result to iconic font"""
    supported_formats = ["otf", "ttf", "woff"]

    class FontStyleArgument(str, AbstractExporter.AbstractArgument):
        """font style. Regular, Semibold, Bold, Black etc, default=Regular."""
        default = "Regular"

    class FontEmboldeningArgument(float, AbstractExporter.AbstractArgument):
        """makes glyphs wider or lighter by the number of em units. >=-1, <=1, default=0."""
        default = 0

    def __call__(
            self,
            style: FontStyleArgument,
            emboldening: FontEmboldeningArgument,
            selector: AbstractExporter.SelectorArgument
    ):
        figma_service = FigmaService()
        document = figma_service.load_document(self.document_id)
        if not os.path.isdir(document.name):
            os.mkdir(document.name)
        os.chdir(document.name)

        rendering_results = figma_service.render_components(
            document,
            "svg",
            1,
            selector
        )
        ff_context = _FontForgeContext()
        for result in rendering_results:
            ff_context.add_svg_glyph(result.node.name, result.data)
        ff_context.save(document.name, style, self.export_format, emboldening)
        ff_context.reset()
