# Format Skill — 按格式规范生成与改稿

用户点名要某种格式（PSD / AI / 印刷 PDF / PPTX / SVG / EPS），就**按那个格式的行业规范原生生成最终文件**，不拿一张扁平图糊弄后缀名。每个交付文件都保留可编辑源，**后续改稿直接改源文件**（改图层、改文字、改路径），不推倒重做。

## 触发
- 用户说「我要 X 格式的」「给我 PSD / AI 文件」「做成 PPT」等点名格式的话。
- 用户点名品类（海报/横幅/名片/封面/PPT…）但没点名格式时：按 `references/specs.md` 规格库自动套规格＋推荐格式，用户点头或改。

## 两条总原则
1. **格式原生**：PSD 就真分层、PPTX 文字就真可编辑、AI 就真矢量路径、印刷 PDF 就真 CMYK＋出血。生成前先查规格库，生成后过核验清单。
2. **源文件即主文件**：交付物 = 源文件（+ 按需的导出/预览图）。改稿时打开源文件改对应图层/文字/路径再重存，禁止「重新生成一张新的」代替改稿，除非用户明确说重做。

## 格式路由（本机实证路线）
环境：`技能目录下 .venv/bin/python（先跑 bash setup.sh）`（psd-tools / python-pptx / cairosvg / pypdf 已装），vtracer 在 skill 自带 `bin/vtracer`（系统目录的安装会被部署冲掉，勿往 /usr/local/bin 装）。

| 格式 | 路线 | 脚本 |
|---|---|---|
| PSD 分层 | psd-tools 写 PixelLayer（RGB/CMYK 均可），文字栅格化为像素层、图层名标注原文 | `scripts/psd_write.py`（支持 --edit 按图层名换图/改名/隐藏） |
| .ai（矢量原生） | 先作 SVG 源 → cairosvg 转 PDF 载荷 → 写为 .ai（现代 .ai 即 PDF 载荷，Illustrator 原生打开、路径可编辑） | `scripts/ai_export.py` |
| .ai（图片描摹） | vtracer 把位图描成轮廓 SVG → 同上转 .ai；同时交付 SVG 源 | `scripts/trace.py` + `ai_export.py` |
| 印刷 PDF | PIL 出 CMYK 图（含出血画布＋裁切标记）→ PDF，页框 = 成品+2×出血 | `scripts/print_pdf.py` |
| PPTX | python-pptx 建 deck，文字全是真文本框；改稿 --replace-text 或按页编辑 | `scripts/pptx_build.py` |
| SVG | 直接手写/生成 SVG 文本，即源文件本身 | — |
| PNG/JPG | PIL 导出，按规格库像素尺寸；JPG 质量 ≥90（交付图），印刷 JPG 用 95 | — |

## 铁律
- **PSD 必须写真实 composite 预览层**（`psd_write.py` 已内置）。2026-10-21 消防海报实证： composite 缺失/空白的 PSD 在部分 PS 上打不开。
- **PSD 图层名走 luni 块**：中文名不能进老式 Pascal 字段，必须经 `layer.name` 赋值器写入（脚本已处理）；换图层像素按 channel id 对位（alpha 的 id=-1 排在首位），不按下标猜。
- **AI 的边界先说清再交付**：本机无 Illustrator 本体；.ai 走 SVG 源转 PDF 载荷，Illustrator 可开可编辑可另存，但不含 AI 专有元数据（画板命名、专色面板等）。合并过的整图转 .ai 只能是描摹轮廓，照片类会碎路径——这类活开工前先讲边界（与用户既定规矩一致）。
- **PSD 文字是像素层**：交付时提醒用户，图层名即原文，在 PS 里照名重排即可变真文字层；用户若明确要「可编辑文字层 PSD」，说明本机路线做不到，不要假装。
- **事实性文案一个字不编**：尺寸、时间、折扣等以用户给的为准；规格库里的通用数值只作版式参数。
- **交付前必核验**：按 `references/specs.md` 末尾的核验清单逐项过（可重开/尺寸/色彩模式/体积上限/源件成对），过了才说交付。

## 改稿流程
1. 找到源文件（PSD/PPTX/SVG/job JSON 与成品成对存放在同一目录）。
2. 用对应脚本 edit 模式或直接编辑源（SVG 改文本、PPTX 换词、PSD 换图层图）。
3. 重存/重导出成品，沿用核验清单再过一遍。
4. 新版另存带版本号，不覆盖旧版（除非用户说覆盖）。
