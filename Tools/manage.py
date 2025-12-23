#!/usr/bin/env python3
import sys
import os
import subprocess
import argparse

def run_script(script_path, args):
    """Run a python script with the given arguments."""
    cmd = [sys.executable, script_path] + args
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Error executing {os.path.basename(script_path)}: {e}")
        sys.exit(e.returncode)

def main():
    parser = argparse.ArgumentParser(
        description="Pablo Cirre - Universal Management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage.py deploy --dry-run
  python manage.py seo --url https://pablocirre.es
  python manage.py index --sitemap https://pablocirre.es/sitemap.xml
  python manage.py performance --url https://pablocirre.es
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Operational capability")
    
    # Deploy
    deploy_parser = subparsers.add_parser("deploy", help="FTP Deployment (Sync local to remote)")
    deploy_parser.add_argument("remaining", nargs=argparse.REMAINDER, help="Arguments for deploy.py")
    
    # SEO
    seo_parser = subparsers.add_parser("seo", help="SEO Quality Audit (Crawler)")
    seo_parser.add_argument("remaining", nargs=argparse.REMAINDER, help="Arguments for audit.py")
    
    # Indexing
    index_parser = subparsers.add_parser("index", help="IndexNow Submission (Bing)")
    index_parser.add_argument("remaining", nargs=argparse.REMAINDER, help="Arguments for bing_indexer.py")
    
    # Performance
    perf_parser = subparsers.add_parser("performance", help="PageSpeed Insights Audit")
    perf_parser.add_argument("remaining", nargs=argparse.REMAINDER, help="Arguments for PageSpeed.py")

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Define script paths
    tools_root = os.path.dirname(os.path.abspath(__file__))
    scripts = {
        "deploy": os.path.join(tools_root, "deployment", "deploy.py"),
        "seo": os.path.join(tools_root, "seo", "audit.py"),
        "index": os.path.join(tools_root, "indexing", "bing_indexer.py"),
        "performance": os.path.join(tools_root, "PageSpeed", "PageSpeed.py")
    }
    
    script_path = scripts.get(args.command)
    if script_path and os.path.exists(script_path):
        # Pass remaining arguments to the sub-script
        run_script(script_path, args.remaining)
    else:
        print(f"❌ Capability '{args.command}' not found or script missing at {script_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()
