# Palantir AIP 中文学习导读

生成时间：2026-05-16T03:02:37.251Z

## 一句话心智模型

AIP 是把 Foundry 里的数据、Ontology、权限治理、模型连接、应用构建和运行观测接到一起的 AI 操作层。它不只是「调用 LLM」，而是让 LLM 能在受控权限、审计、评估和业务对象语义之上执行工作流、问答、分析、文档处理和应用交互。

## 推荐学习路径

1. 先读 [Overview](pages/foundry-aip-overview.md) 和 [AIP features](pages/foundry-aip-aip-features.md)，建立整体框架。
2. 接着读安全、治理、可观测性、算力使用：这些决定能不能把 AI 放进真实生产流程。
3. 如果你要接自己的模型，读 Bring your own model 和 LLM-provider compatible APIs。
4. 如果你要做业务应用，优先读 AIP Logic、Chatbot Studio、AIP Analyst、AIP Assist。
5. 最后读 AIP Evals：没有评估体系，AI 工作流很难稳定上线。

## 核心模块速记

- **AIP 基础层**：模型连接、prompt 工程、安全隐私、治理、observability、compute usage。
- **AIP Logic**：把 AI 能力编排成可运行、可自动化、可监控的逻辑流程。
- **AIP Chatbot Studio**：构建带上下文、工具、引用和 API 集成的聊天机器人。
- **AIP Analyst**：面向业务分析的自然语言分析入口，适合探索数据和解释指标。
- **AIP Assist**：把内部文档、应用和建议动作接入 AI 助手。
- **AIP Evals**：为 Logic 函数、Ontology 编辑和实验建立测试与评估闭环。
- **Document Intelligence**：从文档中提取结构化信息，并可部署到 Python transforms。
- **Model Catalog / BYOM**：管理模型、模型生命周期以及自带模型接入。

## 和这个电商运营分析项目的对应关系

- **Ontology 思路**：把订单、客户、卖家、商品、评价、支付等表转成业务对象和关系，而不是只当 CSV 分析。
- **AIP Analyst**：可作为运营人员的自然语言分析层，例如「哪些卖家导致差评和延迟发货？」。
- **AIP Logic**：可把异常检测、客户分群、卖家预警、自动生成行动建议串成流程。
- **Chatbot Studio / Assist**：可做内部运营助手，回答指标定义、定位异常订单、引用分析报告。
- **Document Intelligence**：可用于处理发票、投诉附件、供应商文档等非结构化资料。
- **AIP Evals**：评估回答是否正确引用数据、是否遵守业务规则、是否给出可执行建议。

## 已抓取范围

- AIP 基础页面：15 页
- AIP 相关应用页面：56 页
- 总计：71 页

详见 [README](README.md) 和 [crawl_manifest.json](crawl_manifest.json)。
