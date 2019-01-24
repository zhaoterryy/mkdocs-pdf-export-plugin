import os

from weasyprint import urls
from bs4 import BeautifulSoup

def get_rel_pdf_href(combined: bool, href: str):
    head, tail = os.path.split(href)
    filename, ext = tuple(os.path.splitext(tail))

    absurl = urls.url_is_absolute(href)
    abspath = os.path.isabs(href)
    internal = href.startswith('#')
    htmlfile = ext.startswith('.html')
    if absurl or abspath or internal or not htmlfile:
        return href

    return urls.iri_to_uri(os.path.join(head, filename + '.pdf'))

def get_abs_asset_href(base_url: str, href: str):
    if urls.url_is_absolute(href) or os.path.isabs(href):
        return href

    return urls.iri_to_uri(urls.urljoin(base_url, href))

def replace_hrefs(soup: BeautifulSoup, base_url: str, combined: bool):
    # transforms all relative hrefs pointing to other html docs
    # into relative pdf hrefs
    for a in soup.find_all('a'):
        try:
            a['href'] = get_rel_pdf_href(combined, a['href'])
        except KeyError:
            pass

    # makes all relative asset links absolute
    for link in soup.find_all('link'):
        try:
            link['href'] = get_abs_asset_href(base_url, link['href'])
        except KeyError:
            pass

    return soup