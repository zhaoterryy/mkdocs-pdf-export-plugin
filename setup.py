from setuptools import setup, find_packages


setup(
    name='mkdocs-pdf-export-plugin',
    version='0.5.10',
    description='An MkDocs plugin to export content pages as PDF files',
    long_description='The pdf-export plugin will export all markdown pages in your MkDocs repository as PDF files'
                     'using WeasyPrint. The exported documents support many advanced features missing in most other'
                     'PDF exports, such as a PDF Index and support for CSS paged media module.',
    keywords='mkdocs pdf export weasyprint',
    url='https://github.com/zhaoterryy/mkdocs-pdf-export-plugin/',
    author='Terry Zhao',
    author_email='zhao.terryy@gmail.com',
    license='MIT',
    python_requires='>=3.5',
    install_requires=[
        'mkdocs>=0.17',
        'weasyprint>=0.44',
        'beautifulsoup4>=4.6.3'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'pdf-export = mkdocs_pdf_export_plugin.plugin:PdfExportPlugin'
        ]
    }
)
