import os
import sys
from timeit import default_timer as timer

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs import utils
from weasyprint import HTML, urls

from .renderer import Renderer


class PdfExportPlugin(BasePlugin):

    DEFAULT_MEDIA_TYPE = 'print'

    config_scheme = (
        ('media_type', config_options.Type(utils.string_types, default=DEFAULT_MEDIA_TYPE)),
        ('verbose', config_options.Type(bool, default=False)),
        ('enabled_if_env', config_options.Type(utils.string_types)),
    )

    def __init__(self):
        self.renderer = None
        self.enabled = True
        self.num_files = 0
        self.num_errors = 0
        self.total_time = 0

    def on_config(self, config):
        self.renderer = Renderer(config['theme'].name)

        from weasyprint.logger import LOGGER
        import logging

        if self.config['verbose']:
            LOGGER.setLevel(logging.DEBUG)
        else:
            LOGGER.setLevel(logging.ERROR)

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        LOGGER.addHandler(handler)

        if 'enabled_if_env' in self.config:
            env_name = self.config['enabled_if_env']
            self.enabled = os.environ.get(env_name) == '1'
            if not self.enabled:
                print('PDF export is disabled (set environment variable {} to 1 to enable)'.format(env_name))

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

        base_url = urls.path2url(os.path.join(path, filename))
        pdf_file = filename + '.pdf'

        try:
            self.renderer.render_pdf(output_content, base_url, os.path.join(path, pdf_file))
            output_content = self.renderer.add_link(output_content, pdf_file)
        except Exception as e:
            print('Error converting {} to PDF: {}'.format(src_path, e), file=sys.stderr)
            self.num_errors += 1

        end = timer()
        self.total_time += (end - start)

        return output_content

    def on_post_build(self, config):
        if self.enabled:
            print('Converting {} files to PDF took {:.1f}s'.format(self.num_files, self.total_time))
            if self.num_errors > 0:
                print('{} conversion errors occurred (see above)'.format(self.num_errors))
