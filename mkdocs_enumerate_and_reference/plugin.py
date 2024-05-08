from mkdocs.config import config_options as c
from mkdocs.config.base import Config
from mkdocs.plugins import BasePlugin
from mkdocs_enumerate_and_reference.enumerate import enumerate_navigation, add_section_numbers
from mkdocs_enumerate_and_reference.reference import refactor_admonitions
import re
from os.path import relpath
from functools import partial

class PluginConfig(Config):
    
    enumerate = c.Type(bool, default=True)
    cumulative = c.Type(bool, default=True)
    number_page_sections = c.Type(bool, default=True)
    start_level = c.Type(int, default=1)
    
    reference = c.Type(bool, default=True)
    tags_paths = c.Type(dict, default=dict())
    tagged_adms = c.Type(dict, default=dict())
    sources = c.Type(dict, default=dict())

class EnumerateAndReference(BasePlugin[PluginConfig]):
    def on_nav(self, nav, **kwargs):
        if self.config.enumerate:   
            enumerate_navigation(nav, self.config.cumulative)
        for page in nav.pages:
            source = read_source(page)
            tag_ids = re.findall(r'@tag\((.+?)\)', source)
            self.config.tags_paths.update({k: page.url for k in tag_ids})
            # next line is to prevent reading source twice
            # config.sources.update({page.file.src_path: source})
    
    def on_page_markdown(self, markdown, page, config,  **kwargs):
        number_page_sections, start_level = self.get_number_headings_params(page.meta)
        if number_page_sections:
            markdown = add_section_numbers(markdown, lowest_level=start_level)

        cnumber = page.cnumber if hasattr(page, "cnumber") else None
        markdown = refactor_admonitions(markdown, cnumber)
        span = r'<span id="\1"></span>'
        markdown = re.sub(r'(?<!-)@tag\((.+?)\)', span, markdown)
        return re.sub(r'-(@tag\(.+?\))', r'\1', markdown)

    def get_number_headings_params(self, meta: dict):
        try:
            number_page_sections = meta["enumerate-and-reference"]["number_page_sections"]
        except KeyError:
            number_page_sections = self.config.number_page_sections

        try:
            start_level = meta["enumerate-and-reference"]["start_level"]
        except KeyError:
            start_level = self.config.start_level

        return number_page_sections, start_level

    def on_page_read_source(self, page, **kwargs):
        try:
            # Only navigation sources read on nav
            source = self.config.sources[page.file.src_path]
        except KeyError:
            source = None
        return source
    
    def on_page_content(self, html, page, **kwargs):
        rel_tr = partial(transform, self.config.tags_paths, page.url)

        def on_match(m):
            tag_id = m.group(1)
            return f'<a href="{rel_tr(tag_id)}">'
        return re.sub('<a href="(.+?)">', on_match, html)

def read_source(page):
    try:
        with open(page.file.abs_src_path, encoding='utf-8-sig', errors='strict') as f:
            source = f.read()
    except OSError:
        raise OSError(f'File not found: {page.file.src_path}')
    except ValueError:
        raise ValueError(f'Encoding error reading file: {page.file.src_path}')
    return source

def transform(tags_paths: dict, url: str, tag_id: str):
    """Create the link to the referenced tag

    Create the relative path between url of page containing the reference
    and page containing the tag then add the tag to that relative path
    """
    if tag_id in tags_paths:
        rel_path = relpath(tags_paths[tag_id], url)
        r = f"{rel_path}/#{tag_id}"
        return f"{rel_path}/#{tag_id}"
    else:
        return tag_id

if __name__ == "__main__":
    from mkdocs.commands.serve import serve
    serve("docs/mkdocs.yml")