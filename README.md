# format-skill — 让 AI 按格式规范生成设计文件

一个给 AI 编程/设计助手用的技能（skill）：当用户点名要某种**文件格式**时，AI 不再交一张扁平图片糊弄后缀名，而是**按该格式的行业规范原生生成最终文件**——PSD 真分层、AI 真矢量路径、印刷 PDF 真 CMYK＋出血、PPTX 文字真可编辑。交付的文件同时就是源文件，后续改稿直接改源文件（换图层、改文字、改路径），不推倒重做。

An agent skill that makes AI deliver design files **natively in the requested format**: layered PSD, true-vector .ai, CMYK print PDF with bleed, editable PPTX — spec-compliant, and editable in place for revisions.

## 能力一览（均已实测）

| 格式 | 路线 | 改稿方式 |
|---|---|---|
| PSD 分层 | psd-tools 写 PixelLayer，支持 RGB/CMYK、DPI 资源、中文图层名（luni）、真实 composite 预览 | 按图层名换图 / 改名 / 隐藏 |
| .ai（矢量） | SVG 源 → cairosvg 转 PDF 载荷写为 .ai（现代 .ai 格式，Illustrator 原生打开、路径可编辑） | 改 SVG 源后重导出，或直接改 .ai 内容流 |
| .ai（图片） | vtracer 描摹位图为轮廓 SVG → 转 .ai | 同上 |
| 印刷 PDF | PIL 出 CMYK（含出血画布＋裁切标记），页框 = 成品＋2×出血 | 改 job JSON 重出 |
| PPTX | python-pptx 建 deck，文字全是真文本框 | `--replace-text` 换词或按页编辑 |
| SVG | 直接生成 SVG 文本，即源文件本身 | 直接改 |

## 安装

```bash
git clone <this-repo> && cd format-skill
bash setup.sh   # 建 .venv、装依赖、按平台下载 vtracer
```

依赖：Python 3.11+、psd-tools、python-pptx、cairosvg、pypdf、Pillow（setup.sh 自动装）。

作为技能使用时，把整个目录放进你的 agent 的 skills 目录即可（如 Muse 的 `~/workspace/custom-skills/`、Claude Code 的 `.claude/skills/`），`SKILL.md` 是入口。

## 用法示例

生成分层 PSD（job JSON 驱动）：

```bash
.venv/bin/python scripts/psd_write.py job.json
# job.json: {"width":2480,"height":3508,"mode":"CMYK","dpi":300,
#            "layers":[{"name":"背景","image":"bg.png"},
#                      {"name":"主标题","image":"title.png","left":100,"top":200}],
#            "out":"poster.psd"}
.venv/bin/python scripts/psd_write.py --edit poster.psd --replace "主视觉=new.png" --out poster_v2.psd
```

位图转 .ai：

```bash
.venv/bin/python scripts/trace.py photo.png traced.svg poster
.venv/bin/python scripts/ai_export.py traced.svg traced.ai
```

规格库（海报/横幅/名片/画册/小红书/公众号/PPT 等品类的尺寸、出血、分辨率、图层规范）在 [`references/specs.md`](references/specs.md)。`examples/` 里有一张矢量海报的 SVG 源与 .ai 成品对照。

## 能力边界（先说清）

- 本路线**不需要** Photoshop / Illustrator 本体；但也因此：PSD 里的文字是像素层（图层名标注原文，进 PS 照名重排即为真文字层）；.ai 是标准 PDF 载荷，不含 Illustrator 专有元数据（画板命名、专色面板等）。
- 照片类图片描摹成矢量会产生大量碎路径，这是描摹的固有特性，适合 logo、图标、扁平插画。

## 格式要点（实战教训，已内置进脚本）

- PSD 必须写**真实 composite 预览层**，空白 composite 会让部分 Photoshop 版本打不开文件。
- PSD 图层中文名必须走 Unicode 名（luni 块），老式 Pascal 字段装不下中文。
- PSD 换图层像素按 channel id 对位（alpha 的 id = −1 排在首位），不要按下标猜。

## License

MIT
