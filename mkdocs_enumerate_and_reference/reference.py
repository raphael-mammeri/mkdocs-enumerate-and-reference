import re

def transform(token, name: str, counter, title=None, tag=None):
    if global_cnumber is not None:
        counter = ".".join([global_cnumber, str(counter)])
    full_title = f"{name.capitalize()} {counter}"
    if title is not None and len(title):
        full_title = " ".join([full_title, f"({title})"])
    if tag is not None:
        full_title = " ".join([full_title, f"@tag({tag})"])
    return f'{token} {name} "{full_title} :"'

counter = 1
global_cnumber = None
def on_match(m):
    global counter
    admonition = m.group(0)
    token = m.group(2)
    name = m.group(3)
    title = m.group(5)
    tag = m.group(7)
    #print(f"{m.group(0)} --- {m.group(2)} --- {m.group(3)} --- {m.group(5)}--- {m.group(7)} --- \n ")
    if True:
        new_admonition = transform(token, name, counter, title, tag)
        counter += 1
        return new_admonition
    else:
        return admonition

def refactor_admonitions(markdown, cnumber: str = None):
    pattern = r'( *(!!!\+?|\?{3}\+?) *(\w+) *("(.*)")? *(@tag\((.+)\))?)'
    global counter
    counter = 1
    global global_cnumber
    global_cnumber = cnumber
    #rel_tr = partial(transform, config.tags_paths, page.url)

    return re.sub(pattern, on_match, markdown)