import sys

from importlib import import_module
from weasyprint import HTML, Document
from bs4 import BeautifulSoup

from .themes import generic as generic_theme


class Renderer(object):
    def __init__(self, theme: str, combined: bool):
        self.theme = self._load_theme_handler(theme)
        self.combined = combined
        self.combined_doc = None

    def write_pdf(self, content: str, base_url: str, filename: str):
        self.render_doc(content, base_url).write_pdf(filename)

    def render_doc(self, content: str, base_url: str):
        soup = BeautifulSoup(content, 'html.parser')

        stylesheet = self.theme.get_stylesheet()
        if stylesheet:
            style_tag = soup.new_tag('style')
            style_tag.string = stylesheet

            soup.head.append(style_tag)

        html = HTML(string=str(soup), base_url=base_url)
        return html.render()

    def add_doc(self, content: str, base_url: str):
        render = self.render_doc(content, base_url)
        cdoc = self.combined_doc
        if cdoc is None:
            self.combined_doc = render
        else:
            self.combined_doc = cdoc.copy(cdoc.pages + render.pages)

    def write_combined_pdf(self, output_path: str):
        self.combined_doc.write_pdf(output_path)

    def add_link(self, content: str, filename: str):
        return self.theme.modify_html(content, filename)

    @staticmethod
    def _load_theme_handler(theme: str):
        try:
            module_name = '.' + (theme or 'generic').replace('-', '_')
            return import_module(module_name, 'mkdocs_pdf_export_plugin.themes')
        except ImportError as e:
            print('Could not load theme {}: {}'.format(theme, e), file=sys.stderr)
            return generic_theme

