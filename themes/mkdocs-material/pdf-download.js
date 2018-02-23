document.addEventListener('DOMContentLoaded', function () {
    var link = document.querySelector('link[rel=alternate][type="application/pdf"]');
    if (link) {
        // Add a download button (the following code works for the mkdocs-material theme):
        var article = document.getElementsByTagName('article')[0];

        var element = document.createElement('a');
        element.setAttribute('href', link.href);
        element.setAttribute('class', 'md-icon md-content__icon');
        element.setAttribute('title', 'Download as PDF');
        element.setAttribute('download', '');
        element.innerHTML = '&#xE2C4;';

        article.insertBefore(element, article.children[0]);
    }
});
