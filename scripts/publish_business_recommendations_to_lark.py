#!/usr/bin/env python3
"""Publish BusinessRecommendation records to the Lark analysis-layer Base."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LARK = Path(os.environ.get("LARK_CLI", "/Users/tristan/.npm-global/bin/lark-cli"))
BASE_TOKEN = os.environ.get("LARK_BASE_TOKEN", "NSswboSyUamlCVsrKyzjQLqWpze")
TABLE_NAME = "business_recommendations"
TABLE_ID = os.environ.get("LARK_BUSINESS_RECOMMENDATIONS_TABLE_ID", "")
BATCH_JSON = ROOT / "outputs" / "business_recommendations" / "business_recommendations_lark_batch.json"
FORCE_REPUBLISH = os.environ.get("LARK_FORCE_REPUBLISH", "").lower() in {"1", "true", "yes"}


FIELD_SPECS: list[dict[str, Any]] = [
    {"name": "recommendation_id", "type": "text"},
    {
        "name": "action_type",
        "type": "select",
        "multiple": False,
        "options": [
            {"name": "CreateCustomerWinbackCampaign", "hue": "Blue", "lightness": "Light"},
            {"name": "SendReactivationOffer", "hue": "Green", "lightness": "Light"},
            {"name": "InvestigateSeller", "hue": "Orange", "lightness": "Light"},
            {"name": "DeprioritizeRiskySeller", "hue": "Red", "lightness": "Light"},
            {"name": "MonitorDeliveryRisk", "hue": "Purple", "lightness": "Light"},
            {"name": "InvestigateLowReviewProductCategory", "hue": "Yellow", "lightness": "Light"},
            {"name": "PromoteHighRevenueCategory", "hue": "Turquoise", "lightness": "Light"},
        ],
    },
    {"name": "target_type", "type": "text"},
    {"name": "target_id", "type": "text"},
    {
        "name": "priority",
        "type": "select",
        "multiple": False,
        "options": [
            {"name": "High", "hue": "Red", "lightness": "Light"},
            {"name": "Medium", "hue": "Orange", "lightness": "Light"},
            {"name": "Low", "hue": "Green", "lightness": "Light"},
        ],
    },
    {
        "name": "status",
        "type": "select",
        "multiple": False,
        "options": [
            {"name": "proposed", "hue": "Blue", "lightness": "Light"},
            {"name": "approved", "hue": "Green", "lightness": "Light"},
            {"name": "rejected", "hue": "Red", "lightness": "Light"},
            {"name": "executed", "hue": "Purple", "lightness": "Light"},
            {"name": "expired", "hue": "Gray", "lightness": "Light"},
        ],
    },
    {"name": "trigger", "type": "text"},
    {"name": "reason", "type": "text"},
    {"name": "evidence_summary", "type": "text"},
    {"name": "source_view", "type": "text"},
    {"name": "created_at", "type": "text"},
    {"name": "orders", "type": "number", "style": {"type": "plain", "precision": 0}},
    {"name": "revenue", "type": "number", "style": {"type": "plain", "precision": 2}},
    {"name": "monetary_value", "type": "number", "style": {"type": "plain", "precision": 2}},
    {"name": "recency_days", "type": "number", "style": {"type": "plain", "precision": 1}},
    {"name": "low_review_rate", "type": "number", "style": {"type": "plain", "precision": 4}},
    {"name": "late_delivery_rate", "type": "number", "style": {"type": "plain", "precision": 4}},
    {"name": "avg_review_score", "type": "number", "style": {"type": "plain", "precision": 2}},
    {"name": "seller_reliability_score", "type": "number", "style": {"type": "plain", "precision": 1}},
    {"name": "revenue_share", "type": "number", "style": {"type": "plain", "precision": 4}},
    {"name": "avg_delay_days", "type": "number", "style": {"type": "plain", "precision": 2}},
]


def run(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        [str(LARK), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = completed.stdout.strip() or completed.stderr.strip()
    try:
        parsed = json.loads(output)
    except json.JSONDecodeError:
        print(output)
        raise
    if completed.returncode != 0 or not parsed.get("ok"):
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
        raise SystemExit(completed.returncode or 1)
    return parsed


def table_id_from_table(table: dict[str, Any]) -> str:
    return table.get("id") or table.get("table_id") or ""


def table_name_from_table(table: dict[str, Any]) -> str:
    return table.get("name") or table.get("table_name") or ""


def table_list() -> list[dict[str, Any]]:
    result = run(
        [
            "base",
            "+table-list",
            "--base-token",
            BASE_TOKEN,
            "--offset",
            "0",
            "--limit",
            "100",
            "--as",
            "user",
        ]
    )
    data = result.get("data", {})
    return data.get("tables") or data.get("items") or []


def find_table_id() -> str:
    if TABLE_ID:
        return TABLE_ID
    for table in table_list():
        if table_name_from_table(table) == TABLE_NAME:
            table_id = table_id_from_table(table)
            if table_id:
                return table_id
    return ""


def create_table() -> str:
    fields = FIELD_SPECS
    result = run(
        [
            "base",
            "+table-create",
            "--base-token",
            BASE_TOKEN,
            "--name",
            TABLE_NAME,
            "--fields",
            json.dumps(fields, ensure_ascii=False),
            "--view",
            json.dumps({"name": "All Recommendations", "type": "grid"}, ensure_ascii=False),
            "--as",
            "user",
        ]
    )
    data = result.get("data", {})
    table = data.get("table") or data.get("item") or data
    table_id = table_id_from_table(table)
    if not table_id:
        table_id = find_table_id()
    if not table_id:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise SystemExit("Could not determine created table id")
    return table_id


def ensure_table() -> str:
    table_id = find_table_id()
    if table_id:
        print(f"table exists: {TABLE_NAME} ({table_id})")
        return table_id
    table_id = create_table()
    print(f"table created: {TABLE_NAME} ({table_id})")
    return table_id


def existing_fields(table_id: str) -> set[str]:
    result = run(
        [
            "base",
            "+field-list",
            "--base-token",
            BASE_TOKEN,
            "--table-id",
            table_id,
            "--offset",
            "0",
            "--limit",
            "200",
            "--as",
            "user",
        ]
    )
    return {field["name"] for field in result["data"]["fields"]}


def ensure_fields(table_id: str) -> None:
    current = existing_fields(table_id)
    for spec in FIELD_SPECS:
        if spec["name"] in current:
            print(f"field exists: {spec['name']}")
            continue
        run(
            [
                "base",
                "+field-create",
                "--base-token",
                BASE_TOKEN,
                "--table-id",
                table_id,
                "--json",
                json.dumps(spec, ensure_ascii=False),
                "--as",
                "user",
            ]
        )
        print(f"field created: {spec['name']}")


def batch_records(batch: dict[str, Any], size: int = 200) -> list[dict[str, Any]]:
    fields = batch["fields"]
    rows = batch["rows"]
    return [
        {"fields": fields, "rows": rows[index : index + size]}
        for index in range(0, len(rows), size)
    ]


def existing_record_count(table_id: str) -> int:
    result = run(
        [
            "base",
            "+record-list",
            "--base-token",
            BASE_TOKEN,
            "--table-id",
            table_id,
            "--field-id",
            "recommendation_id",
            "--offset",
            "0",
            "--limit",
            "200",
            "--format",
            "json",
            "--as",
            "user",
        ]
    )
    data = result.get("data", {})
    records = data.get("record_id_list") or data.get("records") or data.get("items") or []
    return len(records)


def create_records(table_id: str) -> int:
    if not BATCH_JSON.exists():
        raise SystemExit(f"Missing batch JSON: {BATCH_JSON}")
    batch = json.loads(BATCH_JSON.read_text(encoding="utf-8"))
    existing = existing_record_count(table_id)
    expected = len(batch["rows"])
    if existing >= expected and not FORCE_REPUBLISH:
        print(f"existing_records={existing}; expected_records={expected}; skipping_create=true")
        return 0
    created = 0
    tmpdir = ROOT / "outputs" / "business_recommendations" / ".tmp_publish"
    tmpdir.mkdir(parents=True, exist_ok=True)
    for old_file in tmpdir.glob("business_recommendations_batch_*.json"):
        old_file.unlink()
    for index, chunk in enumerate(batch_records(batch), start=1):
        chunk_path = tmpdir / f"business_recommendations_batch_{index}.json"
        chunk_path.write_text(json.dumps(chunk, ensure_ascii=False), encoding="utf-8")
        result = run(
            [
                "base",
                "+record-batch-create",
                "--base-token",
                BASE_TOKEN,
                "--table-id",
                table_id,
                "--json",
                f"@{chunk_path.relative_to(ROOT)}",
                "--as",
                "user",
            ]
        )
        record_ids = result.get("data", {}).get("record_id_list") or []
        created += len(record_ids)
        print(f"batch {index}: created_records={len(record_ids)}")
    return created


def main() -> None:
    table_id = ensure_table()
    ensure_fields(table_id)
    created = create_records(table_id)
    print(f"created_records={created}")
    print(f"base_token={BASE_TOKEN}")
    print(f"table_id={table_id}")


if __name__ == "__main__":
    if not LARK.exists():
        raise SystemExit(f"lark-cli not found: {LARK}")
    sys.exit(main())
