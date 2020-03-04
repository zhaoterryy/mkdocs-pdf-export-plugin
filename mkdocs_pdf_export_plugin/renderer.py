import sys
import os

from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
from weasyprint import HTML
from bs4 import BeautifulSoup

from .themes import generic as generic_theme
from .preprocessor import get_separate as prep_separate, get_combined as prep_combined

class Renderer(object):
    def __init__(self, combined: bool, theme: str, theme_handler_path: str=None):
        self.theme = self._load_theme_handler(theme, theme_handler_path)
        self.combined = combined
        self.page_order = []
        self.pgnum = 0
        self.pages = []

    def write_pdf(self, content: str, base_url: str, filename: str):
        self.render_doc(content, base_url).write_pdf(filename)

    def render_doc(self, content: str, base_url: str, rel_url: str = None):
        soup = BeautifulSoup(content, 'html.parser')

        self.inject_pgnum(soup)

        stylesheet = self.theme.get_stylesheet()
        if stylesheet:
            style_tag = soup.new_tag('style')
            style_tag.string = stylesheet

            soup.head.append(style_tag)

        
        if self.combined:
            soup = prep_combined(soup, base_url, rel_url)
        else:
            soup = prep_separate(soup, base_url)

        html = HTML(string=str(soup))
        return html.render()

    def add_doc(self, content: str, base_url: str, rel_url: str):
        pos = self.page_order.index(rel_url)
        self.pages[pos] = (content, base_url, rel_url)

    def write_combined_pdf(self, output_path: str):
        rendered_pages = []
        for p in self.pages:
            if p is None:
                print('Unexpected error - not all pages were rendered properly')
                continue

            render = self.render_doc(p[0], p[1], p[2])
            self.pgnum += len(render.pages)
            rendered_pages.append(render)

        flatten = lambda l: [item for sublist in l for item in sublist]
        all_pages = flatten([p.pages for p in rendered_pages if p != None])

        rendered_pages[0].copy(all_pages).write_pdf(output_path)

    def add_link(self, content: str, filename: str):
        return self.theme.modify_html(content, filename)

    def inject_pgnum(self, soup):
        pgnum_counter = soup.new_tag('style')
        pgnum_counter.string = '''
        @page :first {{
            counter-reset: __pgnum__ {}; 
        }}
        @page {{
            counter-increment: __pgnum__;
        }}
        '''.format(self.pgnum)

        soup.head.append(pgnum_counter)

    @staticmethod
    def _load_theme_handler(theme: str, custom_handler_path: str = None):
        module_name = '.' + (theme or 'generic').replace('-', '_')

        if custom_handler_path:
            try:
                spec = spec_from_file_location(module_name, os.path.join(os.getcwd(), custom_handler_path))
                mod = module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod
            except FileNotFoundError as e:
                print('Could not load theme handler {} from custom directory "{}": {}'.format(theme, custom_handler_path, e), file=sys.stderr)
                pass

        try:
            return import_module(module_name, 'mkdocs_pdf_export_plugin.themes')
        except ImportError as e:
            print('Could not load theme handler {}: {}'.format(theme, e), file=sys.stderr)
            return generic_theme