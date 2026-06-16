#!/usr/bin/env python3
"""
Save reverse-engineered prompt results to local files.

Usage:
    save_result.py --image <path/url> --platform <name> --prompt <text> --params <json-file>
    save_result.py --search <keyword>

Output: prompts/反推结果_[YYYY-MM-DD]_[HHMMSS].md
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


DEFAULT_OUTPUT_DIR = Path.home() / "Desktop" / "图片反推"

PARAM_BLOCKS = {
    "A": "画面框架",
    "B": "人物主体",
    "C": "摄影语言",
    "D": "光影系统",
    "E": "后期质感",
    "F": "约束输出",
    "G": "输出载体",
}


def format_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_filename():
    return datetime.now().strftime("反推结果_%Y-%m-%d_%H%M%S")


def save_result(image_ref, platform, prompt_text, params, output_dir):
    """Save a reverse-engineered prompt result to a local markdown file."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{format_filename()}.txt"
    filepath = output_dir / filename

    # Build markdown content
    lines = [
        f"# 反推提示词结果\n",
        f"- **原始图片**: {image_ref}",
        f"- **分析时间**: {format_timestamp()}",
        f"- **目标平台**: {platform}\n",
    ]

    # Parameters summary (only filled ones)
    if params:
        filled = {k: v for k, v in sorted(params.items()) if v}
        if filled:
            lines.append(f"- **已标注参数**: {len(filled)} 个\n")
            lines.append(f"## 参数摘要\n")
            lines.append("| 板块 | 参数ID | 标注值 |")
            lines.append("|------|--------|--------|")
            for param_id, value in filled.items():
                block_key = param_id[0] if param_id else "?"
                block_name = PARAM_BLOCKS.get(block_key, "其他")
                lines.append(f"| {block_name} | {param_id} | {value} |")
            lines.append("")

    # Full prompt
    lines.append(f"## {platform} 提示词\n")
    lines.append(prompt_text)
    lines.append("")

    # Full parameter table (all params)
    if params:
        lines.append(f"## 完整参数详情\n")
        lines.append("| 板块 | 参数ID | 标注值 |")
        lines.append("|------|--------|--------|")
        for param_id in sorted(params.keys()):
            value = params[param_id] or "（未测）"
            block_key = param_id[0] if param_id else "?"
            block_name = PARAM_BLOCKS.get(block_key, "其他")
            lines.append(f"| {block_name} | {param_id} | {value} |")
        lines.append("")

    content = "\n".join(lines)
    filepath.write_text(content, encoding="utf-8")
    print(f"✅ 保存成功: {filepath}")
    return str(filepath)


def search_results(keyword, output_dir):
    """Search saved prompt results by keyword in filenames or content."""
    output_dir = Path(output_dir)
    if not output_dir.exists():
        print(f"📭 尚无存档目录: {output_dir}")
        return []

    results = []
    for f in sorted(output_dir.glob("反推结果_*.txt"), reverse=True):
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        if keyword.lower() in f.name.lower() or keyword.lower() in text.lower():
            # Extract first line as title hint
            first_line = text.strip().split("\n")[0] if text else f.name
            results.append((str(f), first_line, f.stat().st_mtime))

    if results:
        print(f"🔍 找到 {len(results)} 条匹配 '{keyword}':")
        for path, title, mtime in results:
            dt = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
            print(f"  [{dt}] {Path(path).name} — {title}")
    else:
        print(f"📭 未找到匹配 '{keyword}' 的结果")
    return results


def main():
    parser = argparse.ArgumentParser(description="Save or search reverse-engineered prompts")
    subparsers = parser.add_subparsers(dest="command", help="save or search")

    # Save subcommand
    save_parser = subparsers.add_parser("save", help="Save a prompt result")
    save_parser.add_argument("--image", required=True, help="Original image path or URL")
    save_parser.add_argument("--platform", required=True, help="Target platform name")
    save_parser.add_argument("--prompt", required=True, help="Generated prompt text")
    save_parser.add_argument("--params", help="Path to JSON file with parameter values")
    save_parser.add_argument("--dir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory")

    # Search subcommand
    search_parser = subparsers.add_parser("search", help="Search saved results")
    search_parser.add_argument("keyword", help="Search keyword")
    search_parser.add_argument("--dir", default=str(DEFAULT_OUTPUT_DIR), help="Search directory")

    args = parser.parse_args()

    if args.command == "save":
        params = {}
        if args.params:
            try:
                params = json.loads(Path(args.params).read_text(encoding="utf-8"))
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"⚠️ 参数文件读取失败: {e}")

        result_path = save_result(
            image_ref=args.image,
            platform=args.platform,
            prompt_text=args.prompt,
            params=params,
            output_dir=args.dir,
        )
        print(f"\n文件路径: {result_path}")

    elif args.command == "search":
        search_results(args.keyword, args.dir)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
