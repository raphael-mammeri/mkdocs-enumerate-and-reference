from __future__ import annotations

import pytest
from mkdocs.structure.files import get_files
from mkdocs.structure.nav import get_navigation


@pytest.mark.parametrize(
    ("enum_param", "page_titles", "section_titles"),
    [
        (
            "cumulative",
            [
                "1. Home",
                "2.1.1 - section one",
                "2.1.2 - section two",
                "2.2.1 - section one",
                "2.2.2 - section two",
            ],
            ["1. Home", "2. demo"],
        ),
        (
            "simple",
            [
                "1. Home",
                "1 - section one",
                "2 - section two",
                "1 - section one",
                "2 - section two",
            ],
            ["1. Home", "2. demo"],
        ),
        (
            "ignore",
            [
                "Home",
                "section one",
                "section two",
                "section one",
                "section two",
            ],
            ["Home", "demo"],
        ),
    ],
)
def test_enumerate(config, enum_param, page_titles, section_titles):
    plugin = config.get("plugins").get("enumerate-and-reference")
    plugin.config["enumerate_sections"] = enum_param
    files = get_files(config)
    nav = get_navigation(files, config)
    plugin.on_nav(nav)
    assert [page.title for page in nav.pages] == page_titles
    assert [x.title for x in nav] == section_titles
