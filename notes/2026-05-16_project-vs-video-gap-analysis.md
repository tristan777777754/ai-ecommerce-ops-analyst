# 目前專案 vs 影片做法：差距分析

建立日期：2026-05-16

相關筆記：[Lark CLI + Palantir FDE 影片筆記](2026-05-16_lark-cli-palantir-fde-video-notes.md)

## 短答案

你現在做的東西，和影片的方向是同一個方向，但還不是完全同一件事。

你目前已經有一個很扎實的本機版 Palantir-style e-commerce operations ontology 原型：

- 本機 Palantir AIP wiki
- Olist 電商資料集
- dataset schema 和 relationship report
- object / link / action 的設計
- RFM 客戶分層
- seller risk 指標
- delivery / review risk 指標
- rule-based recommendations
- dashboard 和 Excel outputs

影片裡展示的則多了一層「營運整合」：

- Agent 讀 methodology / wiki。
- Agent 操作 Lark CLI。
- Wiki 和 Base 建在 Lark 這種協作工作區裡。
- Agent 寫入 Lark Base。
- Agent 推送 Lark 卡片。
- 使用者可以確認 action。
- 系統可以模擬或執行調整。

所以差距不是「你只是做資料庫，他做 ontology」。

更精準的說法是：

> 你目前是本機 ontology + analytics prototype。影片展示的是 agent-operated + Lark-integrated workflow prototype。

## 你現在已經有什麼

### 1. 本機 Palantir AIP 知識庫

路徑：`wiki/palantir-aip/`

你已經建立了一包本機 Palantir AIP wiki，裡面有：

- AIP overview
- AI FDE pages
- AIP Logic
- AIP Analyst
- AIP Assist
- Chatbot Studio
- AIP Evals
- governance、observability、model、document intelligence 等內容

這和影片裡「讓 Agent 學 Palantir 方法論」很接近。

差別是：

你現在的 wiki 比較像是閱讀 / 參考資料；影片裡的 wiki 更像是 Agent 工作時會主動依照的操作方法論，並且它會影響 Agent 怎麼建表、建關係、建 action。

### 2. 本機電商 ontology 設計

路徑：`PROJECT_CONTEXT.md`

這份文件已經把 ontology 的骨架定義得很清楚：

- Object types：Customer、Order、OrderItem、Product、Seller、Payment、Review、Delivery、Geography。
- Analytical object types：CustomerSegment、RetentionOpportunity、SellerRisk、DeliveryRisk、ReviewRisk、ProductOpportunity、BusinessRecommendation。
- Link types：Customer placed Order、Order contains OrderItem、OrderItem references Product、Seller fulfills OrderItem 等。
- Metrics / functions：revenue、RFM、churn risk、late delivery rate、low review rate、seller reliability。
- Action types：SendReactivationOffer、InvestigateSeller、MonitorDeliveryRisk、PromoteHighRevenueCategory 等。

這個部分和影片的核心思想其實非常接近。

### 3. 舊本機原型曾經跑出的分析 outputs

以下是舊本機 prototype 的參考產物或曾規劃產物。它們可以用來理解 metric 定義，但不應該再被當成下一步主線：

- `outputs/DATASET_SCHEMA.md`
- `outputs/OPS_ANALYSIS_REPORT.md`
- `outputs/AIP_APPLIED_ANALYSIS_BLUEPRINT.md`
- `outputs/customer_rfm.csv`
- `outputs/seller_performance.csv`
- `outputs/order_facts_sample.csv`
- `outputs/olist_ecommerce_ops_analysis.xlsx`
- `outputs/ops_dashboard.html`

這代表專案曾經有本機分析基礎，但修正後的主線應該改成 AI Agent 操作 Lark CLI / Lark Base 來重建這些多維分析能力。

這些舊產物表達的業務 signal 仍然有參考價值：

- Customer RFM segments
- Dormant high-value customers
- Seller reliability
- Late delivery risk
- Low review risk
- Category Pareto concentration
- Business recommendations

這比「一個本機資料庫」強很多。它已經是一個本機營運分析層。

## 和影片真正差在哪

| 維度 | 影片 demo | 你目前的專案 | 差距 |
|---|---|---|---|
| 工作空間 | Lark docs / wiki / Base / cards | 本機 files、CSV、Excel、HTML | 少了共享協作工作區 |
| Agent loop | Agent 主動用 CLI 建立 / 更新 Lark artifacts | Python / JS scripts 產出本機 artifacts | 少了常駐或可互動的 Agent 工作流 |
| Ontology wiki | 建在 Lark，作為方法論與操作指南 | 建在本機，主要是 Palantir docs mirror | 有參考價值，但尚未變成機器可執行規格 |
| Data layer | Lark Base tables | 本機 CSV / XLSX outputs | 本機可用，但還不是協作型資料層 |
| Action layer | 預警、what-if、一鍵執行 | 報告裡的 rule-based recommendations | 少了 approval / execution UI |
| Notification | Lark cards / messages | 靜態 dashboard / report | 少了主動推送 |
| Writeback | 模擬或寫回 budget/action changes | recommendations only | 少了真正的寫回目標 |
| Governance | Lark / Palantir-style permission 與 workflow | 本機 files；blueprint 裡有 eval 概念 | 需要 runnable evals 和 approval rules |

## 最大差異不是 wiki 放哪裡

本機 wiki 可以，Lark wiki 也可以。真正關鍵不是位置，而是：

> 這個 wiki 有沒有接進 Agent 的工作迴路？

你現在比較像：

```text
Palantir AIP docs / wiki -> 你閱讀理解 -> scripts 編碼這些想法 -> 本機 outputs
```

影片裡比較像：

```text
Palantir methodology / wiki -> Agent 讀取 -> Agent 操作 Lark CLI -> Lark Base / wiki / cards / actions 更新
```

所以你目前是「人把方法論消化後，寫成分析系統」。

影片是「Agent 直接讀方法論，然後操作企業協作系統」。

這就是最主要的差距。

## 你是不是差很多？

沒有差到從零開始。其實你已經有三個最難的部分：

- 一個像真實業務的資料集。
- 一個清楚的 ontology framing。
- 一個可以跑出 metrics、risks、recommendations 的分析層。

你缺的是 operational shell：

- 自然語言查詢介面。
- Agent / tool loop。
- Lark Base 或其他共享資料庫整合。
- 主動推送通知。
- approval buttons 或 command actions。
- what-if simulation endpoint。
- runnable evals / guardrails。

## 修正後的下一個里程碑

目前已確認：下一步應該先回到影片的主線，不是繼續本機 Python 分析。

修正後的順序是：

1. 讓 AI Agent 從 `dataset/` 讀取 Olist 原始 CSV。
2. 讓 AI Agent 使用 Lark CLI 操作 Lark Base，建立多維分析工作區。
3. 在 Lark Base 中建立 raw tables、joined views、RFM、Pareto、seller performance、category performance、delivery risk、review risk、dashboard views。
4. 明確標記這個階段仍然是 data warehouse / analysis layer，不是 ontology。
5. 讓另一個 AI Agent 讀 `wiki/palantir-aip/`，學習 Palantir / AIP 的 ontology、logic、action、eval 方法論。
6. 再把 Lark Base 分析出來的業務世界轉成 ontology objects、relationships、metrics、actions、BusinessRecommendation。

這樣專案會從：

```text
agent-operated Lark Base analysis workspace
```

升級成：

```text
Palantir-style operational ontology and action workflow
```

本機 scripts 只能作為 legacy/reference，不應該再主導下一步。

## 最終判斷

你和影片在核心概念上是對齊的：

- raw e-commerce data
- business objects
- relationships
- metrics
- risks
- recommendations
- Palantir / FDE framing

影片更強調的是 agent execution environment：

- Lark CLI
- Lark Base
- Lark wiki
- notification cards
- action execution

你目前更強的是 local analytical and ontology foundation：

- schema
- joins
- metrics
- reports
- dashboard
- AIP study wiki
- action blueprint

所以，是的，兩者還有明顯差距；但這個差距不是壞事。你已經有內容和地基，下一步是把它變成互動式、Agent 可操作、可以被批准與執行的營運系統。
