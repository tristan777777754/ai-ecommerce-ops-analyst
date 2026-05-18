#!/usr/bin/env python3
"""Build an Excel staging workbook for Lark Base import.

This script does not analyze the data. It only packages the raw CSV files into
one workbook, one sheet per source table, so Lark can import them as one Base
with multiple tables.
"""

from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset"
OUT_DIR = ROOT / "outputs" / "lark_import_staging"
OUT_FILE = OUT_DIR / "olist_raw_tables_for_lark_base.xlsx"

TABLES = [
    ("raw_customers", "olist_customers_dataset.csv"),
    ("raw_orders", "olist_orders_dataset.csv"),
    ("raw_order_items", "olist_order_items_dataset.csv"),
    ("raw_order_payments", "olist_order_payments_dataset.csv"),
    ("raw_order_reviews", "olist_order_reviews_dataset.csv"),
    ("raw_products", "olist_products_dataset.csv"),
    ("raw_sellers", "olist_sellers_dataset.csv"),
    ("raw_geolocation", "olist_geolocation_dataset.csv"),
    ("raw_category_translation", "product_category_name_translation.csv"),
]


def clean_cell(value: str) -> str:
    return value.replace("\ufeff", "") if isinstance(value, str) else value


def append_csv_to_sheet(workbook: Workbook, sheet_name: str, csv_path: Path) -> int:
    sheet = workbook.create_sheet(sheet_name)
    rows = 0
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        for row in reader:
            sheet.append([clean_cell(cell) for cell in row])
            rows += 1
    return rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    workbook = Workbook(write_only=True)

    print(f"Writing {OUT_FILE}")
    for sheet_name, filename in TABLES:
        csv_path = DATASET / filename
        rows = append_csv_to_sheet(workbook, sheet_name, csv_path)
        print(f"{sheet_name}: {rows:,} rows including header")

    workbook.save(OUT_FILE)
    print(f"Saved {OUT_FILE} ({OUT_FILE.stat().st_size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main()
