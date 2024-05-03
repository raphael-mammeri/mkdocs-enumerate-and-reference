---
title: My Document
summary: A brief description of my document.
authors:
    - Waylan Limberg
    - Tom Christie
date: 2018-07-10
some_url: https://example.com
---

The **Mkdcos Enumerate and Reference Plugin** is a tool designed to enhance your documentation by providing advanced numbering options and simplifying cross-references between pages.

## How it works
The plugin search for references in the complete documentation to create the links to the appropriate tags then transforms the tag ID with corresponding link.

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

