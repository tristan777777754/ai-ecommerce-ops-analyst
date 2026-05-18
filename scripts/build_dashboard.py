from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
WORKBOOK = OUTPUTS / "olist_ecommerce_ops_analysis.xlsx"
DASHBOARD = OUTPUTS / "ops_dashboard.html"


COLOR = {
    "ink": "#17202a",
    "muted": "#5b6472",
    "line": "#d9dee7",
    "panel": "#ffffff",
    "page": "#f6f7f9",
    "blue": "#2f6fed",
    "teal": "#0f9f8f",
    "green": "#2e9d58",
    "amber": "#d99028",
    "red": "#cf4d45",
    "violet": "#7b61c9",
}


def money(value: float) -> str:
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.0f}"


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def read_sheet(sheet: str) -> pd.DataFrame:
    return pd.read_excel(WORKBOOK, sheet_name=sheet)


def fig_html(fig: go.Figure, include_plotlyjs: bool | str = False) -> str:
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=48, r=28, t=72, b=46),
        font=dict(family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        title=dict(font=dict(size=16), y=0.96),
        legend=dict(orientation="h", yanchor="bottom", y=1.07, xanchor="left", x=0),
        hoverlabel=dict(bgcolor="#17202a", font_color="#ffffff"),
    )
    fig.update_xaxes(showgrid=False, linecolor=COLOR["line"], tickfont=dict(color=COLOR["muted"]))
    fig.update_yaxes(gridcolor="#edf0f4", linecolor=COLOR["line"], tickfont=dict(color=COLOR["muted"]))
    return fig.to_html(
        full_html=False,
        include_plotlyjs=include_plotlyjs,
        config={"displayModeBar": False, "responsive": True},
    )


def revenue_orders_chart(monthly: pd.DataFrame) -> str:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=monthly["order_month"],
            y=monthly["revenue"],
            name="Revenue",
            marker_color=COLOR["blue"],
            hovertemplate="%{x}<br>Revenue: $%{y:,.0f}<extra></extra>",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=monthly["order_month"],
            y=monthly["orders"],
            name="Orders",
            mode="lines+markers",
            line=dict(color=COLOR["teal"], width=3),
            marker=dict(size=6),
            hovertemplate="%{x}<br>Orders: %{y:,.0f}<extra></extra>",
        ),
        secondary_y=True,
    )
    fig.update_layout(title="Revenue and Orders")
    fig.update_yaxes(title_text="Revenue", tickprefix="$", secondary_y=False)
    fig.update_yaxes(title_text="Orders", secondary_y=True, showgrid=False)
    return fig_html(fig, include_plotlyjs=True)


def risk_trend_chart(monthly: pd.DataFrame) -> str:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=monthly["order_month"],
            y=monthly["late_delivery_rate"],
            name="Late Delivery Rate",
            mode="lines+markers",
            line=dict(color=COLOR["amber"], width=3),
            hovertemplate="%{x}<br>Late delivery: %{y:.1%}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=monthly["order_month"],
            y=monthly["low_review_rate"],
            name="Low Review Rate",
            mode="lines+markers",
            line=dict(color=COLOR["red"], width=3),
            hovertemplate="%{x}<br>Low review: %{y:.1%}<extra></extra>",
        )
    )
    fig.update_layout(title="Risk Trend")
    fig.update_yaxes(tickformat=".0%")
    return fig_html(fig)


def category_pareto_chart(categories: pd.DataFrame) -> str:
    top = categories.head(18).copy()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=top["category_name"],
            y=top["revenue"],
            name="Revenue",
            marker_color=COLOR["green"],
            hovertemplate="%{x}<br>Revenue: $%{y:,.0f}<extra></extra>",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=top["category_name"],
            y=top["cumulative_share"],
            name="Cumulative Share",
            mode="lines+markers",
            line=dict(color=COLOR["violet"], width=3),
            hovertemplate="%{x}<br>Cumulative: %{y:.1%}<extra></extra>",
        ),
        secondary_y=True,
    )
    fig.add_hline(y=0.8, line_dash="dot", line_color=COLOR["red"], secondary_y=True)
    fig.update_layout(title="Category Pareto: Revenue Concentration")
    fig.update_xaxes(tickangle=-35)
    fig.update_yaxes(title_text="Revenue", tickprefix="$", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative Share", tickformat=".0%", secondary_y=True, range=[0, 1])
    return fig_html(fig)


def rfm_chart(rfm_summary: pd.DataFrame) -> str:
    data = rfm_summary.sort_values("revenue", ascending=True)
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=data["segment"],
            x=data["revenue"],
            orientation="h",
            name="Revenue",
            marker_color=COLOR["blue"],
            text=data["customers"].map(lambda x: f"{int(x):,} customers"),
            textposition="auto",
            hovertemplate="%{y}<br>Revenue: $%{x:,.0f}<br>%{text}<extra></extra>",
        )
    )
    fig.update_layout(title="RFM Segments by Revenue")
    fig.update_xaxes(tickprefix="$")
    return fig_html(fig)


def seller_scatter(sellers: pd.DataFrame) -> str:
    data = sellers.copy()
    data = data[data["orders"] >= 10].head(500)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["revenue"],
            y=data["seller_reliability_score"],
            mode="markers",
            marker=dict(
                size=(data["orders"].clip(10, 600) ** 0.5) * 1.4,
                color=data["late_delivery_rate"],
                colorscale=[[0, "#2e9d58"], [0.5, "#d99028"], [1, "#cf4d45"]],
                showscale=True,
                colorbar=dict(title="Late"),
                line=dict(width=0.5, color="#ffffff"),
            ),
            text=data["seller_id"],
            customdata=data[["orders", "late_delivery_rate", "low_review_rate"]],
            hovertemplate=(
                "Seller: %{text}<br>Revenue: $%{x:,.0f}<br>Reliability: %{y:.1f}"
                "<br>Orders: %{customdata[0]:,.0f}<br>Late: %{customdata[1]:.1%}"
                "<br>Low review: %{customdata[2]:.1%}<extra></extra>"
            ),
        )
    )
    fig.update_layout(title="Seller Reliability vs Revenue")
    fig.update_xaxes(title="Revenue", tickprefix="$")
    fig.update_yaxes(title="Reliability Score", range=[0, 105])
    return fig_html(fig)


def delivery_state_chart(delivery: pd.DataFrame) -> str:
    data = delivery.sort_values(["late_delivery_rate", "orders"], ascending=[False, False]).head(15)
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=data["customer_state"],
            y=data["late_delivery_rate"],
            marker_color=COLOR["amber"],
            customdata=data[["orders", "avg_delay_days", "revenue"]],
            hovertemplate=(
                "%{x}<br>Late delivery: %{y:.1%}<br>Orders: %{customdata[0]:,.0f}"
                "<br>Avg delay days: %{customdata[1]:.2f}<br>Revenue: $%{customdata[2]:,.0f}<extra></extra>"
            ),
        )
    )
    fig.update_layout(title="Delivery Risk by Customer State")
    fig.update_yaxes(tickformat=".0%")
    return fig_html(fig)


def review_risk_chart(review: pd.DataFrame) -> str:
    data = review[(review["orders"] >= 100)].sort_values("review_risk_score", ascending=False).head(25)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["revenue"],
            y=data["low_review_rate"],
            mode="markers+text",
            text=data["category_name"],
            textposition="top center",
            marker=dict(
                size=(data["orders"] ** 0.5) * 1.2,
                color=data["review_risk_score"],
                colorscale=[[0, "#2e9d58"], [0.45, "#d99028"], [1, "#cf4d45"]],
                showscale=True,
                colorbar=dict(title="Risk"),
                line=dict(width=0.5, color="#ffffff"),
            ),
            customdata=data[["orders", "avg_review_score", "review_risk_score"]],
            hovertemplate=(
                "%{text}<br>Revenue: $%{x:,.0f}<br>Low review: %{y:.1%}"
                "<br>Orders: %{customdata[0]:,.0f}<br>Avg score: %{customdata[1]:.2f}"
                "<br>Risk score: %{customdata[2]:.1f}<extra></extra>"
            ),
        )
    )
    fig.update_layout(title="Review Risk: Revenue vs Dissatisfaction")
    fig.update_xaxes(title="Revenue", tickprefix="$")
    fig.update_yaxes(title="Low Review Rate", tickformat=".0%")
    return fig_html(fig)


def recommendations_table(recs: pd.DataFrame) -> str:
    rows = []
    for _, row in recs.head(10).iterrows():
        rows.append(
            f"""
            <tr>
              <td><span class="priority priority-{str(row['priority']).lower()}">{row['priority']}</span></td>
              <td>{row['action_type']}</td>
              <td>{row['target_type']}</td>
              <td class="mono">{row['target_id']}</td>
              <td>{row['reason']}<br><span class="evidence">{row['evidence_metric']}</span></td>
            </tr>
            """
        )
    return "\n".join(rows)


def build_dashboard() -> None:
    executive = read_sheet("Executive Summary")
    monthly = read_sheet("Monthly Trends")
    rfm_summary = read_sheet("RFM Segment Summary")
    categories = read_sheet("Pareto Categories")
    sellers = read_sheet("Seller Performance")
    delivery = read_sheet("Delivery By State")
    review = read_sheet("Review Risk")
    recs = read_sheet("Recommendations")

    metrics = dict(zip(executive["metric"], executive["value"]))
    monthly_core = monthly[monthly["orders"] >= 500].copy()
    top_month = monthly_core.sort_values("revenue", ascending=False).iloc[0]
    latest_month = monthly.sort_values("order_month").iloc[-1]
    top_category = categories.iloc[0]
    dormant = int(metrics["Dormant high-value customers"])
    recommendations = int(metrics["Generated recommendations"])

    charts = {
        "revenue_orders": revenue_orders_chart(monthly_core),
        "risk_trend": risk_trend_chart(monthly_core),
        "category_pareto": category_pareto_chart(categories),
        "rfm": rfm_chart(rfm_summary),
        "seller_scatter": seller_scatter(sellers),
        "delivery_state": delivery_state_chart(delivery),
        "review_risk": review_risk_chart(review),
    }

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Olist E-commerce Ops Dashboard</title>
  <style>
    :root {{
      --ink: {COLOR["ink"]};
      --muted: {COLOR["muted"]};
      --line: {COLOR["line"]};
      --page: {COLOR["page"]};
      --panel: {COLOR["panel"]};
      --blue: {COLOR["blue"]};
      --teal: {COLOR["teal"]};
      --green: {COLOR["green"]};
      --amber: {COLOR["amber"]};
      --red: {COLOR["red"]};
      --violet: {COLOR["violet"]};
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--page);
      color: var(--ink);
      font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
    }}
    .shell {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 28px;
    }}
    header {{
      display: grid;
      grid-template-columns: minmax(0, 1.7fr) minmax(280px, 0.8fr);
      gap: 24px;
      align-items: end;
      margin-bottom: 22px;
    }}
    h1 {{
      font-size: clamp(28px, 4vw, 48px);
      line-height: 1.04;
      margin: 0 0 10px;
      font-weight: 760;
    }}
    .subtitle {{
      margin: 0;
      color: var(--muted);
      max-width: 860px;
      font-size: 16px;
      line-height: 1.55;
    }}
    .summary-note {{
      border-left: 4px solid var(--blue);
      padding: 12px 0 12px 16px;
      color: var(--muted);
      line-height: 1.45;
      background: rgba(255,255,255,.55);
    }}
    .kpis {{
      display: grid;
      grid-template-columns: repeat(5, minmax(150px, 1fr));
      gap: 12px;
      margin-bottom: 18px;
    }}
    .kpi, .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 1px 2px rgba(23,32,42,.04);
    }}
    .kpi {{
      padding: 16px;
      min-height: 112px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .label {{
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .08em;
      font-weight: 700;
    }}
    .value {{
      font-size: 28px;
      line-height: 1;
      font-weight: 760;
      margin-top: 12px;
    }}
    .hint {{
      color: var(--muted);
      font-size: 13px;
      line-height: 1.35;
      margin-top: 8px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 16px;
    }}
    .panel {{
      min-width: 0;
      padding: 10px 12px 4px;
    }}
    .span-4 {{ grid-column: span 4; }}
    .span-5 {{ grid-column: span 5; }}
    .span-6 {{ grid-column: span 6; }}
    .span-7 {{ grid-column: span 7; }}
    .span-8 {{ grid-column: span 8; }}
    .span-12 {{ grid-column: span 12; }}
    .section-title {{
      font-size: 18px;
      font-weight: 730;
      margin: 10px 4px 12px;
    }}
    .insights {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin: 16px 0;
    }}
    .insight {{
      border-top: 3px solid var(--teal);
      background: #fff;
      border-radius: 8px;
      border-left: 1px solid var(--line);
      border-right: 1px solid var(--line);
      border-bottom: 1px solid var(--line);
      padding: 14px;
      line-height: 1.45;
      color: var(--muted);
    }}
    .insight strong {{
      display: block;
      color: var(--ink);
      margin-bottom: 6px;
      font-size: 15px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    th, td {{
      text-align: left;
      padding: 11px 10px;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
    }}
    th {{
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .06em;
      background: #fbfcfd;
    }}
    .mono {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      max-width: 260px;
      overflow-wrap: anywhere;
      color: #2d3748;
    }}
    .priority {{
      display: inline-flex;
      align-items: center;
      min-width: 58px;
      justify-content: center;
      border-radius: 999px;
      padding: 4px 8px;
      font-weight: 700;
      font-size: 12px;
    }}
    .priority-high {{ background: #ffe4df; color: #9c2921; }}
    .priority-medium {{ background: #fff0d8; color: #87520c; }}
    .evidence {{
      color: var(--muted);
      font-size: 12px;
    }}
    footer {{
      color: var(--muted);
      margin: 24px 2px 0;
      font-size: 13px;
    }}
    @media (max-width: 1100px) {{
      header, .insights {{ grid-template-columns: 1fr; }}
      .kpis {{ grid-template-columns: repeat(2, 1fr); }}
      .span-4, .span-5, .span-6, .span-7, .span-8 {{ grid-column: span 12; }}
    }}
    @media (max-width: 640px) {{
      .shell {{ padding: 18px; }}
      .kpis {{ grid-template-columns: 1fr; }}
      .panel {{ padding: 8px 6px 2px; }}
      th:nth-child(4), td:nth-child(4) {{ display: none; }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <header>
      <div>
        <h1>Olist E-commerce Ops Dashboard</h1>
        <p class="subtitle">A first-pass executive view over the marketplace ontology: revenue, orders, RFM customer segments, Pareto concentration, seller reliability, delivery risk, review dissatisfaction, and recommended actions.</p>
      </div>
      <div class="summary-note">
        Peak operating month was <strong>{top_month["order_month"]}</strong> at <strong>{money(top_month["revenue"])}</strong>. Monthly charts exclude thin edge months with fewer than 500 orders; latest raw month is <strong>{latest_month["order_month"]}</strong>.
      </div>
    </header>

    <section class="kpis" aria-label="Executive KPIs">
      <div class="kpi"><div class="label">Total Revenue</div><div class="value">{money(metrics["Total revenue"])}</div><div class="hint">Across {int(metrics["Total orders"]):,} orders</div></div>
      <div class="kpi"><div class="label">Unique Customers</div><div class="value">{int(metrics["Unique customers"]):,}</div><div class="hint">Using customer_unique_id</div></div>
      <div class="kpi"><div class="label">Average Order Value</div><div class="value">{money(metrics["Average order value"])}</div><div class="hint">Payment value based</div></div>
      <div class="kpi"><div class="label">Late Delivery Rate</div><div class="value">{pct(metrics["Late delivery rate"])}</div><div class="hint">Delivered after estimate</div></div>
      <div class="kpi"><div class="label">Low Review Rate</div><div class="value">{pct(metrics["Low review rate"])}</div><div class="hint">Review score <= 2</div></div>
    </section>

    <section class="insights">
      <div class="insight"><strong>Revenue is category-concentrated.</strong>{int(metrics["Categories to reach 80% revenue"])} categories generate roughly 80% of item revenue; the leading category is {top_category["category_name"]}.</div>
      <div class="insight"><strong>Seller base is broader.</strong>{int(metrics["Sellers to reach 80% revenue"])} sellers are needed to reach 80% revenue, so seller operations should be monitored as a portfolio.</div>
      <div class="insight"><strong>Winback pool is large.</strong>{dormant:,} dormant high-value customers are eligible for reactivation style actions.</div>
      <div class="insight"><strong>Action layer is live.</strong>{recommendations} first-pass recommendations were generated from RFM, seller, delivery, category, and review rules.</div>
    </section>

    <section class="grid">
      <div class="panel span-8">{charts["revenue_orders"]}</div>
      <div class="panel span-4">{charts["risk_trend"]}</div>
      <div class="panel span-7">{charts["category_pareto"]}</div>
      <div class="panel span-5">{charts["rfm"]}</div>
      <div class="panel span-6">{charts["seller_scatter"]}</div>
      <div class="panel span-6">{charts["review_risk"]}</div>
      <div class="panel span-5">{charts["delivery_state"]}</div>
      <div class="panel span-7">
        <div class="section-title">Recommended Actions</div>
        <table>
          <thead>
            <tr><th>Priority</th><th>Action</th><th>Target</th><th>ID</th><th>Reason</th></tr>
          </thead>
          <tbody>
            {recommendations_table(recs)}
          </tbody>
        </table>
      </div>
    </section>

    <footer>
      Generated from <code>outputs/olist_ecommerce_ops_analysis.xlsx</code>. This dashboard is a visualization layer over the current ontology functions, not a replacement for the underlying analysis tables.
    </footer>
  </main>
</body>
</html>
"""
    DASHBOARD.write_text(html, encoding="utf-8")
    print(DASHBOARD)


if __name__ == "__main__":
    build_dashboard()
