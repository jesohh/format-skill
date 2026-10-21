#!/usr/bin/env bash
# format-skill 环境安装：建 venv、装 Python 依赖、下载 vtracer 二进制
set -e
cd "$(dirname "$0")"

python3 -m venv .venv
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet psd-tools python-pptx cairosvg pypdf numpy pillow
echo "python deps ok"

mkdir -p bin
if [ ! -x bin/vtracer ]; then
  case "$(uname -s)-$(uname -m)" in
    Linux-x86_64)  A=vtracer-x86_64-unknown-linux-musl.tar.gz ;;
    Linux-aarch64) A=vtracer-aarch64-unknown-linux-musl.tar.gz ;;
    Darwin-arm64)  A=vtracer-aarch64-apple-darwin.tar.gz ;;
    Darwin-x86_64) A=vtracer-x86_64-apple-darwin.tar.gz ;;
    *) echo "未知平台，请手动从 https://github.com/visioncortex/vtracer/releases 下载 vtracer 放到 bin/"; A="" ;;
  esac
  if [ -n "$A" ]; then
    curl -sL "https://github.com/visioncortex/vtracer/releases/download/1.0.0-alpha.4/$A" | tar --no-same-owner -xz -C bin
    chmod +x bin/vtracer
    echo "vtracer ok"
  fi
fi
echo "setup done. Try: .venv/bin/python scripts/ai_export.py examples/ordinary-poster.svg /tmp/test.ai"
