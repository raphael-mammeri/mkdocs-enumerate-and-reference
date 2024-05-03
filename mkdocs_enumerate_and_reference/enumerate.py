import re

def cumulative_number(item):
    anc_numbers = []
    for a in item.ancestors:
        if hasattr(a, "number"):
            anc_numbers.append(a.number)
    anc_numbers.append(item.number)
    cnumber = ".".join(anc_numbers)
    item.cnumber = cnumber
    return cnumber


def enumerate_navigation(nav, cumulative: bool=True):
    for i, item in enumerate(nav.items):
        item.number = str(i+1)
        if item.title is not None:
            item.title = ". ".join([item.number, item.title])
        enumerate_children(item, cumulative)


def enumerate_children(item, cumulative: bool):
    if item.children is not None: 
        for i, child in enumerate(item.children):
            number = str(i+1)
            child.number = number
            if cumulative:
                number = cumulative_number(child)
            if child.title is not None:
                child.title = " - ".join([number, child.title])
            enumerate_children(child, cumulative)

def add_section_numbers(markdown, lowest_level: int=1):
    # Initialize section numbers for each level
    section_number = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    # Define a function to replace each heading match with its numbered version
    def replace_heading(match):
        level = len(match.group(1))
        title = match.group(2)

        # Restart subsection numbering when a new section starts
        for i in range(level + 1, 7):
            section_number[i] = 0

        # Increment section number for the current level
        section_number[level] += 1

        # Add a dot at the end of the numbers for all sections and subsections
        title_number = ".".join([str(section_number[i]) for i in range(lowest_level, level + 1)])
        numbered_title = f"{title_number}. {title}" if len(title_number) else title

        return f"{'#' * level} {numbered_title}\n"

    # Define the regex pattern for detecting headings
    heading_pattern = re.compile(r'^(\#{1,6})\s+(.+?)\s*$', re.MULTILINE)

    # Increment section numbers and replace headings
    numbered_markdown = heading_pattern.sub(replace_heading, markdown)

    return numbered_markdown