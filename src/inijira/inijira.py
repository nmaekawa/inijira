# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


def is_author_class(tag):
    return tag.has_attr("class") and tag["class"] == "author"


def convert(html_doc):
    soup = BeautifulSoup(html_doc, "lxml")

    result = {}

    # get description from title
    title = soup.title.string
    if " - " not in title:
        return result

    (_, description) = title.split(" - ", 1)

    # get author
    """
    metadata = soup.find_all(
            'div',
            attrs={'class': 'page-metadata'}
    )
    """
    metadata = soup.find_all(class_="page-metadata")
    author_tag = metadata[0].contents
    author = author_tag[1].contents[0].strip()
    has_last_modified = metadata[0].contents[-1].strip().strip("\n")
    last_modified = has_last_modified.split("on ")[1].strip()

    # get why, who, when, what
    why = who = when = what = None
    main = soup.find_all(id="main-content")
    main_h1 = main[0].find_all("h1")
    for child in main_h1:
        if child.string == "why":
            why = child.next_sibling
        elif child.string == "who":
            who = child.next_sibling
        elif child.string == "when":
            when = child.next_sibling
        elif child.string == "what":
            what = child.next_sibling
        else:
            continue

    result["description"] = description.strip()
    result["author"] = author
    result["last_modified"] = last_modified

    result["why"] = why
    result["who"] = who
    result["when"] = when
    result["what"] = what
    result["main"] = main

    return result
