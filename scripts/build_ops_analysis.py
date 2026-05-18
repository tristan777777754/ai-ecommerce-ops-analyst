from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset"
OUTPUTS = ROOT / "outputs"


def read_csv(name: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(DATASET / name, low_memory=False, **kwargs)


def score_quantile(series: pd.Series, higher_is_better: bool = True, labels=None) -> pd.Series:
    labels = labels or [1, 2, 3, 4, 5]
    ranked = series.rank(method="first")
    try:
        scored = pd.qcut(ranked, 5, labels=labels)
    except ValueError:
        scored = pd.cut(ranked, 5, labels=labels, include_lowest=True)
    scored = scored.astype(int)
    return scored if higher_is_better else 6 - scored


def pareto_frame(
    df: pd.DataFrame,
    group_col: str,
    revenue_col: str = "revenue",
    extra_aggs: dict | None = None,
    top_n: int | None = None,
) -> pd.DataFrame:
    aggs = {revenue_col: "sum"}
    if extra_aggs:
        aggs.update(extra_aggs)
    out = df.groupby(group_col, dropna=False).agg(aggs).reset_index()
    out = out.rename(columns={revenue_col: "revenue"})
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


def make_recommendation(
    action_type: str,
    target_type: str,
    target_id: str,
    priority: str,
    reason: str,
    evidence_metric: str,
) -> dict:
    return {
        "action_type": action_type,
        "target_type": target_type,
        "target_id": target_id,
        "priority": priority,
        "reason": reason,
        "evidence_metric": evidence_metric,
    }


def load_and_model() -> dict[str, pd.DataFrame]:
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

    payments_order = (
        payments.groupby("order_id")
        .agg(
            payment_value=("payment_value", "sum"),
            payment_count=("payment_sequential", "count"),
            max_installments=("payment_installments", "max"),
            payment_types=("payment_type", lambda x: ", ".join(sorted(set(map(str, x))))),
        )
        .reset_index()
    )

    item_enriched = (
        items.merge(products[["product_id", "category_name"]], on="product_id", how="left")
        .merge(sellers[["seller_id", "seller_city", "seller_state"]], on="seller_id", how="left")
        .merge(orders[["order_id", "order_status", "order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"]], on="order_id", how="left")
    )
    item_enriched["item_revenue"] = item_enriched["price"].fillna(0)
    item_enriched["item_total_with_freight"] = item_enriched["price"].fillna(0) + item_enriched[
        "freight_value"
    ].fillna(0)
    item_enriched["delivery_delay_days"] = (
        item_enriched["order_delivered_customer_date"] - item_enriched["order_estimated_delivery_date"]
    ).dt.days
    item_enriched["late_delivery_flag"] = item_enriched["delivery_delay_days"] > 0

    item_order = (
        item_enriched.groupby("order_id")
        .agg(
            item_count=("order_item_id", "count"),
            item_revenue=("item_revenue", "sum"),
            item_total_with_freight=("item_total_with_freight", "sum"),
            freight_value=("freight_value", "sum"),
            distinct_products=("product_id", "nunique"),
            distinct_sellers=("seller_id", "nunique"),
            categories=("category_name", lambda x: ", ".join(sorted(set(map(str, x.dropna()))))[:300]),
        )
        .reset_index()
    )

    review_order = (
        reviews.groupby("order_id")
        .agg(
            review_count=("review_id", "count"),
            avg_review_score=("review_score", "mean"),
            min_review_score=("review_score", "min"),
            low_review_flag=("review_score", lambda x: bool((x <= 2).any())),
            has_review_comment=("review_comment_message", lambda x: bool(x.notna().any())),
        )
        .reset_index()
    )

    order_facts = (
        orders.merge(customers, on="customer_id", how="left")
        .merge(payments_order, on="order_id", how="left")
        .merge(item_order, on="order_id", how="left")
        .merge(review_order, on="order_id", how="left")
    )
    order_facts["revenue"] = order_facts["payment_value"].fillna(order_facts["item_total_with_freight"]).fillna(0)
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
        "customers": customers,
        "orders": orders,
        "items": items,
        "payments": payments,
        "reviews": reviews,
        "products": products,
        "sellers": sellers,
        "item_enriched": item_enriched,
        "order_facts": order_facts,
    }


def build_rfm(order_facts: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    eligible = order_facts[
        order_facts["order_purchase_timestamp"].notna()
        & order_facts["customer_unique_id"].notna()
        & order_facts["order_status"].isin(["delivered", "shipped", "invoiced", "processing"])
    ].copy()
    snapshot_date = eligible["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
    rfm = (
        eligible.groupby("customer_unique_id")
        .agg(
            last_purchase_date=("order_purchase_timestamp", "max"),
            first_purchase_date=("order_purchase_timestamp", "min"),
            frequency=("order_id", "nunique"),
            monetary_value=("revenue", "sum"),
            avg_order_value=("revenue", "mean"),
            customer_state=("customer_state", lambda x: x.mode().iat[0] if not x.mode().empty else ""),
            customer_city=("customer_city", lambda x: x.mode().iat[0] if not x.mode().empty else ""),
        )
        .reset_index()
    )
    rfm["recency_days"] = (snapshot_date - rfm["last_purchase_date"]).dt.days
    rfm["r_score"] = score_quantile(rfm["recency_days"], higher_is_better=False)
    rfm["f_score"] = score_quantile(rfm["frequency"], higher_is_better=True)
    rfm["m_score"] = score_quantile(rfm["monetary_value"], higher_is_better=True)
    rfm["rfm_score"] = rfm["r_score"] * 100 + rfm["f_score"] * 10 + rfm["m_score"]

    def segment(row):
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

    rfm["segment"] = rfm.apply(segment, axis=1)
    rfm["churn_risk_score"] = (
        (rfm["recency_days"].rank(pct=True) * 60)
        + ((6 - rfm["f_score"]) / 5 * 20)
        + (rfm["m_score"] / 5 * 20)
    ).round(1)

    rfm_summary = (
        rfm.groupby("segment")
        .agg(
            customers=("customer_unique_id", "count"),
            avg_recency_days=("recency_days", "mean"),
            avg_frequency=("frequency", "mean"),
            revenue=("monetary_value", "sum"),
            avg_customer_value=("monetary_value", "mean"),
            avg_churn_risk_score=("churn_risk_score", "mean"),
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    total_revenue = rfm_summary["revenue"].sum()
    rfm_summary["revenue_share"] = np.where(total_revenue > 0, rfm_summary["revenue"] / total_revenue, 0)
    for col in ["avg_recency_days", "avg_frequency", "avg_customer_value", "avg_churn_risk_score", "revenue_share"]:
        rfm_summary[col] = rfm_summary[col].round(3)
    return rfm, rfm_summary


def build_trends(order_facts: pd.DataFrame) -> pd.DataFrame:
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
    trend["revenue_mom_pct"] = trend["revenue"].pct_change()
    trend["orders_mom_pct"] = trend["orders"].pct_change()
    numeric_cols = trend.select_dtypes(include=[np.number]).columns
    trend[numeric_cols] = trend[numeric_cols].round(4)
    return trend


def build_seller_performance(item_enriched: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:
    review_scores = reviews[["order_id", "review_score"]].drop_duplicates()
    seller_items = item_enriched.merge(review_scores, on="order_id", how="left")
    seller = (
        seller_items.groupby("seller_id")
        .agg(
            seller_city=("seller_city", "first"),
            seller_state=("seller_state", "first"),
            orders=("order_id", "nunique"),
            items=("order_item_id", "count"),
            revenue=("item_revenue", "sum"),
            freight_value=("freight_value", "sum"),
            avg_review_score=("review_score", "mean"),
            low_review_rate=("review_score", lambda x: (x <= 2).mean()),
            late_delivery_rate=("late_delivery_flag", "mean"),
            avg_delivery_delay_days=("delivery_delay_days", "mean"),
        )
        .reset_index()
    )
    seller["seller_reliability_score"] = (
        100
        - seller["late_delivery_rate"].fillna(0) * 45
        - seller["low_review_rate"].fillna(0) * 35
        + ((seller["avg_review_score"].fillna(0) - 3) / 2) * 20
    ).clip(0, 100)
    seller["risk_band"] = pd.cut(
        seller["seller_reliability_score"],
        bins=[-1, 50, 70, 85, 101],
        labels=["High Risk", "Monitor", "Reliable", "Excellent"],
    ).astype(str)
    numeric_cols = seller.select_dtypes(include=[np.number]).columns
    seller[numeric_cols] = seller[numeric_cols].round(4)
    return seller.sort_values(["risk_band", "revenue"], ascending=[True, False])


def build_delivery_risk(order_facts: pd.DataFrame, item_enriched: pd.DataFrame) -> dict[str, pd.DataFrame]:
    delivered = order_facts[order_facts["order_delivered_customer_date"].notna()].copy()
    by_state = (
        delivered.groupby("customer_state")
        .agg(
            orders=("order_id", "nunique"),
            revenue=("revenue", "sum"),
            late_delivery_rate=("late_delivery_flag", "mean"),
            avg_delay_days=("delivery_delay_days", "mean"),
            p90_delay_days=("delivery_delay_days", lambda x: x.quantile(0.9)),
            avg_review_score=("avg_review_score", "mean"),
        )
        .reset_index()
        .sort_values(["late_delivery_rate", "orders"], ascending=[False, False])
    )

    category_items = item_enriched[item_enriched["order_delivered_customer_date"].notna()].copy()
    by_category = (
        category_items.groupby("category_name", dropna=False)
        .agg(
            orders=("order_id", "nunique"),
            revenue=("item_revenue", "sum"),
            late_delivery_rate=("late_delivery_flag", "mean"),
            avg_delay_days=("delivery_delay_days", "mean"),
        )
        .reset_index()
        .sort_values(["late_delivery_rate", "orders"], ascending=[False, False])
    )

    for df in [by_state, by_category]:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].round(4)
    return {"delivery_by_state": by_state, "delivery_by_category": by_category}


def build_review_risk(item_enriched: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:
    review_items = item_enriched.merge(reviews[["order_id", "review_score", "review_comment_message"]], on="order_id", how="left")
    review_risk = (
        review_items.groupby("category_name", dropna=False)
        .agg(
            orders=("order_id", "nunique"),
            revenue=("item_revenue", "sum"),
            avg_review_score=("review_score", "mean"),
            low_review_rate=("review_score", lambda x: (x <= 2).mean()),
            review_count=("review_score", "count"),
            comment_rate=("review_comment_message", lambda x: x.notna().mean()),
        )
        .reset_index()
    )
    review_risk["review_risk_score"] = (
        review_risk["low_review_rate"].fillna(0) * 70
        + (1 - (review_risk["avg_review_score"].fillna(5) / 5)) * 30
    ).round(2)
    numeric_cols = review_risk.select_dtypes(include=[np.number]).columns
    review_risk[numeric_cols] = review_risk[numeric_cols].round(4)
    return review_risk.sort_values(["review_risk_score", "revenue"], ascending=[False, False])


def build_recommendations(
    rfm: pd.DataFrame,
    seller_perf: pd.DataFrame,
    category_pareto: pd.DataFrame,
    review_risk: pd.DataFrame,
    delivery_by_state: pd.DataFrame,
) -> pd.DataFrame:
    recommendations = []

    dormant = rfm[rfm["segment"].eq("Dormant High Value")].sort_values("monetary_value", ascending=False).head(20)
    for _, row in dormant.iterrows():
        recommendations.append(
            make_recommendation(
                "SendReactivationOffer",
                "Customer",
                row["customer_unique_id"],
                "High",
                "High-value customer has become inactive.",
                f"monetary_value={row['monetary_value']:.2f}; recency_days={row['recency_days']}",
            )
        )

    risky_sellers = seller_perf[
        (seller_perf["orders"] >= 30)
        & ((seller_perf["late_delivery_rate"] >= 0.15) | (seller_perf["low_review_rate"] >= 0.18))
    ].sort_values(["revenue", "late_delivery_rate"], ascending=[False, False]).head(20)
    for _, row in risky_sellers.iterrows():
        recommendations.append(
            make_recommendation(
                "InvestigateSeller",
                "Seller",
                row["seller_id"],
                "High" if row["seller_reliability_score"] < 60 else "Medium",
                "Seller has meaningful volume and elevated fulfillment or review risk.",
                f"orders={int(row['orders'])}; late_delivery_rate={row['late_delivery_rate']:.2%}; low_review_rate={row['low_review_rate']:.2%}",
            )
        )

    risky_categories = review_risk[(review_risk["orders"] >= 100) & (review_risk["low_review_rate"] >= 0.15)].head(15)
    for _, row in risky_categories.iterrows():
        recommendations.append(
            make_recommendation(
                "InvestigateLowReviewProductCategory",
                "ProductCategory",
                str(row["category_name"]),
                "Medium",
                "Category has enough order volume and a high low-review rate.",
                f"orders={int(row['orders'])}; low_review_rate={row['low_review_rate']:.2%}; avg_review_score={row['avg_review_score']:.2f}",
            )
        )

    strong_categories = category_pareto[
        category_pareto["pareto_band"].eq("top_80_percent_revenue")
    ].head(10)
    for _, row in strong_categories.iterrows():
        recommendations.append(
            make_recommendation(
                "PromoteHighRevenueCategory",
                "ProductCategory",
                str(row["category_name"]),
                "Medium",
                "Category is part of the revenue-driving Pareto set.",
                f"revenue={row['revenue']:.2f}; cumulative_share={row['cumulative_share']:.2%}",
            )
        )

    late_states = delivery_by_state[(delivery_by_state["orders"] >= 100) & (delivery_by_state["late_delivery_rate"] >= 0.12)].head(10)
    for _, row in late_states.iterrows():
        recommendations.append(
            make_recommendation(
                "MonitorDeliveryRisk",
                "Geography",
                str(row["customer_state"]),
                "Medium",
                "Customer state has elevated delivery delay risk.",
                f"orders={int(row['orders'])}; late_delivery_rate={row['late_delivery_rate']:.2%}; avg_delay_days={row['avg_delay_days']:.2f}",
            )
        )

    recs = pd.DataFrame(recommendations)
    if not recs.empty:
        recs.insert(0, "recommendation_id", [f"REC-{i:04d}" for i in range(1, len(recs) + 1)])
    return recs


def write_outputs(results: dict[str, pd.DataFrame]) -> None:
    OUTPUTS.mkdir(exist_ok=True)
    workbook = OUTPUTS / "olist_ecommerce_ops_analysis.xlsx"
    with pd.ExcelWriter(workbook, engine="openpyxl") as writer:
        sheet_map = {
            "Executive Summary": results["executive_summary"],
            "Monthly Trends": results["monthly_trends"],
            "RFM Customers Top": results["rfm_customers_top"],
            "RFM Segment Summary": results["rfm_segment_summary"],
            "Pareto Categories": results["pareto_categories"],
            "Pareto Products": results["pareto_products"],
            "Pareto Sellers": results["pareto_sellers"],
            "Seller Performance": results["seller_performance_top"],
            "Seller Risk Watchlist": results["seller_performance_watchlist"],
            "Delivery By State": results["delivery_by_state"],
            "Delivery By Category": results["delivery_by_category"],
            "Review Risk": results["review_risk"],
            "Recommendations": results["recommendations"],
        }
        for sheet, df in sheet_map.items():
            df.to_excel(writer, index=False, sheet_name=sheet[:31])

    results["order_facts_sample"].to_csv(OUTPUTS / "order_facts_sample.csv", index=False)
    results["rfm_all"].to_csv(OUTPUTS / "customer_rfm.csv", index=False)
    results["seller_performance_all"].to_csv(OUTPUTS / "seller_performance.csv", index=False)

    report = build_markdown_report(results, workbook)
    (OUTPUTS / "OPS_ANALYSIS_REPORT.md").write_text(report, encoding="utf-8")


def build_markdown_report(results: dict[str, pd.DataFrame], workbook: Path) -> str:
    summary = results["executive_summary"]
    metrics = dict(zip(summary["metric"], summary["value"]))
    category_top = results["pareto_categories"].head(5)
    seller_risk = results["seller_performance_watchlist"].head(5)
    recs = results["recommendations"].head(12)

    lines = [
        "# Olist E-commerce Ops Analysis",
        "",
        "This report turns the Olist dataset into first-version operational functions for an AI e-commerce ops ontology: customer segmentation, revenue concentration, trend monitoring, seller reliability, delivery risk, review risk, and recommended actions.",
        "",
        "## Executive Summary",
        "",
    ]
    for _, row in summary.iterrows():
        lines.append(f"- **{row['metric']}**: {row['value']} ({row['note']})")

    lines.extend(["", "## Top Revenue Categories", ""])
    for _, row in category_top.iterrows():
        lines.append(
            f"- `{row['category_name']}`: revenue {row['revenue']:.2f}, share {row['revenue_share']:.2%}, cumulative share {row['cumulative_share']:.2%}."
        )

    lines.extend(["", "## Seller Risk Watchlist", ""])
    for _, row in seller_risk.iterrows():
        lines.append(
            f"- `{row['seller_id']}`: reliability {row['seller_reliability_score']:.1f}, revenue {row['revenue']:.2f}, late delivery {row['late_delivery_rate']:.2%}, low review {row['low_review_rate']:.2%}."
        )

    lines.extend(["", "## Example Recommended Actions", ""])
    for _, row in recs.iterrows():
        lines.append(
            f"- `{row['action_type']}` for `{row['target_type']}:{row['target_id']}` [{row['priority']}]: {row['reason']} Evidence: {row['evidence_metric']}."
        )

    lines.extend(
        [
            "",
            "## Generated Files",
            "",
            f"- Analysis workbook for Lark Base import: `{workbook.relative_to(ROOT)}`",
            "- Customer RFM table: `outputs/customer_rfm.csv`",
            "- Seller performance table: `outputs/seller_performance.csv`",
            "- Order facts sample: `outputs/order_facts_sample.csv`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    data = load_and_model()
    order_facts = data["order_facts"]
    item_enriched = data["item_enriched"]

    rfm, rfm_summary = build_rfm(order_facts)
    monthly_trends = build_trends(order_facts)

    category_source = item_enriched.copy()
    category_pareto = pareto_frame(
        category_source,
        "category_name",
        revenue_col="item_revenue",
        extra_aggs={"order_id": "nunique", "product_id": "nunique"},
    ).rename(columns={"order_id": "orders", "product_id": "products"})
    product_pareto = pareto_frame(
        item_enriched,
        "product_id",
        revenue_col="item_revenue",
        extra_aggs={"order_id": "nunique"},
        top_n=100,
    ).rename(columns={"order_id": "orders"})
    seller_pareto = pareto_frame(
        item_enriched,
        "seller_id",
        revenue_col="item_revenue",
        extra_aggs={"order_id": "nunique"},
    ).rename(columns={"order_id": "orders"})

    seller_performance = build_seller_performance(item_enriched, data["reviews"])
    delivery = build_delivery_risk(order_facts, item_enriched)
    review_risk = build_review_risk(item_enriched, data["reviews"])
    recommendations = build_recommendations(
        rfm, seller_performance, category_pareto, review_risk, delivery["delivery_by_state"]
    )

    total_revenue = float(order_facts["revenue"].sum())
    total_orders = int(order_facts["order_id"].nunique())
    total_customers = int(order_facts["customer_unique_id"].nunique())
    avg_order_value = float(order_facts["revenue"].mean())
    late_delivery_rate = float(order_facts["late_delivery_flag"].mean())
    low_review_rate = float(order_facts["low_review_flag"].mean())
    top_category_count = int((category_pareto["cumulative_share"] <= 0.8).sum())
    top_seller_count = int((seller_pareto["cumulative_share"] <= 0.8).sum())
    dormant_hv = int((rfm["segment"] == "Dormant High Value").sum())

    executive_summary = pd.DataFrame(
        [
            {"metric": "Total revenue", "value": round(total_revenue, 2), "note": "Uses payment value where available, otherwise item total with freight."},
            {"metric": "Total orders", "value": total_orders, "note": "Unique order_id count."},
            {"metric": "Unique customers", "value": total_customers, "note": "Unique customer_unique_id count."},
            {"metric": "Average order value", "value": round(avg_order_value, 2), "note": "Mean revenue per order row."},
            {"metric": "Late delivery rate", "value": round(late_delivery_rate, 4), "note": "Orders delivered after estimated delivery date."},
            {"metric": "Low review rate", "value": round(low_review_rate, 4), "note": "Orders with any review score <= 2."},
            {"metric": "Categories to reach 80% revenue", "value": top_category_count, "note": "Pareto concentration by product category."},
            {"metric": "Sellers to reach 80% revenue", "value": top_seller_count, "note": "Pareto concentration by seller."},
            {"metric": "Dormant high-value customers", "value": dormant_hv, "note": "RFM segment for winback actions."},
            {"metric": "Generated recommendations", "value": len(recommendations), "note": "Rule-based first pass over ontology functions."},
        ]
    )

    results = {
        "executive_summary": executive_summary,
        "monthly_trends": monthly_trends,
        "rfm_all": rfm,
        "rfm_customers_top": rfm.sort_values(["monetary_value", "churn_risk_score"], ascending=[False, False]).head(500),
        "rfm_segment_summary": rfm_summary,
        "pareto_categories": category_pareto,
        "pareto_products": product_pareto,
        "pareto_sellers": seller_pareto,
        "seller_performance_all": seller_performance,
        "seller_performance_top": seller_performance.sort_values("revenue", ascending=False).head(500),
        "seller_performance_watchlist": seller_performance[
            seller_performance["orders"] >= 30
        ].sort_values(["seller_reliability_score", "revenue"], ascending=[True, False]).head(500),
        "delivery_by_state": delivery["delivery_by_state"],
        "delivery_by_category": delivery["delivery_by_category"],
        "review_risk": review_risk,
        "recommendations": recommendations,
        "order_facts_sample": order_facts.head(5000),
    }
    write_outputs(results)

    print("Generated outputs:")
    print(f"- {OUTPUTS / 'olist_ecommerce_ops_analysis.xlsx'}")
    print(f"- {OUTPUTS / 'OPS_ANALYSIS_REPORT.md'}")
    print(f"- {OUTPUTS / 'customer_rfm.csv'}")
    print(f"- {OUTPUTS / 'seller_performance.csv'}")
    print(f"- {OUTPUTS / 'order_facts_sample.csv'}")


if __name__ == "__main__":
    main()
