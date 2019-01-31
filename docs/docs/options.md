# Options

Pass in options through `mkdocs.yml`:

```yaml
plugins:
    - pdf-export:
        verbose: true
        media_type: print
        enabled_if_env: ENABLE_PDF_EXPORT
```

### `verbose`

<small>*default: false*</small>

Setting this to `true` will show all WeasyPrint debug messages during the build.

### `media_type` 

<small>*default: print*</small>

This option allows you to use a different CSS media type (or a custom one like `pdf-export`) for the PDF export.

### `enabled_if_env`

<small>*default: not set*</small>

Setting this option will enable the build only if there is an environment variable set to 1. This is useful to disable building the PDF files during development, since it can take a long time to export all files.

### `combined` 

<small>*default: false*</small>

Setting this to `true` will combine all pages into a single PDF file. All download links will point to this file.

### `combined_output_path` 

<small>*default: pdf/combined.pdf*</small>

This option allows you to use a different destination for the combined PDF file. Has no effect when `combined` is set to `false`.

### `theme_handler_path`

<small>*default: not set*</small>

This option allows you to specify a custom theme handler module. This path must be ***relative to your project root*** (See example below).

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