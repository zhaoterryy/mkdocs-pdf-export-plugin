import os

from .links import transform_href, transform_id, get_body_id, replace_asset_hrefs, rel_pdf_href

from weasyprint import urls
from bs4 import BeautifulSoup

def get_combined(soup: BeautifulSoup, base_url: str, rel_url: str, output_dir: str):

    # the relative URL base is the incoming rel_url with the extension and trailing slash stripped off.
    if rel_url.count('.') is 1:
        rel_url_base, _ = rel_url.split('.')
    else:
        rel_url_base = rel_url
    rel_url_base = rel_url_base.strip('/')

    # Only process links and headings that are inside the article tag
    for article in soup.find_all('article'):

        # If the permalink plugin is active, headings will contain extra useless links. Delete these.
        for headerlink in article.find_all('a', {'class':'headerlink'}):
            headerlink.decompose()

        # Process H1 elements. There *should* be only one of these per page, but process any that are found.
        # Format for H1 IDs is "path/to/page:" with a trailing colon.
        for title in article.find_all('h1'):
            title['id'] = '{}:'.format(rel_url_base)
            print('[pdf export] Processing page: "{}"'.format(title.string))

        # process H2-6 elements. 
        # Format for H2-6 IDs is "path/to/page:subhead-id".
        for heading in article.find_all(['h2','h3','h4','h5','h6']):
            heading['id'] = '{}:{}'.format(rel_url_base, heading.get('id'))

        # process body (article) link hrefs.
        for a in article.find_all('a', href=True):
            if urls.url_is_absolute(a['href']) or os.path.isabs(a['href']):
                continue

            a['href'] = transform_href(a['href'], rel_url_base, base_url, output_dir)

    soup.body['id'] = get_body_id(rel_url)
    soup = replace_asset_hrefs(soup, base_url)
    return soup

def get_separate(soup: BeautifulSoup, base_url: str):
    # transforms all relative hrefs pointing to other html docs
    # into relative pdf hrefs
    for a in soup.find_all('a', href=True):
        a['href'] = rel_pdf_href(a['href'])

    soup = replace_asset_hrefs(soup, base_url)
    return soup