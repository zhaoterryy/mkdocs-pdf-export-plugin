from bs4 import BeautifulSoup


def get_stylesheet() -> str:
    return None


def modify_html(html: str, href: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    if soup.head:
        link = soup.new_tag('link', href=href, rel='alternate', title='PDF Export', type='application/pdf')
        soup.head.append(link)

    return str(soup)
