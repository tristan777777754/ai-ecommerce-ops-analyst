#!/usr/bin/env python3
"""Build derived analysis tables for Lark Base import.

This script creates the staging workbook for the Lark-operated analysis layer.
It is not the final product and does not replace Lark Base. Its purpose is to
materialize derived tables that the AI agent imports into Lark for multi-
dimensional analysis, views, and dashboards.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from openpyxl import Workbook


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset"
OUT_DIR = ROOT / "outputs" / "lark_import_staging"
OUT_FILE = OUT_DIR / "olist_analysis_layer_for_lark_base.xlsx"


def read_csv(name: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(DATASET / name, low_memory=False, **kwargs)


def score_quantile(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    ranked = series.rank(method="first")
    try:
        scored = pd.qcut(ranked, 5, labels=[1, 2, 3, 4, 5])
    except ValueError:
        scored = pd.cut(ranked, 5, labels=[1, 2, 3, 4, 5], include_lowest=True)
    scored = scored.astype(int)
    return scored if higher_is_better else 6 - scored


def clean_for_excel(value):
    if pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime().replace(tzinfo=None)
    if isinstance(value, np.generic):
        return value.item()
    return value


def write_sheet(workbook: Workbook, sheet_name: str, frame: pd.DataFrame) -> None:
    sheet = workbook.create_sheet(sheet_name)
    sheet.append(list(frame.columns))
    for row in frame.itertuples(index=False, name=None):
        sheet.append([clean_for_excel(value) for value in row])
    print(f"{sheet_name}: {len(frame):,} rows")


def percent(series: pd.Series) -> pd.Series:
    return series.fillna(0).astype(float)


def pareto_frame(
    frame: pd.DataFrame,
    group_col: str,
    extra_aggs: dict | None = None,
    top_n: int | None = None,
) -> pd.DataFrame:
    aggs = {"revenue": "sum", "order_id": "nunique"}
    if extra_aggs:
        aggs.update(extra_aggs)
    out = frame.groupby(group_col, dropna=False).agg(aggs).reset_index()
    out = out.rename(columns={"order_id": "orders"})
    out["revenue"] = out["revenue"].fillna(0)
    out = out.sort_values("revenue", ascending=False)
    total = out["revenue"].sum()
    out["revenue_share"] = np.where(total > 0, out["revenue"] / total, 0)
    out["cumulative_revenue"] = out["revenue"].cumsum()
    out["cumulative_share"] = np.where(total > 0, out["cumulative_revenue"] / total, 0)
    out["pareto_band"] = np.where(out["cumulative_share"] <= 0.80, "top_80_percent_revenue", "long_tail")
    out["rank"] = np.arange(1, len(out) + 1)
    if top_n:
        out = out.head(top_n)
    return out


def load_data() -> dict[str, pd.DataFrame]:
    customers = read_csv("olist_customers_dataset.csv")
    orders = read_csv(
        "olist_orders_dataset.csv",
        parse_dates=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )
    items = read_csv("olist_order_items_dataset.csv", parse_dates=["shipping_limit_date"])
    payments = read_csv("olist_order_payments_dataset.csv")
    reviews = read_csv(
        "olist_order_reviews_dataset.csv",
        parse_dates=["review_creation_date", "review_answer_timestamp"],
    )
    products = read_csv("olist_products_dataset.csv")
    sellers = read_csv("olist_sellers_dataset.csv")
    category_translation = read_csv("product_category_name_translation.csv")

    products = products.merge(category_translation, on="product_category_name", how="left")
    products["category_name"] = products["product_category_name_english"].fillna(
        products["product_category_name"]
    )

    return {
        "customers": customers,
        "orders": orders,
        "items": items,
        "payments": payments,
        "reviews": reviews,
        "products": products,
        "sellers": sellers,
    }


def build_model(data: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    customers = data["customers"]
    orders = data["orders"]
    items = data["items"]
    payments = data["payments"]
    reviews = data["reviews"]
    products = data["products"]
    sellers = data["sellers"]

    payments_order = (
        payments.groupby("order_id")
        .agg(
            payment_value=("payment_value", "sum"),
            payment_count=("payment_sequential", "count"),
            max_installments=("payment_installments", "max"),
            payment_types=("payment_type", lambda values: ", ".join(sorted(set(map(str, values))))),
        )
        .reset_index()
    )

    review_order = (
        reviews.groupby("order_id")
        .agg(
            review_count=("review_id", "count"),
            avg_review_score=("review_score", "mean"),
            min_review_score=("review_score", "min"),
            low_review_flag=("review_score", lambda values: bool((values <= 2).any())),
            has_review_comment=("review_comment_message", lambda values: bool(values.notna().any())),
        )
        .reset_index()
    )

    item_enriched = (
        items.merge(products[["product_id", "category_name"]], on="product_id", how="left")
        .merge(sellers[["seller_id", "seller_city", "seller_state"]], on="seller_id", how="left")
        .merge(
            orders[
                [
                    "order_id",
                    "order_status",
                    "order_purchase_timestamp",
                    "order_delivered_customer_date",
                    "order_estimated_delivery_date",
                ]
            ],
            on="order_id",
            how="left",
        )
        .merge(review_order[["order_id", "avg_review_score", "low_review_flag"]], on="order_id", how="left")
    )
    item_enriched["price"] = item_enriched["price"].fillna(0)
    item_enriched["freight_value"] = item_enriched["freight_value"].fillna(0)
    item_enriched["revenue"] = item_enriched["price"]
    item_enriched["total_with_freight"] = item_enriched["price"] + item_enriched["freight_value"]
    item_enriched["delivery_delay_days"] = (
        item_enriched["order_delivered_customer_date"] - item_enriched["order_estimated_delivery_date"]
    ).dt.days
    item_enriched["late_delivery_flag"] = item_enriched["delivery_delay_days"] > 0
    item_enriched["low_review_flag"] = item_enriched["low_review_flag"].fillna(False).astype(bool)

    item_order = (
        item_enriched.groupby("order_id")
        .agg(
            item_count=("order_item_id", "count"),
            item_revenue=("revenue", "sum"),
            freight_value=("freight_value", "sum"),
            total_with_freight=("total_with_freight", "sum"),
            distinct_products=("product_id", "nunique"),
            distinct_sellers=("seller_id", "nunique"),
            primary_category=("category_name", lambda values: values.dropna().mode().iat[0] if not values.dropna().mode().empty else None),
        )
        .reset_index()
    )

    order_facts = (
        orders.merge(customers, on="customer_id", how="left")
        .merge(payments_order, on="order_id", how="left")
        .merge(item_order, on="order_id", how="left")
        .merge(review_order, on="order_id", how="left")
    )
    order_facts["revenue"] = order_facts["payment_value"].fillna(order_facts["total_with_freight"]).fillna(0)
    order_facts["order_month"] = order_facts["order_purchase_timestamp"].dt.to_period("M").astype(str)
    order_facts["delivery_days"] = (
        order_facts["order_delivered_customer_date"] - order_facts["order_purchase_timestamp"]
    ).dt.days
    order_facts["delivery_delay_days"] = (
        order_facts["order_delivered_customer_date"] - order_facts["order_estimated_delivery_date"]
    ).dt.days
    order_facts["late_delivery_flag"] = order_facts["delivery_delay_days"] > 0
    order_facts["low_review_flag"] = order_facts["low_review_flag"].fillna(False).astype(bool)
    order_facts["delivered_flag"] = order_facts["order_status"].eq("delivered")

    return {
        "order_facts": order_facts,
        "item_enriched": item_enriched,
    }


def build_rfm(order_facts: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    eligible = order_facts[
        order_facts["order_purchase_timestamp"].notna()
        & order_facts["customer_unique_id"].notna()
        & order_facts["order_status"].isin(["delivered", "shipped", "invoiced", "processing"])
    ].copy()
    snapshot_date = eligible["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
    rfm = (
        eligible.groupby("customer_unique_id")
        .agg(
            first_purchase_date=("order_purchase_timestamp", "min"),
            last_purchase_date=("order_purchase_timestamp", "max"),
            frequency=("order_id", "nunique"),
            monetary_value=("revenue", "sum"),
            avg_order_value=("revenue", "mean"),
            customer_state=("customer_state", lambda values: values.mode().iat[0] if not values.mode().empty else None),
            customer_city=("customer_city", lambda values: values.mode().iat[0] if not values.mode().empty else None),
        )
        .reset_index()
    )
    rfm["recency_days"] = (snapshot_date - rfm["last_purchase_date"]).dt.days
    rfm["r_score"] = score_quantile(rfm["recency_days"], higher_is_better=False)
    rfm["f_score"] = score_quantile(rfm["frequency"], higher_is_better=True)
    rfm["m_score"] = score_quantile(rfm["monetary_value"], higher_is_better=True)
    rfm["rfm_score"] = rfm["r_score"] * 100 + rfm["f_score"] * 10 + rfm["m_score"]

    def segment(row) -> str:
        if row.r_score >= 4 and row.f_score >= 4 and row.m_score >= 4:
            return "Champions"
        if row.r_score >= 3 and row.f_score >= 4 and row.m_score >= 4:
            return "Loyal High Value"
        if row.r_score >= 4 and row.frequency <= 2:
            return "New / Recent"
        if row.r_score <= 2 and row.m_score >= 4:
            return "Dormant High Value"
        if row.r_score <= 2 and row.f_score >= 3:
            return "At Risk"
        if row.r_score == 3 and row.m_score >= 3:
            return "Needs Attention"
        return "Low Value / Occasional"

    rfm["rfm_segment"] = rfm.apply(segment, axis=1)
    rfm["churn_risk_score"] = (
        (rfm["recency_days"].rank(pct=True) * 60)
        + ((6 - rfm["f_score"]) / 5 * 20)
        + (rfm["m_score"] / 5 * 20)
    ).round(1)

    segment_summary = (
        rfm.groupby("rfm_segment")
        .agg(
            customers=("customer_unique_id", "count"),
            revenue=("monetary_value", "sum"),
            avg_recency_days=("recency_days", "mean"),
            avg_frequency=("frequency", "mean"),
            avg_monetary_value=("monetary_value", "mean"),
            avg_churn_risk_score=("churn_risk_score", "mean"),
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    total_revenue = segment_summary["revenue"].sum()
    segment_summary["revenue_share"] = np.where(total_revenue > 0, segment_summary["revenue"] / total_revenue, 0)

    dormant = (
        rfm[rfm["rfm_segment"].eq("Dormant High Value")]
        .sort_values(["monetary_value", "recency_days"], ascending=[False, False])
        .head(1000)
        .copy()
    )
    dormant["recommended_action"] = "SendReactivationOffer"
    dormant["reason"] = "High historical value and long inactivity signal a winback opportunity."

    return rfm, segment_summary, dormant


def build_monthly_trend(order_facts: pd.DataFrame) -> pd.DataFrame:
    trend = (
        order_facts.groupby("order_month")
        .agg(
            orders=("order_id", "nunique"),
            customers=("customer_unique_id", "nunique"),
            revenue=("revenue", "sum"),
            avg_order_value=("revenue", "mean"),
            delivered_orders=("delivered_flag", "sum"),
            late_delivery_rate=("late_delivery_flag", "mean"),
            avg_delivery_delay_days=("delivery_delay_days", "mean"),
            avg_review_score=("avg_review_score", "mean"),
            low_review_rate=("low_review_flag", "mean"),
        )
        .reset_index()
        .sort_values("order_month")
    )
    trend["revenue_growth_mom"] = trend["revenue"].pct_change()
    trend["orders_growth_mom"] = trend["orders"].pct_change()
    return trend


def build_seller_performance(item_enriched: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    seller = (
        item_enriched.groupby(["seller_id", "seller_city", "seller_state"], dropna=False)
        .agg(
            orders=("order_id", "nunique"),
            items=("order_item_id", "count"),
            revenue=("revenue", "sum"),
            freight_value=("freight_value", "sum"),
            avg_review_score=("avg_review_score", "mean"),
            low_review_rate=("low_review_flag", "mean"),
            late_delivery_rate=("late_delivery_flag", "mean"),
            avg_delivery_delay_days=("delivery_delay_days", "mean"),
        )
        .reset_index()
    )
    seller["seller_reliability_score"] = (
        100
        - percent(seller["late_delivery_rate"]) * 45
        - percent(seller["low_review_rate"]) * 45
        + ((seller["avg_review_score"].fillna(4) - 4) * 5)
    ).clip(0, 100).round(1)
    seller["risk_band"] = np.select(
        [
            (seller["orders"] >= 50)
            & ((seller["late_delivery_rate"] >= 0.25) | (seller["low_review_rate"] >= 0.30) | (seller["seller_reliability_score"] <= 65)),
            (seller["orders"] >= 30)
            & ((seller["late_delivery_rate"] >= 0.15) | (seller["low_review_rate"] >= 0.18) | (seller["seller_reliability_score"] <= 75)),
        ],
        ["High", "Medium"],
        default="Low",
    )
    seller = seller.sort_values(["risk_band", "seller_reliability_score", "revenue"], ascending=[True, True, False])
    risk_watchlist = seller[seller["risk_band"].isin(["High", "Medium"])].head(250).copy()
    risk_watchlist["recommended_action"] = np.where(
        risk_watchlist["risk_band"].eq("High"), "DeprioritizeRiskySeller", "InvestigateSeller"
    )
    risk_watchlist["reason"] = "Meaningful order volume with elevated late delivery, low review rate, or low reliability score."
    return seller, risk_watchlist


def build_category_tables(item_enriched: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    category = pareto_frame(
        item_enriched,
        "category_name",
        extra_aggs={
            "product_id": "nunique",
            "avg_review_score": "mean",
            "low_review_flag": "mean",
            "late_delivery_flag": "mean",
            "delivery_delay_days": "mean",
        },
    )
    category = category.rename(
        columns={
            "product_id": "products",
            "low_review_flag": "low_review_rate",
            "late_delivery_flag": "late_delivery_rate",
            "delivery_delay_days": "avg_delivery_delay_days",
        }
    )
    review_risk = (
        category[(category["orders"] >= 100) & (category["low_review_rate"] >= 0.15)]
        .sort_values(["low_review_rate", "revenue"], ascending=[False, False])
        .copy()
    )
    review_risk["risk_id"] = ["REV-CAT-" + str(i).zfill(4) for i in range(1, len(review_risk) + 1)]
    review_risk["target_type"] = "ProductCategory"
    review_risk["target_id"] = review_risk["category_name"]
    review_risk["priority"] = np.where(
        (review_risk["revenue"] >= 100000) & (review_risk["low_review_rate"] >= 0.20), "High", "Medium"
    )
    review_risk["recommended_action"] = "InvestigateLowReviewProductCategory"

    category_opportunity = (
        category[category["pareto_band"].eq("top_80_percent_revenue")]
        .sort_values("revenue", ascending=False)
        .copy()
    )
    category_opportunity["recommended_action"] = np.where(
        category_opportunity["low_review_rate"] < 0.15,
        "PromoteHighRevenueCategory",
        "ProtectRevenueButInvestigateRisk",
    )
    return category, review_risk, category_opportunity


def build_delivery_risk(order_facts: pd.DataFrame) -> pd.DataFrame:
    delivery = (
        order_facts.groupby("customer_state", dropna=False)
        .agg(
            orders=("order_id", "nunique"),
            revenue=("revenue", "sum"),
            late_delivery_rate=("late_delivery_flag", "mean"),
            avg_delay_days=("delivery_delay_days", "mean"),
            avg_delivery_days=("delivery_days", "mean"),
            low_review_rate=("low_review_flag", "mean"),
        )
        .reset_index()
        .rename(columns={"customer_state": "target_id"})
    )
    delivery["target_type"] = "GeographyState"
    delivery = delivery[(delivery["orders"] >= 100) & (delivery["late_delivery_rate"] >= 0.12)].copy()
    delivery = delivery.sort_values(["late_delivery_rate", "orders"], ascending=[False, False])
    delivery["risk_id"] = ["DEL-STATE-" + str(i).zfill(4) for i in range(1, len(delivery) + 1)]
    delivery["priority"] = np.where(
        (delivery["orders"] >= 500) & (delivery["late_delivery_rate"] >= 0.15), "High", "Medium"
    )
    delivery["recommended_action"] = "MonitorDeliveryRisk"
    return delivery


def build_product_performance(item_enriched: pd.DataFrame) -> pd.DataFrame:
    product = (
        item_enriched.groupby(["product_id", "category_name"], dropna=False)
        .agg(
            orders=("order_id", "nunique"),
            items=("order_item_id", "count"),
            sellers=("seller_id", "nunique"),
            revenue=("revenue", "sum"),
            avg_review_score=("avg_review_score", "mean"),
            low_review_rate=("low_review_flag", "mean"),
            late_delivery_rate=("late_delivery_flag", "mean"),
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
        .head(1000)
    )
    return product


def build_executive_summary(
    order_facts: pd.DataFrame,
    rfm: pd.DataFrame,
    seller: pd.DataFrame,
    category: pd.DataFrame,
    delivery_risk: pd.DataFrame,
    review_risk: pd.DataFrame,
) -> pd.DataFrame:
    total_revenue = order_facts["revenue"].sum()
    total_orders = order_facts["order_id"].nunique()
    low_review_rate = order_facts["low_review_flag"].mean()
    late_delivery_rate = order_facts["late_delivery_flag"].mean()
    dormant = rfm[rfm["rfm_segment"].eq("Dormant High Value")]
    metrics = [
        ("Total revenue", total_revenue, "Revenue across all orders"),
        ("Total orders", total_orders, "Unique orders"),
        ("Unique customers", rfm["customer_unique_id"].nunique(), "Customer identities by customer_unique_id"),
        ("Average order value", total_revenue / total_orders if total_orders else 0, "Total revenue / orders"),
        ("Late delivery rate", late_delivery_rate, "Orders delivered after estimated date"),
        ("Low review rate", low_review_rate, "Orders with at least one review score <= 2"),
        ("Dormant high-value customers", len(dormant), "RFM segment count"),
        ("High/medium seller risks", seller["risk_band"].isin(["High", "Medium"]).sum(), "Seller risk watchlist population"),
        ("Delivery risk geographies", len(delivery_risk), "States meeting delivery risk threshold"),
        ("Review risk categories", len(review_risk), "Categories meeting low-review threshold"),
        ("Categories reaching 80% revenue", int((category["pareto_band"] == "top_80_percent_revenue").sum()), "Category revenue concentration"),
    ]
    return pd.DataFrame(metrics, columns=["metric", "value", "meaning"])


def round_numeric(frames: Iterable[pd.DataFrame]) -> None:
    for frame in frames:
        for col in frame.select_dtypes(include=["float"]).columns:
            frame[col] = frame[col].round(4)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = load_data()
    model = build_model(data)
    order_facts = model["order_facts"]
    item_enriched = model["item_enriched"]

    rfm, rfm_summary, dormant = build_rfm(order_facts)
    monthly = build_monthly_trend(order_facts)
    seller, seller_risk = build_seller_performance(item_enriched)
    category, review_risk, category_opportunity = build_category_tables(item_enriched)
    delivery_risk = build_delivery_risk(order_facts)
    product_performance = build_product_performance(item_enriched)
    executive = build_executive_summary(order_facts, rfm, seller, category, delivery_risk, review_risk)

    order_facts_export = order_facts[
        [
            "order_id",
            "customer_id",
            "customer_unique_id",
            "customer_state",
            "customer_city",
            "order_status",
            "order_purchase_timestamp",
            "order_month",
            "revenue",
            "item_revenue",
            "freight_value",
            "item_count",
            "distinct_products",
            "distinct_sellers",
            "primary_category",
            "avg_review_score",
            "low_review_flag",
            "delivery_days",
            "delivery_delay_days",
            "late_delivery_flag",
        ]
    ].copy()

    frames = [
        executive,
        monthly,
        order_facts_export,
        rfm,
        rfm_summary,
        dormant,
        seller,
        seller_risk,
        category,
        category_opportunity,
        product_performance,
        delivery_risk,
        review_risk,
    ]
    round_numeric(frames)

    workbook = Workbook(write_only=True)
    print(f"Writing {OUT_FILE}")
    write_sheet(workbook, "executive_summary", executive)
    write_sheet(workbook, "monthly_revenue_trend", monthly)
    write_sheet(workbook, "order_facts", order_facts_export)
    write_sheet(workbook, "customer_rfm", rfm)
    write_sheet(workbook, "rfm_segment_summary", rfm_summary)
    write_sheet(workbook, "dormant_high_value", dormant)
    write_sheet(workbook, "seller_performance", seller)
    write_sheet(workbook, "seller_risk_watchlist", seller_risk)
    write_sheet(workbook, "category_performance", category)
    write_sheet(workbook, "category_opportunity", category_opportunity)
    write_sheet(workbook, "product_performance_top", product_performance)
    write_sheet(workbook, "delivery_risk_by_state", delivery_risk)
    write_sheet(workbook, "review_risk_by_category", review_risk)
    workbook.save(OUT_FILE)
    print(f"Saved {OUT_FILE} ({OUT_FILE.stat().st_size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main()
