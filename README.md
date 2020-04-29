# MkDocs PDF Export Plugin [![Build Status][travis-status]][travis-link]

*An MkDocs plugin to export content pages as PDF files*

The pdf-export plugin will export all markdown pages in your MkDocs repository as PDF files using [WeasyPrint](http://weasyprint.org/). The exported documents support many advanced features missing in most other PDF exports, such as a PDF Index and support for [CSS paged media module](https://drafts.csswg.org/css-page-3/).

## Requirements

1. This package requires MkDocs version 1.0 or higher (0.17 works as well)
2. Python ~3.4~ 3.5 or higher
3. WeasyPrint depends on cairo, Pango and GDK-PixBuf which need to be installed separately. Please follow the installation instructions for your platform carefully:
    - [Linux][weasyprint-linux]
    - [MacOS][weasyprint-macos]
    - [Windows][weasyprint-windows]
4. Explicit support for your mkdocs theme is probably required. As of now, the only supported theme is [mkdocs-material][mkdocs-material]. A generic version will just generate the PDF files and put the download link into a `<link>` tag.

If you want to add a new theme, see [adding support for new themes](#adding-support-for-new-themes) for more information.

## Installation

Install the package with pip:

```bash
pip install mkdocs-pdf-export-plugin
```

Enable the plugin in your `mkdocs.yml`:

```yaml
plugins:
    - search
    - pdf-export
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation][mkdocs-plugins].

## Testing

When building your repository with `mkdocs build`, you should now see the following message at the end of your build output:

> Converting 17 files to PDF took 15.6s

In your `site_dir` you should now have a PDF file for every markdown page.

## Options

You may customize the plugin by passing options in `mkdocs.yml`:

```yaml
plugins:
    - pdf-export:
        verbose: true
        media_type: print
        enabled_if_env: ENABLE_PDF_EXPORT
```

### `verbose`

Setting this to `true` will show all WeasyPrint debug messages during the build. Default is `false`.

### `media_type`

This option allows you to use a different CSS media type (or a custom one like `pdf-export`) for the PDF export. Default is `print`.

### `enabled_if_env`

Setting this option will enable the build only if there is an environment variable set to 1. This is useful to disable building the PDF files during development, since it can take a long time to export all files. Default is not set.

### `combined`

Setting this to `true` will combine all pages into a single PDF file. All download links will point to this file. Default is `false`.

### `combined_output_path`

This option allows you to use a different destination for the combined PDF file. Has no effect when `combined` is set to `false`. Default is `pdf/combined.pdf`.

### `theme_handler_path`

This option allows you to specify a custom theme handler module. This path must be **relative to your project root** (See example below). Default is not set.

`mkdocs.yml`:
```yaml
plugins:
    - pdf-export:
        theme_handler_path: theme-handler.py
```
```bash
project-root
├── theme-handler.py
├── docs
├── mkdocs.yml
├── site
.
.
```

## Adjusting the output

The resulting PDF can be customized easily by adding a custom stylesheet such as the following:

```
@page {
    size: a4 portrait;
    margin: 25mm 10mm 25mm 10mm;
    counter-increment: page;
    font-family: "Roboto","Helvetica Neue",Helvetica,Arial,sans-serif;
    white-space: pre;
    color: grey;
    @top-left {
        content: '© 2018 My Company';
    }
    @top-center {
        content: string(chapter);
    }
    @top-right {
        content: 'Page ' counter(page);
    }
}
```
For this to take effect, use the `extra_css` directive in mkdocs.yml, as described in the [MkDocs user guide][extra-css].

## Adding support for new themes

If you use a mkdocs theme which is currently not supported, check out the `themes/material.py` file and adjust it according to your requirements. You will have to implement two methods to support a theme:

1. `get_stylesheet` should return a CSS which gets applied to fix issues with weasyprint
2. `modify_html` should add a link to the PDF download before writing it to disk

If there is no explicit support for your theme, the generic version will just add a `<link>` tag in the head pointing to the generated PDF.

## Contributing

From reporting a bug to submitting a pull request: every contribution is appreciated and welcome. Report bugs, ask questions and request features using [Github issues][github-issues].
If you want to contribute to the code of this project, please read the [Contribution Guidelines][contributing].

## Special thanks

Special thanks go to [Stephan Hauser][shauser] for the original development of this plugin.

Special thanks go to [Lukas Geiter][lukasgeiter] for developing the [mkdocs-awesome-pages-plugin][awesome-pages-plugin] which was used as a base and for convincing [Stephan Hauser][shauser] to write a plugin for this.

[travis-status]: https://travis-ci.org/zhaoterryy/mkdocs-pdf-export-plugin.svg?branch=master
[travis-link]: https://travis-ci.org/zhaoterryy/mkdocs-pdf-export-plugin
[weasyprint-linux]: https://weasyprint.readthedocs.io/en/latest/install.html#linux
[weasyprint-macos]: https://weasyprint.readthedocs.io/en/latest/install.html#os-x
[weasyprint-windows]: https://weasyprint.readthedocs.io/en/latest/install.html#windows
[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[mkdocs-material]: https://github.com/squidfunk/mkdocs-material
[github-issues]: https://github.com/zhaoterryy/mkdocs-pdf-export-plugin/issues
[contributing]: CONTRIBUTING.md
[lukasgeiter]: https://github.com/lukasgeiter
[shauser]: https://github.com/shauser
[awesome-pages-plugin]: https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin
[extra-css]: https://www.mkdocs.org/user-guide/configuration/#extra_css
