import argparse
from pathlib import Path
import zipfile
import sys
import requests

COMPETITIONS = {
    "ipl"   : "https://cricsheet.org/downloads/ipl_male_json.zip",
    "smat"  : "https://cricsheet.org/downloads/sma_male_json.zip",
    "bbl"   : "https://cricsheet.org/downloads/bbl_male_json.zip",
    "t20i"  : "https://cricsheet.org/downloads/t20s_male_json.zip",
    "sa20"  : "https://cricsheet.org/downloads/sat_male_json.zip",
    "ilt20" : "https://cricsheet.org/downloads/ilt_male_json.zip",
}

def is_data_present(competition: str) -> bool:
    """
    Check if the data for the given competition is already present in the data directory.

    Args:
        competition (str): The name of the competition.

    Returns:
        bool: True if the data is present, False otherwise.
    """
    data_dir = Path(__file__).parent.parent / "data" / "raw" / competition
    return data_dir.exists() and any(data_dir.glob("*.json"))

def download_competition(competition_slug: str, competition_url: str) -> None:
    """
    Download and extract the data for a given competition.

    Args:
        competition_slug (str): The slug of the competition.
        competition_url (str): The URL to download the competition data from.
    """
    dest_dir = Path(__file__).parent.parent / "data" / "raw" / competition_slug
    dest_dir.mkdir(parents=True, exist_ok=True)

    zip_path = dest_dir.parent / f"{competition_slug}.zip"

    print(f"Downloading {competition_slug} data...")
    response = requests.get(competition_url, stream=True)

    if response.status_code == 200:
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Extracting {competition_slug} data...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(dest_dir)

        zip_path.unlink()

        json_count = len(list(dest_dir.glob("*.json")))
        print(f"Done. {json_count} match files extracted to data/raw/{competition_slug}/")

    else:
        print(f"Download failed. Status code: {response.status_code}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Download cricket match data from Cricsheet.")
    parser.add_argument(
        "competition",
        choices=COMPETITIONS.keys(),
        help="The competition to download data for. Choices are: " + ", ".join(COMPETITIONS.keys())
    )
    args = parser.parse_args()

    competition_slug = args.competition
    competition_url = COMPETITIONS[competition_slug]

    if is_data_present(competition_slug):
        print(f"Data for {competition_slug} is already present in the data/raw/{competition_slug}/ directory.")
        sys.exit(0)

    download_competition(competition_slug, competition_url)

if __name__ == "__main__":
    main()