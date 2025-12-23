# Pablo Cirre - Python Utility Belt 🐍

This directory contains the operational tools for the project. Use the unified management script `manage.py` as your primary entry point.

## 🚀 Quick Start

Run any capability directly from the root of the `Tools/` directory:

```bash
python manage.py [command] [args]
```

## 📂 Capability Index

| Command | Subdirectory | Function | Config File |
| --- | --- | --- | --- |
| `deploy` | `deployment/` | **FTP Deployment**. Syncs local state to remote. | `config.json` |
| `seo` | `seo/` | **SEO Crawler**. Audits Titles, Metas, Links. | (CLI Args) |
| `index` | `indexing/` | **IndexNow Submission**. Pings Bing with URLs. | `bing_config.json` |
| `performance` | `PageSpeed/` | **Performance Audit**. PageSpeed Insights API. | `PageSpeedInsightAP1.txt` |

## 🛠️ Usage Examples

- **Deployment**: `python manage.py deploy --dry-run`
- **SEO Audit**: `python manage.py seo --url https://pablocirre.es`
- **Bing Indexing**: `python manage.py index --sitemap https://pablocirre.es/sitemap.xml`
- **Page Performance**: `python manage.py performance --url https://pablocirre.es`

## 📦 Dependencies

All tools require Python 3. Install required packages:

```bash
pip install -r requirements.txt
```

---
*Note: Legacy and discovery scripts have been moved to the `discovery/` folder.*
