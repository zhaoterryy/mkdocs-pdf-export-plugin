from bs4 import BeautifulSoup


def get_stylesheet() -> str:
    return """
    h1, h2, h3 {
         string-set: chapter content();
    }
    
    .md-container {
        display: block;
        padding-top: 0;
    }
    
    .md-main {
        display: block;
        height: inherit;
    }
    
    .md-main__inner {
        height: inherit;
        padding-top: 0;
    }
    
    .md-typeset .codehilitetable .linenos {
        display: none;
    }
    
    .md-typeset .footnote-ref {
        display: inline-block;
    }
    
    .md-typeset .admonition {
        display: block;
        border-top: .1rem solid rgba(0,0,0,.07);
        border-right: .1rem solid rgba(0,0,0,.07);
        border-bottom: .1rem solid rgba(0,0,0,.07);
        page-break-inside: avoid;
    }
    
    .md-typeset a::after {
        color: inherit;
        content: none;
    }
    
    .md-typeset table:not([class]) th {
        min-width: 0;
    }
    
    .md-typeset table {
        border: .1rem solid rgba(0,0,0,.07);
    }
    """


def modify_html(html: str, href: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.new_tag('a', href=href, title='PDF Export', download=None)
    a['class'] = 'md-icon md-content__icon'
    a.string = '\uE2C4'
    soup.article.insert(0, a)

    return str(soup)
