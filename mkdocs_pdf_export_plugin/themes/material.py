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
    
    .md-typeset a.footnote-backref {
        transform: translateX(0);
        opacity: 1;
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

    # SVG 'file-download' size 2x from fontawesome: https://fontawesome.com/icons/file-download?style=solid
    # resized to 1.2rem width * height
    a_tag = "<a class=\"md-content__button md-icon\" download href=\"%s\" title=\"PDF Export\">" % href
    icon = '<svg style="height: 1.2rem; width: 1.2rem;" viewBox="0 0 384 512" xmlns="http://www.w3.org/2000/svg"><path d="M224 136V0H24C10.7 0 0 10.7 0 24v464c0 13.3 10.7 24 24 24h336c13.3 0 24-10.7 24-24V160H248c-13.2 0-24-10.8-24-24zm76.45 211.36l-96.42 95.7c-6.65 6.61-17.39 6.61-24.04 0l-96.42-95.7C73.42 337.29 80.54 320 94.82 320H160v-80c0-8.84 7.16-16 16-16h32c8.84 0 16 7.16 16 16v80h65.18c14.28 0 21.4 17.29 11.27 27.36zM377 105L279.1 7c-4.5-4.5-10.6-7-17-7H256v128h128v-6.1c0-6.3-2.5-12.4-7-16.9z"></path></svg>'
    button_tag = a_tag + icon + "</a>"

    # insert into HTML
    insert_point = "<article class=\"md-content__inner md-typeset\">"
    html = html.replace(insert_point, insert_point + button_tag)
    
    return html

