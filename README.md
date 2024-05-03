![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-enumerate-and-reference)
![PyPI](https://img.shields.io/pypi/v/mkdocs-enumerate-and-reference)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mkdocs-enumerate-and-reference)
![GitHub contributors](https://img.shields.io/github/contributors/raphael-mammeri/mkdocs-enumerate-and-reference)
![PyPI - License](https://img.shields.io/pypi/l/mkdocs-enumerate-and-reference)

# Mkdocs Plugin for Enhanced Referencing and Enumeration
An [Mkdocs](https://www.mkdocs.org) plugin for referencing within documentation, section numbering, and page heading numbering.

## Features
1. Referencing: This is the main feature of the plugin. Using a tag system, it allows referencing specific points on pages without having to specify the page path.
2. Navigation numbering: navigation sections are automatically numbered
3. Admonition numbering: numbering of (selected) admonitions accross documentation

## How it works
The plugin search for references in the complete documentation to create the links to the appropriate tags then transforms the tag ID with corresponding link.
* Sections enumeration does not work on first level sections
* May be there's an issue if a page is used in multiple places
* In navigation there need to be a section title, if only page provided : - page.md instead of : - subsection: page.md it will not work
## Installation

``` bash
pip install mkdocs-enumerate-and-reference
```
Enable the pluggin

```yaml
plugins:
  - enumerate-and-reference
```

## Example
```yaml
plugins:
  - enumerate-and-reference:
      enumerate:
        enabled: true
        cumulative: true
      number_headings:
        enabled: true
        activated: true
        lowest_level: 2
```

## Parameters
The plugin is composed of two parts that can be either be used or not seprately: the `enumerate` and the `number_headings` part.
