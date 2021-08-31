import os
import sys
from timeit import default_timer as timer

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

class PdfExportPlugin(BasePlugin):

    DEFAULT_MEDIA_TYPE = 'print'

    config_scheme = (
        ('media_type', config_options.Type(str, default=DEFAULT_MEDIA_TYPE)),
        ('verbose', config_options.Type(bool, default=False)),
        ('enabled_if_env', config_options.Type(str)),
        ('combined', config_options.Type(bool, default=False)),
        ('combined_output_path', config_options.Type(str, default="pdf/combined.pdf")),
        ('theme_handler_path', config_options.Type(str))
    )

    def __init__(self):
        self.renderer = None
        self.enabled = True
        self.combined = False
        self.num_files = 0
        self.num_errors = 0
        self.total_time = 0

    def on_config(self, config):
        if 'enabled_if_env' in self.config:
            env_name = self.config['enabled_if_env']
            if env_name:
                self.enabled = os.environ.get(env_name) == '1'
                if not self.enabled:
                    print('PDF export is disabled (set environment variable {} to 1 to enable)'.format(env_name))
                    return

        self.combined = self.config['combined']
        if self.combined:
            print('Combined PDF export is enabled')

        from weasyprint.logger import LOGGER
        import logging

        if self.config['verbose']:
            LOGGER.setLevel(logging.DEBUG)
        else:
            LOGGER.setLevel(logging.ERROR)

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        LOGGER.addHandler(handler)
        return config

    def on_nav(self, nav, config, files):
        if not self.enabled:
            return nav

        from .renderer import Renderer
        self.renderer = Renderer(self.combined, config['theme'].name, self.config['theme_handler_path'])

        self.renderer.pages = [None] * len(nav.pages)
        for page in nav.pages:
            self.renderer.page_order.append(page.file.url)

        return nav

    def on_post_page(self, output_content, page, config):
        if not self.enabled:
            return output_content

        start = timer()

        self.num_files += 1

        try:
            abs_dest_path = page.file.abs_dest_path
            src_path = page.file.src_path
        except AttributeError:
            # Support for mkdocs <1.0
            abs_dest_path = page.abs_output_path
            src_path = page.input_path

        path = os.path.dirname(abs_dest_path)
        os.makedirs(path, exist_ok=True)

        filename = os.path.splitext(os.path.basename(src_path))[0]

        from weasyprint import urls
        base_url = urls.path2url(os.path.join(path, filename))
        pdf_file = filename + '.pdf'

        try:
            if self.combined:
                self.renderer.add_doc(output_content, base_url, page.file.url)
                pdf_path = self.get_path_to_pdf_from(page.file.dest_path)
                output_content = self.renderer.add_link(output_content, pdf_path)
            else:
                self.renderer.write_pdf(output_content, base_url, os.path.join(path, pdf_file))
                output_content = self.renderer.add_link(output_content, pdf_file)
        except Exception as e:
            print('Error converting {} to PDF: {}'.format(src_path, e), file=sys.stderr)
            self.num_errors += 1

        end = timer()
        self.total_time += (end - start)

        return output_content

    def on_post_build(self, config):
        if not self.enabled:
            return

        if self.combined:
            start = timer()

            abs_pdf_path = os.path.join(config['site_dir'], self.config['combined_output_path'])
            os.makedirs(os.path.dirname(abs_pdf_path), exist_ok=True)
            self.renderer.write_combined_pdf(abs_pdf_path)

            end = timer()
            self.total_time += (end - start)

        print('Converting {} files to PDF took {:.1f}s'.format(self.num_files, self.total_time))
        if self.num_errors > 0:
            print('{} conversion errors occurred (see above)'.format(self.num_errors))

    def get_path_to_pdf_from(self, start):
        pdf_split = os.path.split(self.config['combined_output_path'])
        start_dir = os.path.split(start)[0]
        pdf_dir = pdf_split[0] if pdf_split[0] else '.'
        return os.path.join(os.path.relpath(pdf_dir, start_dir), pdf_split[1])
