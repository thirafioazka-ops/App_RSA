"""Memuat dataset Old Faithful Geyser (faithful).

Urutan pencarian data:
1. data/faithful.csv (lokal)
2. Unduh dari Rdatasets, lalu simpan ke data/faithful.csv
"""
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).parent / "data" / "faithful.csv"
DATA_URL = (
    "https://vincentarelbundock.github.io/Rdatasets/csv/datasets/faithful.csv"
)


def load_faithful() -> pd.DataFrame:
    """Mengembalikan DataFrame dengan kolom `eruptions` dan `waiting`."""
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
    else:
        df = pd.read_csv(DATA_URL)
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        df[["eruptions", "waiting"]].to_csv(DATA_PATH, index=False)

    return df[["eruptions", "waiting"]].dropna().reset_index(drop=True)


if __name__ == "__main__":
    data = load_faithful()
    print(f"Data tersimpan di: {DATA_PATH}")
    print(data.describe())
