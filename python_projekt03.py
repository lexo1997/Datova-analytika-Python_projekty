"""
main.py: třetí projekt do Engeto Online Python Akademie
Projekt: Elections Scraper

author: Alex Mičáň
email: mican.alex@gmail.com
"""

import csv
import sys
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

BASE_COLUMNS = ["code", "location", "registered", "envelopes", "valid"]
CSV_DELIMITER = ";"
REQUEST_TIMEOUT = 15


def validate_arguments(arguments: list[str]) -> tuple[str, str]:
    """Validate CLI arguments and return source URL and output CSV path."""
    if len(arguments) != 3:
        raise ValueError(
            "Použití: python main.py <url_uzemniho_celku> <vystup.csv>"
        )

    source_url = arguments[1]
    output_file = arguments[2]
    parsed_url = urlparse(source_url)

    if parsed_url.scheme not in {"http", "https"}:
        raise ValueError("První argument musí být platná URL adresa.")
    if "volby.cz" not in parsed_url.netloc:
        raise ValueError("URL musí směřovat na web volby.cz.")
    if "ps2017nss" not in parsed_url.path:
        raise ValueError("URL musí směřovat na výsledky voleb PS 2017.")
    if not output_file.lower().endswith(".csv"):
        raise ValueError("Druhý argument musí být název souboru s příponou .csv.")

    return source_url, output_file


def get_soup(url: str) -> BeautifulSoup:
    """Download a web page and return parsed HTML content."""
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return BeautifulSoup(response.text, "html.parser")


def clean_text(value: str) -> str:
    """Normalize text values from HTML tables."""
    return " ".join(value.replace("\xa0", " ").split())


def clean_number(value: str) -> str:
    """Remove spaces from numeric values scraped from the web."""
    return clean_text(value).replace(" ", "")


def cell_by_header(soup: BeautifulSoup, header: str) -> str:
    """Find a table cell by its exact HTML headers attribute."""
    cell = soup.find("td", attrs={"headers": header})
    if cell is None:
        raise ValueError(f"Nelze najít hodnotu ve sloupci {header}.")
    return clean_number(cell.get_text())


def find_municipalities(
    soup: BeautifulSoup, source_url: str
) -> list[tuple[str, str, str]]:
    """Return municipality code, name and detail URL from territorial page."""
    municipalities = []

    for row in soup.find_all("tr"):
        code_cell = row.find("td", class_="cislo")
        name_cell = row.find("td", class_="overflow_name")
        link = code_cell.find("a") if code_cell else None

        if not link or not name_cell:
            continue

        code = clean_text(link.get_text())
        location = clean_text(name_cell.get_text())
        detail_url = urljoin(source_url, link["href"])
        municipalities.append((code, location, detail_url))

    if not municipalities:
        raise ValueError("Na zadané stránce nebyly nalezeny odkazy na obce.")

    return municipalities


def parse_parties_and_votes(soup: BeautifulSoup) -> dict[str, str]:
    """Return election party names and their vote counts for one municipality."""
    results = {}

    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 3:
            continue

        party_number = clean_number(cells[0].get_text())
        party_name = clean_text(cells[1].get_text())
        votes = clean_number(cells[2].get_text())

        if party_number.isdigit() and party_name and votes.isdigit():
            results[party_name] = votes

    if not results:
        raise ValueError("Na stránce obce nebyly nalezeny výsledky stran.")

    return results


def parse_municipality(code: str, location: str, url: str) -> dict[str, str]:
    """Scrape all required data for one municipality."""
    soup = get_soup(url)
    row = {
        "code": code,
        "location": location,
        "registered": cell_by_header(soup, "sa2"),
        "envelopes": cell_by_header(soup, "sa3"),
        "valid": cell_by_header(soup, "sa6"),
    }
    row.update(parse_parties_and_votes(soup))
    return row


def scrape_elections(source_url: str) -> list[dict[str, str]]:
    """Scrape election results for all municipalities in the selected area."""
    soup = get_soup(source_url)
    municipalities = find_municipalities(soup, source_url)
    results = []

    for index, (code, location, detail_url) in enumerate(municipalities, start=1):
        print(f"Stahuji obec {index}/{len(municipalities)}: {location}")
        results.append(parse_municipality(code, location, detail_url))

    return results


def get_csv_header(rows: list[dict[str, str]]) -> list[str]:
    """Create CSV header while preserving the order of party columns."""
    header = BASE_COLUMNS.copy()

    for row in rows:
        for column in row:
            if column not in header:
                header.append(column)

    return header


def save_to_csv(rows: list[dict[str, str]], output_file: str) -> None:
    """Save scraped rows into a CSV file."""
    header = get_csv_header(rows)

    with open(output_file, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=header,
            delimiter=CSV_DELIMITER,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    """Run the election scraper from command-line arguments."""
    try:
        source_url, output_file = validate_arguments(sys.argv)
        print(f"Stahuji data z vybraného územního celku: {source_url}")
        rows = scrape_elections(source_url)
        save_to_csv(rows, output_file)
        print(f"Hotovo. Výsledky byly uloženy do souboru: {output_file}")
    except (requests.RequestException, ValueError) as error:
        print(f"Chyba: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
