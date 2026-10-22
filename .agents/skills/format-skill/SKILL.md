---
name: format-skill
description: Create layered pixel PSD, editable-text PPTX, SVG and print PDF files, or export SVG as PDF-compatible AI. Use for explicit design-source format requests. Does not recover original layers or editable PSD text from flattened images.
---

# 按指定格式交付设计文件

先读取 references/specs.md，按用户指定参数准备素材和 job JSON。明确缺失的事实，不编造产品参数。
以本目录为技能根目录；运行 bash setup.sh 创建 .venv，使用 .venv/bin/python 调用 scripts。
安装阶段需要访问 PyPI；SVG 转换还需要系统提供 Cairo。安装不下载或执行 vtracer。

## 格式与入口

- PSD：scripts/psd_write.py job.json。像素图层可分别替换，文字为像素层，不是可编辑文字。
- PSD 编辑：scripts/psd_write.py --edit input.psd --replace "图层名=new.png" --out output_v2.psd。
- PPTX：scripts/pptx_build.py job.json，文本框文字可编辑。
- PPTX 编辑：scripts/pptx_build.py --edit input.pptx --replace-text "旧词=新词" --out output_v2.pptx。
- 印刷 PDF：scripts/print_pdf.py job.json，输出栅格 CMYK PDF；不承诺 PDF/X 合规或印厂色彩匹配，需按印厂要求另行检查。
- AI：scripts/ai_export.py input.svg output.ai；仅允许无外部引用的本地 SVG，输出 PDF 兼容内容，不含 Illustrator 专有数据。
- SVG：直接编辑源文件。导出器为安全起见拒绝 style、script、foreignObject、CSS url() 和外部 href。
- 位图描摹：暂时禁用 scripts/trace.py，不自动获取二进制。

脚本头部给出 job JSON 字段示例。保留 job JSON 与素材以便后续改稿。

## 文件与安全

只处理用户指定输入，使用独立工作目录。禁止读取凭据或无关文件。
所有输出必须是不存在的新路径；PSD/PPTX 编辑必须明确指定 --out，避免覆盖原文件。
这不是操作系统沙箱；输入输出路径仍由调用者指定。不要运行陌生 job JSON。
不要绕过 SVG 资源限制或自动启用描摹。

交付前重新打开文件，核验尺寸、图层或页数、色彩模式和体积，再查看渲染效果。
不能将扁平图片恢复为原始设计图层；不能承诺 PSD 实时文字或完整 Illustrator 兼容性。
核验发现异常时修复或如实说明，不以修改扩展名代替格式转换。

上游来源：jesohh/format-skill，提交 fe64b22c4b2844d7901ccbe76b88195e0efa8ad2，保留 MIT LICENSE。
