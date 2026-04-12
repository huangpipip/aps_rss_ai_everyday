# APS RSS Smoke Example

这组文件来自一次成功的 APS RSS 端到端测试运行，用于后续对比新旧实现的输出。

## 生成条件

- 数据源：APS RSS
- 运行入口：`run.sh`
- 环境文件：`test.env`
- 日期基准：UTC `2026-04-12`
- RSS 配置：`prl=https://feeds.aps.org/rss/recent/prl.xml,prx=https://feeds.aps.org/rss/recent/prx.xml`
- 抓取限制：`PAPER_LIMIT=5`
- 输出语言：`Chinese`

## 文件说明

- `raw.jsonl`：原始 APS RSS 元数据，共 5 条
- `ai_enhanced_Chinese.jsonl`：AI 增强结果，共 5 条
- `output.md`：Markdown 导出结果

## 校验信息

- `raw.jsonl`
  - SHA-256: `8de39ff7d79a653d00fb5f1982b6b182d980eddf7c251e5cc9cfb1f4145b1ec3`
- `ai_enhanced_Chinese.jsonl`
  - SHA-256: `e2077736544c87617888325b164017709ce710ddb6bfa7db1503b235f0a8331e`
- `output.md`
  - SHA-256: `ec27fa8090821582d42a60a5124075bb099d7940a2303afc7153cfcd96959027`
