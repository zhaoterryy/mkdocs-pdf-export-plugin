import os

from weasyprint import urls
from bs4 import BeautifulSoup

def rel_pdf_href(href: str):
    head, tail = os.path.split(href)
    filename, ext = tuple(os.path.splitext(tail))

    absurl = urls.url_is_absolute(href)
    abspath = os.path.isabs(href)
    internal = href.startswith('#')
    htmlfile = ext.startswith('.html')
    if absurl or abspath or internal or not htmlfile:
        return href

    return urls.iri_to_uri(os.path.join(head, filename + '.pdf'))

def abs_asset_href(href: str, base_url: str):
    if urls.url_is_absolute(href) or os.path.isabs(href):
        return href

    return urls.iri_to_uri(urls.urljoin(base_url, href))

# makes all relative asset links absolute
def replace_asset_hrefs(soup: BeautifulSoup, base_url: str):
    for link in soup.find_all('link', href=True):
        link['href'] = abs_asset_href(link['href'], base_url)

    for asset in soup.find_all(src=True):
        asset['src'] = abs_asset_href(asset['src'], base_url)
    
    return soup

# normalize href to #foo/bar/section:id
def normalized_href(href: str, rel_url: str):
    head, tail = os.path.split(href)

    num_hashtags = tail.count('#')
    if num_hashtags is 0:
        return href
    elif num_hashtags > 1:
        raise RuntimeError('Why are there so many hashtags in {}!?!?'.format(href))

    if tail.startswith('#'):
        head, section = os.path.split(rel_url)
        section = os.path.splitext(section)[0]
        id = tail[1:]
    else:
        section, ext = tuple(os.path.splitext(tail))
        id = str.split(ext, '#')[1]

    return '#{}/{}:{}'.format(head, section, id)

# normalize id to foo/bar/section:id
def normalized_id(id: str, rel_url: str):
    if ':' in id or '/' in id:
        print('":" and "/" characters are banned! /:')
        raise RuntimeError('Invalid ID found in {}, ID: {}'.format(rel_url, id))

    head, tail = os.path.split(rel_url)
    section, _ = tuple(os.path.splitext(tail))

    return '{}/{}:{}'.format(head, section, id)

def prep_combined(soup: BeautifulSoup, base_url: str, rel_url: str):
    for id in soup.find_all(id=True):
        id['id'] = normalized_id(id['id'], rel_url)

    for a in soup.find_all('a', href=True):
        if urls.url_is_absolute(a['href']) or os.path.isabs(a['href']):
            continue

        a['href'] = normalized_href(a['href'], rel_url)

    soup = replace_asset_hrefs(soup, base_url)
    return soup

def replace_hrefs(soup: BeautifulSoup, base_url: str):
    # transforms all relative hrefs pointing to other html docs
    # into relative pdf hrefs
    for a in soup.find_all('a', href=True):
        a['href'] = rel_pdf_href(a['href'])

    soup = replace_asset_hrefs(soup, base_url)
    return soup