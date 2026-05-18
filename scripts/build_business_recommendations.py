#!/usr/bin/env python3
"""Build first-version BusinessRecommendation records.

The output is the first ontology/action layer on top of the Lark analysis
workspace. It uses the same metric logic as the analysis-layer workbook, then
converts qualifying signals into proposed, human-approved recommendations.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from build_lark_analysis_workbook import (
    build_category_tables,
    build_delivery_risk,
    build_model,
    build_rfm,
    build_seller_performance,
    load_data,
    round_numeric,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs" / "business_recommendations"
OUT_CSV = OUT_DIR / "business_recommendations.csv"
OUT_MD = OUT_DIR / "BUSINESS_RECOMMENDATIONS.md"
OUT_JSON = OUT_DIR / "business_recommendations_lark_batch.json"
CREATED_AT = date(2026, 5, 18).isoformat()

FIELDS = [
    "recommendation_id",
    "action_type",
    "target_type",
    "target_id",
    "priority",
    "status",
    "trigger",
    "reason",
    "evidence_summary",
    "source_view",
    "created_at",
    "orders",
    "revenue",
    "monetary_value",
    "recency_days",
    "low_review_rate",
    "late_delivery_rate",
    "avg_review_score",
    "seller_reliability_score",
    "revenue_share",
    "avg_delay_days",
]


def clean(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (np.integer, np.floating)):
        value = value.item()
    if isinstance(value, float) and np.isnan(value):
        return None
    return value


def pct(value: Any) -> str:
    value = clean(value)
    if value is None:
        return "n/a"
    return f"{float(value):.2%}"


def money(value: Any) -> str:
    value = clean(value)
    if value is None:
        return "n/a"
    return f"{float(value):,.2f}"


def add_recommendation(records: list[dict[str, Any]], **kwargs: Any) -> None:
    record = {field: None for field in FIELDS}
    record.update(kwargs)
    record["status"] = record.get("status") or "proposed"
    record["created_at"] = record.get("created_at") or CREATED_AT
    records.append({key: clean(value) for key, value in record.items()})


def build_recommendations() -> pd.DataFrame:
    data = load_data()
    model = build_model(data)
    order_facts = model["order_facts"]
    item_enriched = model["item_enriched"]

    rfm, rfm_summary, dormant = build_rfm(order_facts)
    seller, seller_risk = build_seller_performance(item_enriched)
    category, review_risk, category_opportunity = build_category_tables(item_enriched)
    delivery_risk = build_delivery_risk(order_facts)
    round_numeric([rfm, rfm_summary, dormant, seller, seller_risk, category, review_risk, category_opportunity, delivery_risk])

    records: list[dict[str, Any]] = []

    campaign_segments = rfm_summary[
        rfm_summary["rfm_segment"].isin(["Dormant High Value", "At Risk"])
        & (rfm_summary["customers"] >= 100)
    ].sort_values("revenue", ascending=False)
    for _, row in campaign_segments.iterrows():
        priority = "High" if row["revenue_share"] >= 0.10 or row["revenue"] >= 100000 else "Medium"
        add_recommendation(
            records,
            action_type="CreateCustomerWinbackCampaign",
            target_type="CustomerSegment",
            target_id=row["rfm_segment"],
            priority=priority,
            trigger='segment in ["Dormant High Value", "At Risk"] and customers >= 100',
            reason="Customer segment has enough dormant or at-risk value to justify a winback campaign proposal.",
            evidence_summary=(
                f"customers={int(row['customers'])}; revenue={money(row['revenue'])}; "
                f"revenue_share={pct(row['revenue_share'])}; avg_recency_days={row['avg_recency_days']:.1f}"
            ),
            source_view="rfm_segment_summary",
            orders=None,
            revenue=round(float(row["revenue"]), 2),
            revenue_share=round(float(row["revenue_share"]), 4),
            recency_days=round(float(row["avg_recency_days"]), 1),
        )

    for _, row in dormant.sort_values(["monetary_value", "recency_days"], ascending=[False, False]).head(30).iterrows():
        priority = "High" if row["monetary_value"] >= 300 and row["recency_days"] >= 180 else "Medium"
        add_recommendation(
            records,
            action_type="SendReactivationOffer",
            target_type="Customer",
            target_id=row["customer_unique_id"],
            priority=priority,
            trigger='rfm_segment == "Dormant High Value" and monetary_value is present and recency_days is present',
            reason="High historical value and long inactivity signal a winback opportunity.",
            evidence_summary=(
                f"monetary_value={money(row['monetary_value'])}; recency_days={int(row['recency_days'])}; "
                f"rfm_segment={row['rfm_segment']}"
            ),
            source_view="dormant_high_value",
            monetary_value=round(float(row["monetary_value"]), 2),
            recency_days=int(row["recency_days"]),
        )

    for _, row in seller_risk.sort_values(["risk_band", "seller_reliability_score", "revenue"], ascending=[True, True, False]).head(30).iterrows():
        severe = (
            int(row["orders"]) >= 50
            and (
                row["late_delivery_rate"] >= 0.25
                or row["low_review_rate"] >= 0.30
                or row["seller_reliability_score"] <= 65
            )
        )
        action_type = "DeprioritizeRiskySeller" if severe else "InvestigateSeller"
        priority = "High" if severe or row["low_review_rate"] >= 0.35 or row["late_delivery_rate"] >= 0.25 or row["seller_reliability_score"] <= 70 else "Medium"
        trigger = (
            "orders >= 50 and severe seller risk threshold met"
            if severe
            else "orders >= 30 and late_delivery_rate >= 0.15 or low_review_rate >= 0.18 or seller_reliability_score <= 75"
        )
        add_recommendation(
            records,
            action_type=action_type,
            target_type="Seller",
            target_id=row["seller_id"],
            priority=priority,
            trigger=trigger,
            reason="Seller has meaningful order volume and elevated fulfillment or customer dissatisfaction risk.",
            evidence_summary=(
                f"orders={int(row['orders'])}; revenue={money(row['revenue'])}; "
                f"late_delivery_rate={pct(row['late_delivery_rate'])}; low_review_rate={pct(row['low_review_rate'])}; "
                f"seller_reliability_score={row['seller_reliability_score']:.1f}"
            ),
            source_view="seller_risk_watchlist",
            orders=int(row["orders"]),
            revenue=round(float(row["revenue"]), 2),
            low_review_rate=round(float(row["low_review_rate"]), 4),
            late_delivery_rate=round(float(row["late_delivery_rate"]), 4),
            avg_review_score=round(float(row["avg_review_score"]), 2) if pd.notna(row["avg_review_score"]) else None,
            seller_reliability_score=round(float(row["seller_reliability_score"]), 1),
            avg_delay_days=round(float(row["avg_delivery_delay_days"]), 2) if pd.notna(row["avg_delivery_delay_days"]) else None,
        )

    for _, row in delivery_risk.head(10).iterrows():
        priority = "High" if row["orders"] >= 500 and row["late_delivery_rate"] >= 0.15 else "Medium"
        add_recommendation(
            records,
            action_type="MonitorDeliveryRisk",
            target_type="Geography",
            target_id=row["target_id"],
            priority=priority,
            trigger="orders >= 100 and late_delivery_rate >= 0.12",
            reason="Customer geography has elevated delivery delay risk and should be monitored before changing promises or logistics rules.",
            evidence_summary=(
                f"orders={int(row['orders'])}; revenue={money(row['revenue'])}; "
                f"late_delivery_rate={pct(row['late_delivery_rate'])}; avg_delay_days={row['avg_delay_days']:.2f}"
            ),
            source_view="delivery_risk_by_state",
            orders=int(row["orders"]),
            revenue=round(float(row["revenue"]), 2),
            late_delivery_rate=round(float(row["late_delivery_rate"]), 4),
            low_review_rate=round(float(row["low_review_rate"]), 4),
            avg_delay_days=round(float(row["avg_delay_days"]), 2) if pd.notna(row["avg_delay_days"]) else None,
        )

    for _, row in review_risk.head(20).iterrows():
        priority = "High" if row["revenue"] >= 100000 and row["low_review_rate"] >= 0.20 else "Medium"
        add_recommendation(
            records,
            action_type="InvestigateLowReviewProductCategory",
            target_type="ProductCategory",
            target_id=row["category_name"],
            priority=priority,
            trigger="orders >= 100 and low_review_rate >= 0.15",
            reason="Category has enough order volume and elevated low-review rate; investigate product, fulfillment, or expectation mismatch before growth actions.",
            evidence_summary=(
                f"orders={int(row['orders'])}; revenue={money(row['revenue'])}; "
                f"low_review_rate={pct(row['low_review_rate'])}; avg_review_score={row['avg_review_score']:.2f}"
            ),
            source_view="review_risk_by_category",
            orders=int(row["orders"]),
            revenue=round(float(row["revenue"]), 2),
            low_review_rate=round(float(row["low_review_rate"]), 4),
            late_delivery_rate=round(float(row["late_delivery_rate"]), 4),
            avg_review_score=round(float(row["avg_review_score"]), 2) if pd.notna(row["avg_review_score"]) else None,
            avg_delay_days=round(float(row["avg_delivery_delay_days"]), 2) if pd.notna(row["avg_delivery_delay_days"]) else None,
        )

    promotable = category_opportunity[
        category_opportunity["recommended_action"].eq("PromoteHighRevenueCategory")
    ].head(10)
    for _, row in promotable.iterrows():
        priority = "High" if row["revenue_share"] >= 0.05 and row["low_review_rate"] < 0.15 else "Medium"
        add_recommendation(
            records,
            action_type="PromoteHighRevenueCategory",
            target_type="ProductCategory",
            target_id=row["category_name"],
            priority=priority,
            trigger='pareto_band == "top_80_percent_revenue" and low_review_rate < 0.15',
            reason="Category is revenue-critical and review risk is below the investigation threshold, so it is a candidate for promotion or protection.",
            evidence_summary=(
                f"revenue={money(row['revenue'])}; revenue_share={pct(row['revenue_share'])}; "
                f"cumulative_share={pct(row['cumulative_share'])}; low_review_rate={pct(row['low_review_rate'])}"
            ),
            source_view="category_opportunity",
            orders=int(row["orders"]),
            revenue=round(float(row["revenue"]), 2),
            low_review_rate=round(float(row["low_review_rate"]), 4),
            late_delivery_rate=round(float(row["late_delivery_rate"]), 4),
            avg_review_score=round(float(row["avg_review_score"]), 2) if pd.notna(row["avg_review_score"]) else None,
            revenue_share=round(float(row["revenue_share"]), 4),
            avg_delay_days=round(float(row["avg_delivery_delay_days"]), 2) if pd.notna(row["avg_delivery_delay_days"]) else None,
        )

    recs = pd.DataFrame(records, columns=FIELDS)
    recs.insert(0, "rank", range(1, len(recs) + 1))
    recs["recommendation_id"] = [f"REC-{i:04d}" for i in range(1, len(recs) + 1)]
    return recs


def write_markdown(recs: pd.DataFrame) -> None:
    counts = recs.groupby(["action_type", "priority"]).size().reset_index(name="count")
    lines = [
        "# BusinessRecommendation Records",
        "",
        "Generated from the Olist analysis layer and the e-commerce ontology action rules.",
        "",
        "## Summary",
        "",
        f"- Total recommendations: {len(recs)}",
        f"- Generated at: {CREATED_AT}",
        "- Status: all records are `proposed` and require human approval before execution.",
        "",
        "## Counts by Action and Priority",
        "",
        "| Action type | Priority | Count |",
        "|---|---:|---:|",
    ]
    for _, row in counts.iterrows():
        lines.append(f"| {row['action_type']} | {row['priority']} | {int(row['count'])} |")

    lines.extend(["", "## Top Recommendations", ""])
    for _, row in recs.head(20).iterrows():
        lines.append(
            f"- `{row['recommendation_id']}` `{row['action_type']}` -> `{row['target_type']}:{row['target_id']}` "
            f"[{row['priority']}]: {row['reason']} Evidence: {row['evidence_summary']}"
        )

    lines.extend(
        [
            "",
            "## Files",
            "",
            f"- CSV: `{OUT_CSV.relative_to(ROOT)}`",
            f"- Lark batch JSON: `{OUT_JSON.relative_to(ROOT)}`",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs(recs: pd.DataFrame) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    recs.to_csv(OUT_CSV, index=False)
    batch = {
        "fields": FIELDS,
        "rows": [
            [clean(row[field]) for field in FIELDS]
            for row in recs[FIELDS].to_dict(orient="records")
        ],
    }
    OUT_JSON.write_text(json.dumps(batch, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(recs)


def main() -> None:
    recs = build_recommendations()
    write_outputs(recs)
    print(f"Generated {len(recs)} BusinessRecommendation records")
    print(f"- {OUT_CSV}")
    print(f"- {OUT_MD}")
    print(f"- {OUT_JSON}")


if __name__ == "__main__":
    main()
