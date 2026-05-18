import { mkdir, writeFile, rm } from "node:fs/promises";
import path from "node:path";

const DOCS_ROOT = "https://www.palantir.com/docs";
const START_URL = `${DOCS_ROOT}/foundry/aip`;
const OUT_DIR = path.resolve("wiki/palantir-aip");
const PAGES_DIR = path.join(OUT_DIR, "pages");

const scrapedAt = new Date().toISOString();

function docsUrlFor(target) {
  if (target.startsWith("http://") || target.startsWith("https://")) return target;
  if (target.startsWith("/docs/")) return new URL(target, "https://www.palantir.com").href;
  if (target.startsWith("/")) return new URL(`/docs${target}`, "https://www.palantir.com").href;
  return new URL(target, `${DOCS_ROOT}/`).href;
}

function extractNextData(html, url) {
  const match = html.match(/<script id="__NEXT_DATA__"[^>]*>([\s\S]*?)<\/script>/);
  if (!match) {
    throw new Error(`Unable to find __NEXT_DATA__ in ${url}`);
  }
  return JSON.parse(match[1]);
}

function normalizeDocsPath(url) {
  const parsed = new URL(url, DOCS_ROOT);
  let pathname = parsed.pathname;
  if (pathname.startsWith("/docs/")) pathname = pathname.slice("/docs".length);
  if (!pathname.endsWith("/")) pathname += "/";
  return pathname;
}

function filenameForUrl(url) {
  const parsed = new URL(url, DOCS_ROOT);
  let key = parsed.pathname.replace(/^\/docs\//, "").replace(/^\/+|\/+$/g, "");
  if (!key) key = "index";
  if (parsed.search) {
    key += `-${parsed.searchParams.toString().replace(/[^a-zA-Z0-9]+/g, "-").replace(/-+$/g, "")}`;
  }
  return `${key.replace(/[^a-zA-Z0-9]+/g, "-").replace(/^-+|-+$/g, "").toLowerCase()}.md`;
}

function collectPages(items, trail = [], out = []) {
  for (const item of items || []) {
    if (item.type === "header") {
      out.push({ type: "header", title: item.text, trail });
    } else if (item.type === "pageLink") {
      const link = item.link || {};
      if (link.url?.startsWith("/foundry/")) {
        out.push({
          type: "page",
          title: link.text || item.pageId,
          url: link.url,
          openInNewTab: Boolean(link.openInNewTab),
          trail,
        });
      }
    } else if (item.type === "pageGroup") {
      collectPages(item.pages, [...trail, item.title], out);
    } else if (item.type === "section") {
      collectPages(item.items, [...trail, item.title], out);
    }
  }
  return out;
}

function uniquePages(entries) {
  const seen = new Set();
  return entries.filter((entry) => {
    if (entry.type !== "page") return true;
    const key = entry.url;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function escapeYaml(value) {
  return String(value ?? "").replaceAll("\\", "\\\\").replaceAll('"', '\\"');
}

function stripTitlePrefix(title) {
  return String(title || "")
    .replace(/^Documentation\s*\|\s*/i, "")
    .replace(/^AI Platform \(AIP\)\s*>\s*/i, "");
}

function buildLocalMaps(pages) {
  const map = new Map();
  for (const page of pages.filter((entry) => entry.type === "page")) {
    const full = docsUrlFor(page.url);
    const pathname = normalizeDocsPath(full);
    const file = filenameForUrl(full);
    map.set(pathname, file);
    map.set(`/docs${pathname}`, file);
  }
  return map;
}

function rewriteMarkdownLinks(markdown, localMap) {
  return markdown.replace(/(\]\()([^)#\s]+)(#[^)]+)?(\))/g, (whole, open, rawTarget, hash = "", close) => {
    if (
      rawTarget.startsWith("http://") ||
      rawTarget.startsWith("https://") ||
      rawTarget.startsWith("mailto:") ||
      rawTarget.startsWith("#")
    ) {
      return whole;
    }

    if (rawTarget.startsWith("/docs/resources/") || rawTarget.startsWith("/docs/favicon")) {
      return `${open}${new URL(rawTarget, "https://www.palantir.com").href}${hash}${close}`;
    }

    const docsPath = rawTarget.startsWith("/docs/")
      ? normalizeDocsPath(rawTarget)
      : rawTarget.startsWith("/foundry/")
        ? normalizeDocsPath(`/docs${rawTarget}`)
        : null;

    if (docsPath) {
      const file = localMap.get(docsPath);
      if (file) return `${open}${file}${hash}${close}`;
      const absolute = rawTarget.startsWith("/docs/")
        ? new URL(rawTarget, "https://www.palantir.com").href
        : new URL(`/docs${rawTarget}`, "https://www.palantir.com").href;
      return `${open}${absolute}${hash}${close}`;
    }

    if (rawTarget.startsWith("/")) {
      return `${open}${new URL(rawTarget, "https://www.palantir.com").href}${hash}${close}`;
    }

    return whole;
  });
}

function frontMatter(page, sourceUrl, data, sectionPath) {
  const metadata = data.props.pageProps.metadata?.data || {};
  const title = stripTitlePrefix(metadata.pageTitle || page.title);
  return [
    "---",
    `title: "${escapeYaml(title)}"`,
    `source_url: "${escapeYaml(sourceUrl)}"`,
    `scraped_at: "${scrapedAt}"`,
    `section: "${escapeYaml(sectionPath || "Root")}"`,
    `canonical_slug: "${escapeYaml(metadata.slug || "")}"`,
    "---",
    "",
  ].join("\n");
}

function renderIndex(entries, pageRecords) {
  const byUrl = new Map(pageRecords.map((record) => [record.navUrl, record]));
  const lines = [
    "# Palantir AIP Wiki",
    "",
    `Source: [Palantir Foundry AIP documentation](${START_URL})`,
    `Generated: ${scrapedAt}`,
    "",
    "This wiki is generated from Palantir's public documentation pages. Use the local page links for reading, and the `source_url` front matter in each page when you need to verify against the original.",
    "",
    "## Start Here",
    "",
    "- [中文学习导读](LEARNING_GUIDE_ZH.md)",
    "- [Crawl manifest](crawl_manifest.json)",
    "",
    "## Pages",
    "",
  ];

  let currentHeader = "";
  for (const entry of entries) {
    if (entry.type === "header") {
      currentHeader = entry.title;
      if (lines.at(-1) !== "") lines.push("");
      lines.push(`### ${entry.title}`);
      lines.push("");
      continue;
    }
    if (entry.type !== "page") continue;

    const record = byUrl.get(entry.url);
    const section = entry.trail.join(" / ");
    const prefix = section
      ? `- **${section}**:`
      : currentHeader
        ? `- **${currentHeader}**:`
        : "-";
    if (!record) {
      lines.push(`${prefix} [${entry.title}](${docsUrlFor(entry.url)})`);
      continue;
    }
    lines.push(`${prefix} [${entry.title}](pages/${record.file})`);
  }

  lines.push("");
  return lines.join("\n");
}

function renderLearningGuide(pageRecords) {
  const core = pageRecords.filter((record) => record.navUrl.startsWith("/foundry/aip/"));
  const apps = pageRecords.filter((record) => !record.navUrl.startsWith("/foundry/aip/"));
  return `# Palantir AIP 中文学习导读

生成时间：${scrapedAt}

## 一句话心智模型

AIP 是把 Foundry 里的数据、Ontology、权限治理、模型连接、应用构建和运行观测接到一起的 AI 操作层。它不只是「调用 LLM」，而是让 LLM 能在受控权限、审计、评估和业务对象语义之上执行工作流、问答、分析、文档处理和应用交互。

## 推荐学习路径

1. 先读 [Overview](pages/${core.find((p) => p.navUrl === "/foundry/aip/overview/")?.file || "foundry-aip-overview.md"}) 和 [AIP features](pages/${core.find((p) => p.navUrl === "/foundry/aip/aip-features/")?.file || "foundry-aip-aip-features.md"})，建立整体框架。
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

- AIP 基础页面：${core.length} 页
- AIP 相关应用页面：${apps.length} 页
- 总计：${pageRecords.length} 页

详见 [README](README.md) 和 [crawl_manifest.json](crawl_manifest.json)。
`;
}

async function fetchPage(url) {
  const response = await fetch(url, {
    headers: {
      "user-agent": "Codex local documentation wiki builder",
      "accept": "text/html,application/xhtml+xml",
    },
  });
  if (!response.ok) throw new Error(`HTTP ${response.status} for ${url}`);
  const html = await response.text();
  return { response, html, data: extractNextData(html, url) };
}

async function main() {
  const start = await fetchPage(START_URL);
  const entries = uniquePages(collectPages(start.data.props.pageProps.sidebarNavProps.items));
  const pages = entries.filter((entry) => entry.type === "page" && !entry.openInNewTab);
  const localMap = buildLocalMaps(pages);

  await rm(OUT_DIR, { recursive: true, force: true });
  await mkdir(PAGES_DIR, { recursive: true });

  const pageRecords = [];
  for (const [index, page] of pages.entries()) {
    const sourceUrl = docsUrlFor(page.url);
    process.stdout.write(`[${index + 1}/${pages.length}] ${sourceUrl}\n`);
    const fetched = await fetchPage(sourceUrl);
    const props = fetched.data.props.pageProps;
    const metadata = props.metadata?.data || {};
    const file = filenameForUrl(sourceUrl);
    const sectionPath = page.trail.join(" / ");
    const markdown = props.markdown || "";
    const rewritten = rewriteMarkdownLinks(markdown, localMap);
    const content = `${frontMatter(page, sourceUrl, fetched.data, sectionPath)}${rewritten.trim()}\n`;
    await writeFile(path.join(PAGES_DIR, file), content, "utf8");
    pageRecords.push({
      title: stripTitlePrefix(metadata.pageTitle || page.title),
      navTitle: page.title,
      section: sectionPath,
      navUrl: page.url,
      sourceUrl,
      canonicalSlug: metadata.slug || "",
      file,
      lastModified: fetched.response.headers.get("last-modified"),
      markdownChars: markdown.length,
      headings: (props.tableOfContentsItems || []).map((toc) => toc.title),
    });
  }

  await writeFile(path.join(OUT_DIR, "README.md"), renderIndex(entries, pageRecords), "utf8");
  await writeFile(path.join(OUT_DIR, "LEARNING_GUIDE_ZH.md"), renderLearningGuide(pageRecords), "utf8");
  await writeFile(
    path.join(OUT_DIR, "crawl_manifest.json"),
    `${JSON.stringify({ startUrl: START_URL, scrapedAt, pageCount: pageRecords.length, pages: pageRecords }, null, 2)}\n`,
    "utf8",
  );

  process.stdout.write(`Done. Wrote ${pageRecords.length} pages to ${OUT_DIR}\n`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
