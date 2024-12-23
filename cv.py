import json

import requests
from pylatex import Command, Document, Package, Section
from pylatex.utils import NoEscape, bold, escape_latex, italic
from scholarly import scholarly


def education(doc):
    with doc.create(Section("Education", numbering=False)):
        # Colubmia
        doc.append(bold("Columbia University, New York, NY"))
        doc.append(NoEscape(r"\hfill May 2025"))
        doc.append("\nM.S. in Materials Science and Engineering")
        doc.append("\n- Advisor: Prof. Simon Billinge")
        doc.append("\n- Department of Applied Physics and Applied Mathematics")

        # Cooper Union
        doc.append("\n\n")
        doc.append(bold("Cooper Union, New York, NY"))
        doc.append(NoEscape(r"\hfill May 2023"))
        doc.append(
            "\nB.E. in Chemical Engineering, minors in Computer Science and Chemistry"
        )
        doc.append("\n- Advisor: Prof. Robert Topper")
        doc.append("\n- Department of Chemical Engineering")


def interests(doc):
    with doc.create(Section("Interests", numbering=False)):
        doc.append(
            "Data-driven materials discovery, High-throughput, Experimental "
            "validation, Open-source development, DFT, Deep neural network potential"
        )


def awards(doc):
    with doc.create(Section("Awards", numbering=False)):
        doc.append(
            "2023 American Chemical Society (ACS) New York Outstanding Student Award\n"
        )
        doc.append("2023 American Institute of Chemists (AIC) Student Award\n")
        doc.append("2022 Summer STEM Teaching Fellowship, Cooper Union\n")
        doc.append("4-Year Half-tuition Merit Scholarship, Cooper Union\n")
        doc.append("4-Year Innovator’s Merit Scholarship, Cooper Union\n")
        doc.append("4-Year Corporate Scholarship, Donghwa Enterprise ")


def publications(doc):
    data = _load_json_file("data/publications.json")
    with doc.create(Section("Publications", numbering=False)):
        doc.append(
            f"Google Scholar citations: {str(_get_google_scholar_citations())} "
            f"from {len(data)} peer-reviewed publications\n\n"
        )
        doc.append(
            "‡ – these authors contributed equally to the work; * – corresponding author\n\n"
        )

        # Enumerate and format each publication with numbering in reverse order
        for i, pub in enumerate(data, start=1):
            doc.append(bold(f"{i}. {pub['title']}\n"))
            doc.append(", ".join(pub["authors"]) + "\n")
            doc.append(
                _hyperlink(f"https://doi.org/{pub['doi']}", italic(pub["journal"]))
            )
            doc.append(_add_extra_line_break_if_not_last_item(data, i))


def manuscript(doc):
    with doc.create(Section("Manuscripts submitted", numbering=False)):
        data = _load_json_file("data/manuscripts.json")
        data.sort(key=lambda x: x["date"], reverse=True)
        for i, pub in enumerate(data, start=1):
            doc.append(bold(f"{i}. {pub['title']}\n"))
            doc.append(", ".join(pub["authors"]) + "\n")
            if "doi" in pub and pub["doi"]:  # Check if DOI is present and not empty
                doc.append(
                    _hyperlink(f"https://doi.org/{pub['doi']}", italic(pub["doi"]))
                )
            # Add a new line if not the last publication
            doc.append(_add_extra_line_break_if_not_last_item(data, i))


def presentation(doc):
    with doc.create(Section("Presentations", numbering=False)):
        data = _load_json_file("data/presentations.json")
        data.sort(key=lambda x: x["date"], reverse=True)
        for i, presentation in enumerate(data, start=1):
            doc.append(bold(f"{i}.{presentation['title']}\n"))
            doc.append(f"{presentation['authors']}\n")
            doc.append(NoEscape(r"\emph{" + presentation["conference"] + "}."))
            doc.append(
                f"\n {presentation['type']}, {presentation['location']}, {presentation['date']}. "
            )
            if "url" in presentation and presentation["url"]:
                doc.append(_hyperlink(presentation["url"], "[pdf]"))
            doc.append(_add_extra_line_break_if_not_last_item(data, i))


def software(doc):
    with doc.create(Section("Research software", numbering=False)):
        data = _load_json_file("data/software.json")
        for i, software in enumerate(data, start=1):
            doc.append(bold(f"{i}. {software['title']}"))
            doc.append("\n")
            doc.append(_hyperlink(software["url"], "GitHub"))
            owner = software["owner"]
            repo = software["repo_name"]
            star_count = _get_github_repo_stars(owner, repo)
            doc.append(f", {star_count} stars")
            doc.append(_add_extra_line_break_if_not_last_item(data, i))


def _add_extra_line_break_if_not_last_item(data, i):
    if i != len(data):
        return "\n\n"
    return ""


def _get_github_repo_stars(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url)
    data = response.json()
    return data["stargazers_count"]


def _load_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def _hyperlink(url, text):
    text = escape_latex(text)
    return NoEscape(r"\href{" + url + "}{" + text + "}")


def _get_google_scholar_citations(author_id="L07HlVsAAAAJ"):
    author = scholarly.search_author_id(author_id)
    return author["citedby"]


if __name__ == "__main__":
    geometry_options = {"tmargin": "0.5in", "lmargin": "1.0in"}
    doc = Document("basic", geometry_options=geometry_options)
    doc.packages.append(Package("hyperref"))
    doc.preamble.append(Command("date", NoEscape(r"\today")))
    doc.append(
        NoEscape(r"\moveleft.5\hoffset\centerline{\large\bf Sangjoon (Bob) Lee}")
    )  # Your name
    doc.append(
        NoEscape(
            r"\moveleft.5\hoffset\centerline{\small sl5400@columbia.edu | \href{https://bobleesj.github.io/}{https://bobleesj.github.io/} | (404) 747-2468}"
        )
    )

    education(doc)
    interests(doc)
    awards(doc)
    manuscript(doc)
    publications(doc)
    presentation(doc)
    software(doc)
    doc.generate_pdf("Sangjoon_Lee_CV", clean_tex=True)

# Without NoEscape, you'd need to manually escape backslashes in Python strings.
# With NoEscape, you can directly use LaTeX commands.
# doc.append(NoEscape(r"\textbf{Bold Text}"))

# doc.generate_pdf("sample", clean_tex=False)
