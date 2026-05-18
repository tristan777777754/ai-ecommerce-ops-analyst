#!/usr/bin/env python3
"""Publish BusinessRecommendation records to the Lark analysis-layer Base."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LARK = Path("/Users/tristan/.npm-global/bin/lark-cli")
BASE_TOKEN = "EXkPb3IaUapEgfsYMvKjYGdxpQe"
TABLE_NAME = "business_recommendations"
TABLE_ID = "tblkxo9xl31Rfmc8"
BATCH_JSON = ROOT / "outputs" / "business_recommendations" / "business_recommendations_lark_batch.json"


FIELD_SPECS: list[dict[str, Any]] = [
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


def existing_fields() -> set[str]:
    result = run(
        [
            "base",
            "+field-list",
            "--base-token",
            BASE_TOKEN,
            "--table-id",
            TABLE_ID,
            "--offset",
            "0",
            "--limit",
            "200",
        ]
    )
    return {field["name"] for field in result["data"]["fields"]}


def ensure_fields() -> None:
    current = existing_fields()
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
                TABLE_ID,
                "--json",
                json.dumps(spec, ensure_ascii=False),
            ]
        )
        print(f"field created: {spec['name']}")


def create_records() -> int:
    if not BATCH_JSON.exists():
        raise SystemExit(f"Missing batch JSON: {BATCH_JSON}")
    result = run(
        [
            "base",
            "+record-batch-create",
            "--base-token",
            BASE_TOKEN,
            "--table-id",
            TABLE_ID,
            "--json",
            f"@{BATCH_JSON.relative_to(ROOT)}",
        ]
    )
    record_ids = result.get("data", {}).get("record_id_list") or []
    return len(record_ids)


def main() -> None:
    ensure_fields()
    created = create_records()
    print(f"created_records={created}")
    print(f"table_id={TABLE_ID}")


if __name__ == "__main__":
    if not LARK.exists():
        raise SystemExit(f"lark-cli not found: {LARK}")
    sys.exit(main())
