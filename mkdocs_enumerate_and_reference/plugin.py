import re
from functools import partial
from os.path import relpath
from pathlib import Path

from mkdocs.config import config_options as c
from mkdocs.config.base import Config
from mkdocs.plugins import BasePlugin

from mkdocs_enumerate_and_reference.enumerate import (
    add_section_numbers,
    enumerate_navigation,
)
from mkdocs_enumerate_and_reference.reference import refactor_admonitions


class PluginConfig(Config):
    enumerate_sections = c.Choice(
        ("ignore", "simple", "cumulative"),
        default="cumulative",
    )
    enumerate_markdown = c.Type(bool, default=True)
    start_level = c.Type(int, default=1)
    enumerate_admonitions = c.Choice(
        ("ignore", "simple", "cumulative"),
        default="ignore",
    )
    reference = c.Type(bool, default=True)
    tags_paths = c.Type(dict, default={})
    tagged_adms = c.Type(dict, default={})
    sources = c.Type(dict, default={})


class EnumerateAndReference(BasePlugin[PluginConfig]):
    def on_nav(self, nav, **kwargs) -> None:
        # enumerate navigation sections
        if self.config.enumerate_sections != "ignore":
            enumerate_navigation(
                nav,
                self.config.enumerate_sections,
            )

        # collect all tags and save their page url in a dict
        for page in nav.pages:
            source = read_source(page)
            tag_ids = re.findall(r"@tag\((.+?)\)", source)
            self.config.tags_paths.update({"#" + k: page.url for k in tag_ids})

    def on_page_markdown(self, markdown, page, config, **kwargs):
        # retrieve page specific enumerate markdown params or defaut if None
        enumerate_markdown, start_level = self.get_enumerate_markdown_params(
            page.meta,
        )
        # refactor markdow to add enumeration
        if enumerate_markdown:
            markdown = add_section_numbers(markdown, lowest_level=start_level)

        # enumerate admonitions params
        if self.config.enumerate_admonitions == "cumulative" and hasattr(
            page,
            "cnumber",
        ):
            cnumber = page.cnumber
        else:
            cnumber = None
        counter = None if self.config.enumerate_admonitions == "ignore" else 1

        # refactor adminition titles with numbering and tags
        markdown = refactor_admonitions(markdown, cnumber, counter)
        span = r'<span id="\1"></span>'
        markdown = re.sub(r"(?<!-)@tag\((.+?)\)", span, markdown)
        return re.sub(r"-(@tag\(.+?\))", r"\1", markdown)

    def get_enumerate_markdown_params(self, meta: dict):
        try:
            enumerate_markdown = meta["enumerate-and-reference"][
                "enumerate_markdown"
            ]
        except KeyError:
            enumerate_markdown = self.config.enumerate_markdown
        try:
            start_level = meta["enumerate-and-reference"]["start_level"]
        except KeyError:
            start_level = self.config.start_level

        return enumerate_markdown, start_level

    def on_page_read_source(self, page, **kwargs):
        try:
            # Only navigation sources read on nav
            source = self.config.sources[page.file.src_path]
        except KeyError:
            source = None
        return source

    def on_page_content(self, html, page, **kwargs):
        rel_tr = partial(transform, self.config.tags_paths, page.url)

        def on_match(m) -> str:
            tag_id = m.group(1)
            return f'<a href="{rel_tr(tag_id)}">'

        return re.sub('<a href="(.+?)">', on_match, html)


def read_source(page):
    try:
        with Path.open(
            page.file.abs_src_path,
            encoding="utf-8-sig",
            errors="strict",
        ) as f:
            source = f.read()
    except OSError as exc:
        msg = f"File not found: {page.file.src_path}"
        raise OSError(msg) from exc
    except ValueError as exc:
        msg = f"Encoding error reading file: {page.file.src_path}"
        raise ValueError(msg) from exc
    return source


def transform(tags_paths: dict, url: str, tag_id: str):
    """Create the link to the referenced tag.

    Create the relative path between url of page containing the reference
    and page containing the tag then add the tag to that relative path
    """
    if tag_id in tags_paths:
        rel_path = relpath(tags_paths[tag_id], url)
        return f"{rel_path}/{tag_id}"
    return tag_id


if __name__ == "__main__":
    from mkdocs.commands.serve import serve

    serve("docs/mkdocs.yml")
