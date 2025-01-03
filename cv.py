import json
from datetime import datetime

import requests
from pylatex import Document, Package, Section
from pylatex.utils import NoEscape, bold, escape_latex, italic
from scholarly import scholarly


def education(doc):
    with doc.create(Section("Education", numbering=False)):
        # Colubmia University
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
            "\nB.E. in Chemical Engineering, "
            "minors in Computer Science and Chemistry"
        )
        doc.append("\n- Advisor: Prof. Robert Topper")
        doc.append("\n- Department of Chemical Engineering")


def interests(doc):
    with doc.create(Section("Interests", numbering=False)):
        doc.append(
            "Data-driven materials discovery, High-throughput, Experimental "
            "validation, Open-source development, DFT, Deep neural network "
            "potential"
        )


def awards(doc):
    with doc.create(Section("Awards", numbering=False)):
        doc.append(
            "2023 American Chemical Society (ACS) "
            "New York Outstanding Student Award\n"
        )
        doc.append("2023 American Institute of Chemists (AIC) Student Award\n")
        doc.append("2022 Summer STEM Teaching Fellowship, Cooper Union\n")
        doc.append("4-Year Half-tuition Merit Scholarship, Cooper Union\n")
        doc.append("4-Year Innovator’s Merit Scholarship, Cooper Union\n")
        doc.append("4-Year Corporate Scholarship, Donghwa Enterprise")


def publications(doc):
    data = _load_json_file_date("data/publications.json")
    with doc.create(Section("Publications", numbering=False)):
        doc.append(
            f"Google Scholar citations: {str(_get_gscholar_citations())} "
            f"from {len(data)} peer-reviewed publications\n\n"
        )
        doc.append(
            "‡ – these authors contributed equally to the work; "
            "* – corresponding author\n\n"
        )

        # Enumerate and format each publication with numbering in reverse order
        for i, pub in enumerate(data, start=1):
            doc.append(bold(f"{i}. {pub['title']}\n"))
            doc.append(", ".join(pub["authors"]) + "\n")
            doc.append(
                _hyperlink(
                    f"https://doi.org/{pub['doi']}", italic(pub["journal"])
                )
            )
            doc.append(_add_two_extra_line_break_if_not_last_item(data, i))


def manuscripts(doc):
    with doc.create(Section("Manuscripts submitted", numbering=False)):
        data = _load_json_file_date("data/manuscripts.json")
        for i, entry in enumerate(data, start=1):
            doc.append(bold(f"{i}. {entry['title']}\n"))
            doc.append(", ".join(entry["authors"]) + "\n")
            if (
                "doi" in entry and entry["doi"]
            ):  # Check if DOI is present and not empty
                doc.append(
                    _hyperlink(
                        f"https://doi.org/{entry['doi']}", italic(entry["doi"])
                    )
                )
            # Add a new line if not the last publication
            doc.append(_add_two_extra_line_break_if_not_last_item(data, i))


def presentations(doc):
    with doc.create(Section("Presentations", numbering=False)):
        data = _load_json_file_date("data/presentations.json")
        for i, item in enumerate(data, start=1):
            doc.append(bold(f"{i}.{item['title']}\n"))
            doc.append(f"{item['authors']}\n")
            doc.append(NoEscape(r"\emph{" + item["conference"] + "}"))
            doc.append(
                f"\n {item['type']}, {item['location']}, {item['date']}. "
            )
            if "url" in item and item["url"]:
                doc.append(_hyperlink(item["url"], "[pdf]"))
            doc.append(_add_two_extra_line_break_if_not_last_item(data, i))


def software(doc):
    with doc.create(Section("Research software", numbering=False)):
        data = _load_json_file_date("data/software.json", sorted_by_date=False)
        for i, software in enumerate(data, start=1):
            doc.append(bold(f"{i}. {software['title']}"))
            doc.append("\n")
            doc.append(_hyperlink(software["url"], "GitHub"))
            owner = software["owner"]
            repo = software["repo_name"]
            star_count = _get_github_repo_stars(owner, repo)
            doc.append(f", {star_count} stars")
            doc.append(_add_two_extra_line_break_if_not_last_item(data, i))


def coursework(doc):
    with doc.create(Section("Graduate coursework", numbering=False)):
        doc.append(bold("Computation: "))
        doc.append(
            "Deep Learning, Natural Language Processing, Introduction to "
            "Numerical Analysis "
        )
        doc.append(bold("Materials Science & Chemical Engineering: "))
        doc.append(
            "Phonons, Electrons, Condensed Matter Physics I, Crystallography, "
            "Electronic & Magnetic Properties of Solids, Mechanical Behaviors "
            "of Materials, Materials Thermodynamics, Kinetics of "
            "Transformations, Polymer Technology and Engineering"
        )


def teaching(doc):
    with doc.create(Section("Teaching experience", numbering=False)):
        data = _load_json_file_date("data/teaching.json", sorted_by_date=False)
        for i, entry in enumerate(data, start=1):
            doc.append(bold(entry["title"]))
            doc.append(NoEscape(r"\hfill " + entry["duration"]))
            detail = f"\n{entry['symbol']}: {entry['name']} {entry['info']}"
            doc.append(detail)
            location_info = f"\n{entry['org']}, {entry['location']}"
            doc.append(location_info)
            doc.append(_add_two_extra_line_break_if_not_last_item(data, i))


def leadership(doc):
    with doc.create(Section("Leadership", numbering=False)):
        data = _load_json_file_date(
            "data/leadership.json", sorted_by_date=False
        )
        for i, entry in enumerate(data, start=1):
            doc.append(bold(f"{entry['title']}: "))
            doc.append(f"{entry['org']}")
            doc.append(NoEscape(r"\hfill " + entry["duration"]))
            doc.append(_add_one_extra_line_break_if_not_last_item(data, i))


def service(doc):
    with doc.create(Section("Service", numbering=False)):
        data = _load_json_file_date("data/service.json")
        for i, entry in enumerate(data, start=1):
            formatted_date = _format_month_from_number_to_word(entry["date"])
            doc.append(f"{entry['event']}, ")
            doc.append(f"{entry['role']}")
            doc.append(NoEscape(r"\hfill " + formatted_date))
            doc.append(_add_one_extra_line_break_if_not_last_item(data, i))


###############################################################################
# Helper functions ex) Google Scholar citation, date format, GitHub star,
# add hyperlink to text, load JSON file, add extra line break
###############################################################################


def _add_one_extra_line_break_if_not_last_item(data: dict, i: int) -> str:
    if i != len(data):
        return "\n"
    return ""


def _add_two_extra_line_break_if_not_last_item(data: dict, i: int) -> str:
    if i != len(data):
        return "\n\n"
    return ""


def _get_github_repo_stars(owner: str, repo: str) -> int:
    "Get the number of stars for a GitHub repository."
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url)
    data = response.json()
    return data["stargazers_count"]


def _load_json_file_date(file_path: str, sorted_by_date=True) -> dict:
    """Load a JSON file and return the data."""
    with open(file_path, "r") as file:
        data = json.load(file)
        if sorted_by_date:
            data.sort(
                key=lambda x: datetime.strptime(x["date"], "%Y-%m"),
                reverse=True,
            )
        return data


def _format_month_from_number_to_word(date_str):
    # Convert date string from "YYYY-MM" to "Month YYYY"
    return datetime.strptime(date_str, "%Y-%m").strftime("%B %Y")


def _hyperlink(url: str, text: str) -> NoEscape:
    """Add a hpyerlink to the Latex text."""
    text = escape_latex(text)
    return NoEscape(r"\href{" + url + "}{" + text + "}")


def _get_gscholar_citations(author_id="L07HlVsAAAAJ") -> int:
    """Get the number of citations from Google Scholar."""
    author = scholarly.search_author_id(author_id)
    return author["citedby"]


###############################################################################
# Entry when you run python cv.py
###############################################################################

if __name__ == "__main__":

    """PLEASE READ BEFORE RUNNING THE SCRIPT:
    (1) The education, interests, awards sections are hard-coded to provide
    greater flexibility. Other sections are loaded from JSON files under data.

    (2) To format automatically run the following command:
        pre-commit run --all-files

    (3) Visit README https://github.com/bobleesj/python-cv-template for the
        latest CV template and dynamic rendering instructions.
    """
    # Set the geometry options for the document
    geometry_options = {"tmargin": "0.5in", "lmargin": "1.0in"}
    doc = Document("basic", geometry_options=geometry_options)
    # Required to use hyperlinks when rendered as a pdf
    doc.packages.append(Package("hyperref"))
    doc.packages.append(Package("microtype"))

    # Header (Name, email, phone number)
    doc.append(
        NoEscape(
            r"\moveleft.5\hoffset\centerline{\large\bf Sangjoon (Bob) Lee}"
        )
    )
    doc.append(
        NoEscape(
            r"\moveleft.5\hoffset\centerline{\small sl5400@columbia.edu | "
            r"\href{https://bobleesj.github.io/}{bobleesj.github.io} "
            r"| (404) 747-2468}"
        )
    )

    # Sections
    education(doc)
    interests(doc)
    awards(doc)
    manuscripts(doc)
    publications(doc)
    presentations(doc)
    software(doc)
    coursework(doc)
    teaching(doc)
    leadership(doc)
    service(doc)

    # Generate the PDF
    doc.generate_pdf("Sangjoon_Lee_CV", clean_tex=True)
