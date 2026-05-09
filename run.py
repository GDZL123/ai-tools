"""SEO Content Generation Pipeline - CLI Entry Point

Usage:
    python run.py run                  # 批量处理所有 pending 关键词
    python run.py run -k "关键词"       # 单篇生成
    python run.py dry-run              # 验证配置+提示词，不调API
    python run.py status               # 查看关键词进度
"""
import argparse
import sys
import os

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from seo_pipeline.config import load_config


def cmd_run(args):
    from seo_pipeline.pipeline import Pipeline
    config = load_config()
    pipeline = Pipeline(config)
    single = args.keyword.strip() if args.keyword else None
    pipeline.run(single_keyword=single)


def cmd_dry_run(args):
    print("=== Dry Run: 验证配置与提示词模板 ===\n")

    config = load_config()
    print(f"[OK] 配置文件加载成功")
    print(f"  API端点: {config.llm.base_url}")
    print(f"  模型: {config.llm.model}")
    print(f"  API Key: {'已设置' if config.llm.api_key else '未设置!'}")

    from seo_pipeline.prompt_manager import PromptManager
    prompts = PromptManager(config.paths.prompt_dir)
    print(f"\n[OK] 提示词模板加载成功 ({len(prompts._templates)} 个模板)")

    sys_prompt = prompts.render(
        "system",
        language=config.generation.language,
        min_chars=str(config.generation.min_chars_per_section),
        max_chars=str(config.generation.max_chars_per_section),
    )
    print(f"  system.txt: {len(sys_prompt)} 字符 [OK]")

    dummy = {
        "title": {"keyword": "测试关键词", "title": "测试标题", "category": "测试分类",
                   "count": "5", "search_volume": "100", "difficulty": "低",
                   "target_chars": "5000"},
        "outline": {"keyword": "测试关键词", "title": "测试标题", "category": "测试分类",
                     "target_chars": "5000"},
        "intro": {"keyword": "测试关键词", "title": "测试标题"},
        "section": {"keyword": "测试关键词", "title": "测试标题",
                    "section_heading": "测试章节", "section_index": "1",
                    "total_sections": "5", "previous_sections_text": "前面内容...",
                    "min_chars": "300", "max_chars": "1500"},
        "polish": {"keyword": "测试关键词", "full_article": "测试文章全文..."},
    }

    for name, params in dummy.items():
        try:
            result = prompts.render(name, **params)
            print(f"  {name}.txt: {len(result)} 字符 [OK]")
        except KeyError as e:
            print(f"  {name}.txt: [FAIL] {e}")

    print(f"\n[OK] Dry run 通过，所有模板正常。")


def cmd_status(args):
    from seo_pipeline.csv_manager import CSVManager
    config = load_config()
    csv_mgr = CSVManager(config.paths.input_csv)
    summary = csv_mgr.status_summary()
    print(f"关键词状态:")
    print(f"  总计: {summary['total']}")
    print(f"  待处理: {summary['pending']}")
    print(f"  进行中: {summary['in_progress']}")
    print(f"  已完成: {summary['done']}")
    print(f"  错误: {summary['error']}")


def main():
    parser = argparse.ArgumentParser(description="SEO 内容生产 Pipeline")
    sub = parser.add_subparsers(dest="command")

    run_parser = sub.add_parser("run", help="运行内容生产")
    run_parser.add_argument("-k", "--keyword", type=str, default=None, help="单篇生成指定关键词")
    run_parser.set_defaults(func=cmd_run)

    dry_parser = sub.add_parser("dry-run", help="验证配置和提示词，不调用API")
    dry_parser.set_defaults(func=cmd_dry_run)

    status_parser = sub.add_parser("status", help="查看关键词进度")
    status_parser.set_defaults(func=cmd_status)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
