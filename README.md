# format-skill

**让 AI 按格式规范生成设计文件 —— 点名什么格式，就原生生成什么格式的成品源文件。**
**An agent skill that makes AI generate design files natively in the requested format — spec-compliant, editable source files, not flattened images with renamed extensions.**

---

## 这是什么 / What is this

`format-skill` 是一个给 AI 助手（agent）用的技能包，解决一个很具体的问题：

> 当用户说「给我一个 PSD」「我要 AI 格式」「做成 PPT」时，AI 往往只是生成一张图片，再改个后缀名。本技能要求 AI **按目标格式的行业规范原生生成文件**：PSD 就真分层、AI 就真矢量路径、印刷 PDF 就真 CMYK＋出血、PPTX 文字就真可编辑。交出去的文件同时就是源文件，下次改稿直接打开它改（换图层、改文字、改路径），不推倒重做。

`format-skill` is a skill package for AI agents that fixes a specific failure mode: when a user asks for "a PSD", "an AI file", or "a PPTX", models tend to generate a flat image and rename the extension. This skill makes the agent **generate the file natively, to the format's professional spec** — real layers for PSD, real vector paths for AI, real CMYK + bleed for print PDF, real editable text for PPTX. The deliverable *is* the source file, so revisions edit it in place instead of regenerating from scratch.

技能由三部分组成 / The package has three parts:

- **规格库（`references/specs.md`）** — 海报、横幅、展板、名片、画册、小红书/公众号/视频封面、PPT、VI 等品类的尺寸、出血、分辨率、色彩模式、图层规范。
  *Spec library* — sizes, bleed, resolution, color mode and layer conventions for posters, banners, business cards, brochures, social covers, decks, brand assets, and more.
- **生成脚本（`scripts/`）** — PSD / AI / 印刷 PDF / PPTX / 描摹矢量五条真出文件路线，全部实测通过。
  *Generation scripts* — five verified pipelines that produce real files, listed below.
- **交付规范（`SKILL.md`）** — 生成前套规格、交付前逐项核验（可重开、尺寸、色彩模式、体积上限、源件成对）的流程与铁律。
  *Delivery rules* — apply the spec before generating; verify before delivering (re-openable, exact size, correct color mode, size limits, source + export paired).

## 能干什么 / What it can do

| 格式 Format | 生成方式 How it's generated | 改稿方式 How revisions work |
|---|---|---|
| PSD 分层 / Layered PSD | psd-tools 写像素图层，RGB/CMYK、DPI 资源、中文图层名（luni）、真实 composite 预览 | 按图层名换图 / 改名 / 隐藏 — replace, rename, hide layers by name |
| .ai（矢量）/ .ai (vector) | SVG 源 → 转 PDF 载荷写为 .ai（现代 .ai 格式，Illustrator 原生打开、路径可编辑） | 改 SVG 源重导出，或直接改 .ai 内容流 — edit the SVG master, or patch the .ai content stream |
| .ai（图片）/ .ai (from raster) | vtracer 把位图描摹为轮廓 SVG → 转 .ai | 同上 / same as above |
| 印刷 PDF / Print PDF | CMYK 图（含出血画布＋裁切标记），页框 = 成品＋2×出血 | 改 job 参数重出 — adjust the job spec and re-export |
| PPTX | python-pptx 建 deck，文字全是真文本框 | 换词 / 按页编辑 — replace text, edit per slide |
| SVG | 直接生成 SVG 文本，即源文件本身 | 直接改 — edit the text file |

每条路线都经过冒烟测试：真出文件 → 重新打开 → 核验图层数、页框尺寸（精确到 0.1mm）、像素值。
Every pipeline is smoke-tested end to end: generate a real file, re-open it, and verify layer counts, page-box dimensions (to 0.1 mm), and pixel values.

## 有什么用 / Why it matters

- **交付能直接进生产流程** — PSD 能进 Photoshop 继续加工、能发印刷厂；.ai 能在 Illustrator 里点选每条路径改；PPTX 里的字客户自己就能改。不再是「看着像、没法用」的假文件。
  *Deliverables that enter real production workflows* — the PSD opens in Photoshop and can go to the print shop; the .ai exposes every path in Illustrator; deck text is editable by the client. No more "looks right, can't be used" fakes.
- **改稿成本低** — 改一个图层、一句文案、一个颜色，只动源文件对应部分，不用整张重做、不担心「AI 重新生成一张不一样的」。
  *Cheap revisions* — change one layer, one line, one color in the source file; no full regeneration, no "the AI redrew it differently" risk.
- **规格不再靠记性** — 出血、分辨率、图层命名、文件体积上限都沉淀在规格库里，AI 每次自动套用并核验，少翻车。
  *Specs stop depending on memory* — bleed, resolution, layer naming, and file-size caps live in the spec library; the agent applies and verifies them every time.
- **给 agent 工作流定标准** — 任何装上这个技能的 AI 助手，都按同一套格式规范干活，产出可预期、可交接。
  *A shared standard for agent workflows* — any assistant with this skill produces files to the same spec: predictable and hand-off ready.

典型场景 / Typical scenarios: 比赛与征稿海报的 PSD＋JPG 双格式交付、印刷横幅与展板、品牌标志的矢量源文件、课程作业与商业汇报 PPT、社媒封面的成套尺寸。
Competition posters delivered as PSD + JPG pairs, print banners and display boards, logo source files, coursework and business decks, social-cover size sets.

## 安装 / Installation

```bash
git clone https://github.com/zyking14/format-skill.git && cd format-skill
bash setup.sh   # 建 .venv、装依赖、按平台下载 vtracer / creates .venv, installs deps, downloads vtracer
```

依赖 / Requires: Python 3.11+（psd-tools、python-pptx、cairosvg、pypdf、Pillow，由 setup.sh 自动安装 / installed by setup.sh）。

作为技能使用：把整个目录放进你的 agent 的 skills 目录（如 Muse 的 `~/workspace/custom-skills/`、Claude Code 的 `.claude/skills/`），入口是 `SKILL.md`。
To use as a skill: drop the folder into your agent's skills directory (e.g. `~/workspace/custom-skills/` for Muse, `.claude/skills/` for Claude Code). The entry point is `SKILL.md`.

## 用法示例 / Usage

生成分层 PSD（job JSON 驱动）/ Layered PSD from a job spec:

```bash
.venv/bin/python scripts/psd_write.py job.json
# job.json: {"width":2480,"height":3508,"mode":"CMYK","dpi":300,
#            "layers":[{"name":"背景","image":"bg.png"},
#                      {"name":"主标题","image":"title.png","left":100,"top":200}],
#            "out":"poster.psd"}
.venv/bin/python scripts/psd_write.py --edit poster.psd --replace "主视觉=new.png" --out poster_v2.psd
```

位图转 .ai / Raster image to .ai:

```bash
.venv/bin/python scripts/trace.py photo.png traced.svg poster
.venv/bin/python scripts/ai_export.py traced.svg traced.ai
```

`examples/` 里有一张矢量海报的 SVG 源与 .ai 成品对照。/ `examples/` contains a vector poster as an SVG master with its exported .ai counterpart.

## 能力边界 / Limitations

- 本路线**不需要** Photoshop / Illustrator 本体；但也因此：PSD 里的文字是像素层（图层名标注原文，进 PS 照名重排即为真文字层）；.ai 是标准 PDF 载荷，不含 Illustrator 专有元数据（画板命名、专色面板等）。
  *No Photoshop / Illustrator required — with honest trade-offs:* PSD text layers are rasterized (layer names carry the original text, so re-typing them in Photoshop restores live text); the .ai is a standard PDF payload without Illustrator-proprietary metadata (artboard names, spot-color panels, etc.).
- 照片类图片描摹成矢量会产生大量碎路径，这是描摹的固有特性，适合 logo、图标、扁平插画。
  *Tracing photos produces many fragmented paths — an inherent property of tracing; best for logos, icons, and flat illustration.*

## 格式要点 / Hard-won format notes

- PSD 必须写**真实 composite 预览层**，空白 composite 会让部分 Photoshop 版本打不开文件。/ A PSD must carry a *real* merged composite — a blank one makes some Photoshop versions refuse the file.
- PSD 图层中文名必须走 Unicode 名（luni 块），老式 Pascal 字段装不下中文。/ Non-ASCII layer names must go through the Unicode (luni) block; the legacy Pascal field can't hold them.
- PSD 换图层像素按 channel id 对位（alpha 的 id = −1 排在首位），不要按下标猜。/ When replacing layer pixels, align by channel id (alpha is −1 and comes first) — never guess by index.

## License

MIT
