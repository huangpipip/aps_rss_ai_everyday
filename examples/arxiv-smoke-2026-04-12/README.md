# arXiv Smoke Example

这组文件用于后续后端改造时做基线对比，来自一次成功的端到端测试运行。

## 生成条件

- 数据源：当前 `arxiv` 抓取流程
- 运行入口：`run.sh`
- 环境文件：`test.env`
- 日期基准：UTC `2026-04-12`
- 抓取限制：`PAPER_LIMIT=5`
- 输出语言：`Chinese`

## 文件说明

- `raw.jsonl`：原始抓取结果，共 5 条
- `ai_enhanced_Chinese.jsonl`：AI 增强结果，共 3 条
- `output.md`：Markdown 导出结果

## 校验信息

- `raw.jsonl`
  - SHA-256: `383ca55f11d394f3d7c0941290db58bdab8535cbab0078c709eefd521ea88eb3`
- `ai_enhanced_Chinese.jsonl`
  - SHA-256: `52d235722bf074c543d19af00266742f24b5b651305c6bdf02b56b99e69b806f`
- `output.md`
  - SHA-256: `7b3258a5e5dc20fdd05bd86952e731c55a1f1d2b270d90b1aede66af46769a1e`

## 对比建议

- 对比抓取阶段：检查 `raw.jsonl` 的条数、字段完整性和论文 ID
- 对比 AI 阶段：检查 `ai_enhanced_Chinese.jsonl` 的保留条数和 `AI` 字段结构
- 对比导出阶段：检查 `output.md` 的章节结构和条目顺序
