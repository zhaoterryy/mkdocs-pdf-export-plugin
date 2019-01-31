# MkDocs PDF Export Plugin <span class="noprint">[![Build Status](https://travis-ci.org/zhaoterryy/mkdocs-pdf-export-plugin.svg?branch=master)](https://travis-ci.org/zhaoterryy/mkdocs-pdf-export-plugin)</span>

The pdf-export plugin will export all markdown pages in your MkDocs repository as PDF files using [WeasyPrint](http://weasyprint.org/). The exported documents support many advanced features missing in most other PDF exports, such as a PDF Index and support for [CSS paged media module](https://developer.mozilla.org/en-US/docs/Web/CSS/@page).

- MkDocs >= 1.0
- Python >= 3.4
- WeasyPrint >= 44

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

More information about plugins in the [MkDocs documentation](http://www.mkdocs.org/user-guide/plugins/).

## Contributing

From reporting a bug to submitting a pull request: every contribution is appreciated and welcome. Report bugs, ask questions and request features using [Github issues][github-issues].

If you want to contribute to the code of this project, please read the [Contribution Guidelines][contributing].

#### **Special thanks**

Special thanks go to [Stephan Hauser][shauser] for the original development of this plugin.

Special thanks go to [Lukas Geiter][lukasgeiter] for developing the [mkdocs-awesome-pages-plugin][awesome-pages-plugin] which was used as a base and for convincing [Stephan Hauser][shauser] to write a plugin for this.

[github-issues]: https://github.com/zhaoterryy/mkdocs-pdf-export-plugin/issues
[contributing]: https://github.com/zhaoterryy/mkdocs-pdf-export-plugin/blob/master/CONTRIBUTING.md
[lukasgeiter]: https://github.com/lukasgeiter
[shauser]: https://github.com/shauser
[awesome-pages-plugin]: https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin