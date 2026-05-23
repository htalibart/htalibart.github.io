import sys
import os
from pathlib import Path
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

MAIN_DIR = Path(os.path.realpath(__file__)).parent.parent

def format_authors(authors_str, my_name="Talibart, Hugo"):
    authors = [a.strip() for a in authors_str.split(" and ")]
    formatted = []
    for author in authors:
        if "," in author:
            last, first = author.split(",", 1)
            name = f"{first.strip()} {last.strip()}"
        else:
            name = author
        if author == my_name:
            formatted.append(f"<strong>{name}</strong>")
        else:
            formatted.append(name)
    return ", ".join(formatted)

def entry_to_html(entry):
    title = entry.get("title", "").replace("{", "").replace("}", "")
    authors = format_authors(entry.get("author", ""))
    journal = entry.get("journal", "")
    year = entry.get("year", "")
    venue = f"{journal} · {year}" if journal and year else journal or year

    url = entry.get("url", "")
    if not url and entry.get("doi"):
        url = f"https://doi.org/{entry['doi']}"

    title_html = (
        f'<a href="{url}" target="_blank">{title}</a>'
        if url else title
    )

    return (
        f'<div class="pub-item">\n'
        f'  <div class="pub-title">{title_html}</div>\n'
        f'  <div class="pub-authors">{authors}</div>\n'
        f'  <div class="pub-venue">{venue}</div>\n'
        f'</div>'
    )

def bib_to_html(bib_path):
    parser = BibTexParser(common_strings=True)
    parser.customization = convert_to_unicode
    with open(bib_path) as f:
        db = bibtexparser.load(f, parser=parser)
    entries = sorted(db.entries, key=lambda e: e.get("year", "0"), reverse=True)
    blocks = [entry_to_html(e) for e in entries]
    print("\n\n".join(blocks))

if __name__ == "__main__":
    bib_to_html(MAIN_DIR / 'data' / 'my_biblio.bib')
