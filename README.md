# MkDocs PDF Export Plugin [![Build Status][travis-status]][travis-link]

*An MkDocs plugin to export content pages as PDF files*

The pdf-export plugin will export all markdown pages in your MkDocs repository as PDF files using [WeasyPrint](http://weasyprint.org/). The exported documents support many advanced features missing in most other PDF exports, such as a PDF Index and support for [CSS paged media module](https://drafts.csswg.org/css-page-3/).

## Before you start

Setting this up is not easy. If you're running Windows or MacOS, it will require you to install third-party software on your system. Getting it to work perfectly also requires some customization of your mkdocs setup (extra stylesheet and javascript).

After testing many different solutions to export PDFs from MkDocs, this has been the only one that fulfilled all expected features from a PDF export:

- PDF index for quick navigation
- Working hyperlinks (except for inter-page links)
- Decent page break handling (no section title on page 1 and contents on page 2)

## Installation

> **Note:** This package requires MkDocs version 0.17 or higher.

WeasyPrint depends on cairo, Pango and GDK-PixBuf which need to be installed separately. Please follow the installation instructions for your platform carefully:

- [Linux][weasyprint-linux]
- [MacOS][weasyprint-macos]
- [Windows][weasyprint-windows]

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

## Install theme support

Depending on the mkdocs theme you use, you might need to add some support files for this plugin. See [adding support for new themes](#adding-support-for-new-themes) for more information.

### mkdocs-material

If you are using the [mkdocs-material theme][mkdocs-material], you'll need to add the following two files to your mkdocs project:

- [`docs/assets/stylesheets/weasyprint.css`](themes/mkdocs-material/weasyprint.css)
- [`docs/assets/javascripts/pdf-download.js`](themes/mkdocs-material/pdf-download.js)

Reference them from your `mkdocs.yml` file so they are included in the build output:

```yaml
extra_css:
    - assets/stylesheets/weasyprint.css
extra_javascript:
    - assets/javascripts/pdf-download.js
```

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

## Adding support for new themes

It is possible that WeasyPrint will not perfectly export the PDF initially. Depending on the theme you're using, there might be issues such as wrong text rendering or even missing pages. These issues are normally caused by combinations of CSS attributes not handled perfectly by WeasyPrint.

It's normally easiest to fix these issues by providing an additional stylesheet which gets applied for the print medium.

Since the plugin does not have any knowledge about how your theme works, it will only generate the PDF and add a `<link rel="alternate" href="filename.pdf" type="application/pdf" title="PDF Export">` element to the HTML before writing it to disk. To add a download link to your page, you'll need to add it to the page while loading.

Please see one of the existing themes on examples of how to do this.

## Contributing

From reporting a bug to submitting a pull request: every contribution is appreciated and welcome. Report bugs, ask questions and request features using [Github issues][github-issues].
If you want to contribute to the code of this project, please read the [Contribution Guidelines][contributing].

## Special thanks

Special thanks go to [Lukas Geiter][lukasgeiter] for developing the [mkdocs-awesome-pages-plugin][awesome-pages-plugin] which I could use as a base and for convincing me to write a plugin for this.

[travis-status]: https://travis-ci.org/shauser/mkdocs-pdf-export-plugin.svg?branch=master
[travis-link]: https://travis-ci.org/shauser/mkdocs-pdf-export-plugin
[weasyprint-linux]: https://weasyprint.readthedocs.io/en/latest/install.html#linux
[weasyprint-macos]: https://weasyprint.readthedocs.io/en/latest/install.html#os-x
[weasyprint-windows]: https://weasyprint.readthedocs.io/en/latest/install.html#windows
[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[mkdocs-material]: https://github.com/squidfunk/mkdocs-material
[github-issues]: https://github.com/shauser/mkdocs-pdf-export-plugin/issues
[contributing]: CONTRIBUTING.md
[lukasgeiter]: https://github.com/lukasgeiter
[awesome-pages-plugin]: https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin
