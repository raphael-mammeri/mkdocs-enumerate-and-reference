from __future__ import annotations

import re


def transform(token, name: str, counter, title=None, tag=None) -> str:
    if global_cnumber is not None:
        counter = ".".join([global_cnumber, str(counter)])
    if counter is not None:
        full_title = f"{name.capitalize()} {counter}"
    else:
        full_title = f"{name.capitalize()}"
    if title is not None and len(title):
        full_title = " ".join([full_title, f"({title})"])
    if tag is not None:
        full_title = " ".join([full_title, f"@tag({tag})"])
    return f'{token} {name} "{full_title}"'


counter = 1
global_cnumber = None


def on_match(m):
    global counter
    # admonition has the group 0
    token = m.group(2)
    name = m.group(3)
    title = m.group(5)
    tag = m.group(7)
    new_admonition = transform(token, name, counter, title, tag)
    if counter is not None:
        counter += 1
    return new_admonition


def refactor_admonitions(
    markdown,
    cnumber: str | None = None,
    ncounter=None,
):
    pattern = r'( *(!!!\+?|\?{3}\+?) *(\w+) *("(.*)")? *(@tag\((.+)\))?)'
    global counter
    counter = ncounter
    global global_cnumber
    global_cnumber = cnumber
    return re.sub(pattern, on_match, markdown)
