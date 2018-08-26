import sys

from importlib import import_module
from weasyprint import HTML
from bs4 import BeautifulSoup

from .themes import generic as generic_theme


class Renderer(object):
    def __init__(self, theme: str):
        self.theme = self._load_theme_handler(theme)

    def render_pdf(self, content: str, base_url: str, filename: str):
        soup = BeautifulSoup(content, 'html.parser')

        stylesheet = self.theme.get_stylesheet()
        if stylesheet:
            style_tag = soup.new_tag('style')
            style_tag.string = stylesheet

            soup.head.append(style_tag)

        html = HTML(string=str(soup), base_url=base_url)
        html.write_pdf(filename)

    def add_link(self, content: str, filename: str):
        return self.theme.modify_html(content, filename)

    @staticmethod
    def _load_theme_handler(theme: str):
        try:
            module_name = '.' + theme.replace('-', '_')
            return import_module(module_name, 'mkdocs_pdf_export_plugin.themes')
        except ImportError as e:
            print('Could not load theme {}: {}'.format(theme, e), file=sys.stderr)
            return generic_theme

