# Lark CLI + Palantir FDE 影片筆記

影片：https://www.youtube.com/watch?v=q4I2exv6l8U&t=324s

建立日期：2026-05-16

## 一句話結論

這支影片的核心不是「Lark CLI 很紅」，而是：Lark CLI 讓 AI Agent 有能力讀取企業資料、建立業務本體、推送建議、甚至執行動作，因此可以做出一個輕量版的 Palantir Forward Deployed Engineer 工作流。

## 影片想講什麼

影片一開始提到飛書 / Lark CLI 很快衝到 GitHub 萬星。作者的解讀是：這不是單純一個開源 CLI 專案受歡迎，而是開發者正在搶一個新的入口。

這個入口是：

> 幫企業把散落在表格、文件、流程、訊息裡的資料，轉成 AI 能理解、能操作的數位孿生 / ontology。

他的核心論點：

- 企業 AI 落地的瓶頸，不只是模型夠不夠強。
- 更大的瓶頸是 AI 是否理解企業的真實業務世界。
- Palantir 把這個業務語義層稱為 Ontology。
- Lark CLI 則讓 AI Agent 可以碰到企業的資料、文件、協作和流程。
- 所以 Lark CLI 可能成為中小企業版 Palantir / FDE 工作流的入口。

## 他在影片裡做了什麼

### 1. 先用 AI + Lark CLI 分析 Lark CLI 自己

他讓 Claude Code 直接調用飛書 CLI，把 GitHub issue 和 PR 抓到本地或多維表格裡做分析。

分析結果包括：

- 595 個 PR
- 83 位貢獻者
- 很多貢獻來自外部社群
- 約 50 天發了 30 多個版本
- 100 多個功能
- PR 合併常常是小時級
- 合併時間中位數約 6.5 小時

這段不是最終產品 demo，而是在證明：AI Agent 可以透過 CLI 快速抓資料、建模、分析，並產出可讀的結論。

### 2. 解釋 Palantir 的 FDE / Ontology 思路

作者把 Palantir 的價值解釋成：不只是有 AI，而是能幫企業建立一張「業務世界地圖」。

他把 ontology 簡化成三個部分：

- Object 對象：客戶、訂單、商品、SKU、賣家、投放、庫存。
- Relationship 關係：誰買了什麼、哪個 SKU 屬於哪個投放、哪個客戶有哪些訂單。
- Action 動作：退款、調撥庫存、調整預算、發券、攔截訂單、觸發預警。

影片裡最重要的一句心智模型是：

> 先讓 AI 看懂你的世界，再讓它動手改你的世界。

傳統 FDE 的工作很重：

- 到客戶現場。
- 跟客戶開會。
- 理解業務流程。
- 一個個定義 object。
- 一條條梳理 relationship。
- 一個個配置 action。

影片的主張是：現在 AI Agent 加上 Lark CLI，有機會自動化掉一大部分 FDE 的前期建模與落地工作。

### 3. 用電商資料做了一個模擬營運 ontology

他用了約 15,000 筆電商交易資料，覆蓋 6 個平台。

AI Agent 透過 Lark CLI 連上 Lark Base，建立了：

- 6 張平台原始表
- 1 張全平台匯總表
- RFM 客戶分層
- 帕雷托分析
- 月度趨勢
- 2 個看板
- 投放記錄表
- SKU 與 ROI 的關聯

但作者特別說：這時候還不是 ontology，只是 data warehouse。

原因是：如果問「客戶 U9912 最近狀況怎麼樣」，客戶這個對象仍然散落在多張表裡。AI 可以查資料，但還沒有真正把這個人理解成一個有狀態、有關係、有可執行動作的業務 object。

### 4. 補上最重要的 action layer

接著他讓 Agent 去學習 Palantir 的方法論，並在 Lark 上建立一套 ontology wiki。

這個 wiki 的作用不是單純存文件，而是教 Agent：

- 什麼是業務對象。
- 對象之間有什麼關係。
- 哪些指標代表狀態。
- 哪些狀態應該觸發動作。
- 動作需要什麼證據。
- 什麼可以自動執行，什麼需要人工確認。

影片裡展示了三類動作：

- 自動預警
- What-if 模擬
- 一鍵執行

範例流程：

1. 某平台 ROI 跌破 2。
2. Lark 卡片自動推送。
3. 卡片建議降低預算 30%。
4. 使用者確認。
5. 預算被調整。
6. 使用者再問：如果把省下來的預算投到另一個平台會怎樣？
7. Agent 跑資料，回覆預估 ROI 會提升。

其他範例：

- 高價值客戶 158 天沒回購，AI 建議發定向券。
- 同款商品在不同平台價差 20%，AI 建議測試提價。
- 投放可以做成定時任務，完成監控、分析、推送、執行。

## Data warehouse 和 ontology 的差別

| 層級 | 意思 | 例子 |
|---|---|---|
| Raw data | 只有原始表，業務意義分散 | orders.csv、customers.csv、products.csv |
| Data warehouse | 表被清理、join、匯總、做成報表 | RFM 表、月度趨勢、帕雷托分析 |
| Ontology | 業務對象、關係、狀態、動作都被明確建模 | Customer 有訂單、分層、流失風險、可觸發 SendCoupon |
| Operational system | AI 可以監控、建議、請求確認、執行 | ROI 預警卡片、確認調預算、寫回投放表 |

影片真正想說的是：開發者的機會在於幫企業從前兩層走到後兩層。

## Lark CLI 的角色

影片裡 Lark CLI 不是單純開發者工具，而是 AI Agent 的「手」。

它可以讓 Agent：

- 讀寫 Lark Base。
- 建立或更新 wiki / docs。
- 推送訊息或卡片。
- 串起資料、文件、流程和人。
- 從「只回答文字」變成「能操作企業系統」。

所以作者才說 Lark CLI 是 AI 和企業資料之間的最後一公里。

## Ontology wiki 的角色

Ontology wiki 是方法論層，不只是資料庫。

它要回答：

- 有哪些 object？
- 有哪些 relationship？
- 每個 object 有哪些重要 properties？
- 哪些 metrics 代表狀態？
- 哪些 action 被允許？
- 什麼 trigger 會產生 recommendation？
- 執行前需要哪些 evidence？

重點不是 wiki 放在哪裡，而是 Agent 有沒有真的用它來建表、建關係、產生建議和執行動作。

## 影片最後的結論

作者認為 AI 時代的開發者應該準備成為 FDE 型角色。

FDE 型價值不是只會寫 SQL 或 dashboard，而是：

- 理解一個業務領域。
- 把混亂資料映射成業務 objects。
- 建立 relationships 和 metrics。
- 設計 action types。
- 讓 AI workflow 能推薦，甚至能執行。

簡化成公式：

```text
AI + 企業資料 + Ontology + CLI 執行能力 = 輕量版 Forward Deployed Engineer
```

## 對目前本機專案的啟發

這支影片和目前的電商營運分析專案非常相關，因為兩者都在處理同一件事：

> 把電商資料變成 object、relationship、metric、risk、recommendation、action。

真正的問題不是「有沒有 dashboard」，而是：

> AI Agent 能不能理解這些業務對象，並安全地對它們採取行動？

所以後續方向不是單純加更多圖表，而是讓 ontology 變得可執行：

- object definition 明確化。
- relationship 可查詢。
- action trigger 可測試。
- recommendation 結構化。
- 加入 approval / execution surface。
- 加入 eval / guardrail，避免 Agent 亂建議或亂執行。

