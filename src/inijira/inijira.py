# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

components = [
    "catch-legacy",
    "catchpy",
    "devops",
    "fake",
    "fnup",
    "hxarc",
    "hxat",
    "hxighlighter",
    "hximg",
    "hxydra",
    "socializeremotely",
    "threads",
    "www2",
]
user_map = {
    "Naomi Maekawa": "nam363",
    "Mr Luis Francisco Duarte": "lfd776",
}


def is_author_class(tag):
    return tag.has_attr("class") and tag["class"] == "author"


def is_attachment_link(href):
    # return href and re.compile("attachments").search(href)
    return href and href.startswith("attachments")


def is_incident_reference(href):
    return href and href.startswith("20")


def toticket(html_doc):
    soup = BeautifulSoup(html_doc, "lxml")

    result = {}

    # get description from title
    title = soup.title.string
    if " - " not in title or " : " not in title:
        return result

    (_, description) = title.split(" : ", 1)
    if not description:
        return result

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

    # get why, who, when, what, etc
    main = soup.find_all(id="main-content")
    main_h1 = main[0].find_all("h1")
    for child in main_h1:
        result[child.string] = child.next_sibling

    # fix who
    result["who"] = "lfd776" if "lduarte" in main[0].get_text() else "nam363"

    # make a attachment list
    main_attachments = soup.find_all(href=is_attachment_link)

    # make a reference list
    main_references = main[0].find_all(href=is_incident_reference)

    # guess the component
    result["component"] = "na"
    for c in components:
        if c in description:
            result["component"] = c

    result["description"] = description.strip()
    result["author"] = user_map.get(author, "na")
    result["last_modified"] = last_modified
    result["main"] = main[0].get_text()
    result["attachments"] = main_attachments
    result["references"] = main_references

    return result


def tocsv(tickets, separator="\t"):
    result = separator.join(
        [
            "component",
            "reporter",
            "assignee",
            "description",
            "\n",
        ]
    )
    for t in tickets:
        line = separator.join(
            [
                t["component"],
                t["author"],
                t["who"],
                t["description"],
                "\n",
            ]
        )
        result += line
    return result
