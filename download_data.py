"""Download the real Ames Housing dataset (no synthetic data).

Fetches the training CSV from the SPS mirror repository (a mirror of the
Kaggle "House Prices: Advanced Regression Techniques" competition data,
compiled by Dean De Cock) and saves it to data/ames_housing.csv.

URL: https://raw.githubusercontent.com/jzuniga123/SPS/master/DATA%20605/train.csv
"""

import urllib.request
from pathlib import Path

URL = "https://raw.githubusercontent.com/jzuniga123/SPS/master/DATA%20605/train.csv"


def main() -> None:
    target = Path(__file__).resolve().parent / "data" / "ames_housing.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading Ames Housing dataset from:\n  {URL}")
    urllib.request.urlretrieve(URL, target)
    print(f"Saved to {target} ({target.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
