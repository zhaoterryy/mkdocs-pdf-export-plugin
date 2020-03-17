#!/usr/bin/env python

from mkdocs_pdf_export_plugin.preprocessor.links.transform import transform_href


def test_transform_href():
    assert transform_href("#a/b/:test", "a/b/") == "#a/b/:test"

    # 1. href do not contain directory
    # 1.1 rel_url is directory
    assert transform_href("#test", "a/b/") == "#a/b/:test"
    assert transform_href("section#test", "a/b/") == "#a/b/section:test"
    assert transform_href("section.md#test", "a/b/") == "#a/b/section:test"
    assert transform_href("section.abc.md#test",
                          "a/b/") == "#a/b/section.abc:test"

    # 1.2 rel_url has section part
    assert transform_href("#test", "a/b/c") == "#a/b/c:test"
    # may conflic?
    # assert transform_href("section#test", "a/b/c") == "#a/b/section:test"

    # 2. href has directory
    assert transform_href("c/#test", "a/b/") == "#a/b/c/:test"
    assert transform_href("c/section#test", "a/b/") == "#a/b/c/section:test"
    assert transform_href("../c/section#test", "a/b/") == "#a/c/section:test"
    assert transform_href("../../c/section#test", "a/b/") == "#c/section:test"
    assert transform_href("../../../c/section#test",
                          "a/b/") == "#../c/section:test"

    # is a file
    # assert transform_href("section", "a/b/") == "#a/b/section"
    # assert transform_href("c/", "a/b/") == "#a/b/c/"
    assert transform_href("c.svg", "a/b/") == "c.svg"
    assert transform_href("c.html", "a/b/") == "#a/b/c.html:"

    # test for #70
    assert transform_href("index.md#4.-New-Section",
                          "a/b/") == "#a/b/index:4.-New-Section"

    # test footnotes
    assert transform_href("index.md#fn:1", "a/b/") == "#a/b/index:fn:1"
    assert transform_href("index.md#fnref:@#$%",
                          "a/b/") == "#a/b/index:fnref:@#$%"
    assert transform_href("#fnref:@#$%", "a/b/") == "#a/b/:fnref:@#$%"
