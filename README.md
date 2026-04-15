# APS RSS AI Backend

这个仓库改造了https://github.com/dw-dengwei/daily-arXiv-ai-enhanced中的后端部分
实现对APS(美国物理学会)期刊的RSS抓取和AI总结
处理后的数据以和原始repo同样的格式存在/data中

访问https://arxiv.cquctcmp.com/ 并切换到APS数据源即可以查看每日RSS

这个仓库当前以 APS RSS feed 为数据源，抓取论文元数据并复用现有 AI 增强与 Markdown 导出流程。

当前迁入的模块：

- `daily_arxiv/`：APS RSS 抓取与去重逻辑
- `ai/`：LLM 增强处理
- `to_md/`：结果转 Markdown
- `run.sh`：本地串行执行入口

## 快速开始

1. 安装依赖

```bash
uv python install 3.12
uv sync
```

2. 配置环境变量

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"
export LANGUAGE="Chinese"
export APS_FEEDS="prl=https://feeds.aps.org/rss/recent/prl.xml,prx=https://feeds.aps.org/rss/recent/prx.xml"
export MODEL_NAME="gpt-4o-mini"
export PAPER_LIMIT="5"
export TOKEN_GITHUB=""
```

3. 运行本地流程

```bash
bash run.sh
```

如只想做小规模测试，可以设置 `PAPER_LIMIT`，例如只抓取 5 篇文章。

`APS_FEEDS` 的格式为逗号分隔的 `自定义分类=RSS链接` 映射。每条文章最终会继承它所属 RSS 配置的分类名。

## 目录说明

- `data/`：抓取结果与 AI 增强结果输出目录
- `examples/`：固定示例输出，用于后续重构后的结果对比
- `.github/workflows/run.yml`：后端版 GitHub Actions 工作流
