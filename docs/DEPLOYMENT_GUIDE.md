# Deployment Guide

This guide explains how to deploy the Strategickhaos empire deliverables created in this repository.

## 1. Public Profile README (Me10101-01 GitHub Profile)

**Source:** `docs/PROFILE_README.md`

**Deployment Steps:**
1. Create a new repository at `https://github.com/Me10101-01/Me10101-01`
2. Copy the contents of `docs/PROFILE_README.md` to `README.md` in that repository
3. Commit and push

**Result:** This README will appear on your GitHub profile at `https://github.com/Me10101-01`

---

## 2. Me10101-01.github.io Website

**Source:** `docs/index.html`

**Deployment Steps:**
1. Create or navigate to `https://github.com/Me10101-01/Me10101-01.github.io`
2. Copy `docs/index.html` to the root as `index.html`
3. Commit and push
4. Enable GitHub Pages in repository settings (if not already enabled)

**Result:** Your personal site will be live at `https://me10101-01.github.io`

---

## 3. Visible Repos Table

**Source:** `docs/VISIBLE_REPOS.md`

**Usage Options:**
- Add to your Obsidian vault for reference
- Create a pinned GitHub gist
- Include in project documentation
- Keep private for internal reference only

---

## 4. Private Taxonomy

**Source:** `docs/PRIVATE_TAXONOMY.md`

**⚠️ IMPORTANT: Keep this private!**

**Recommended Usage:**
- Copy to your Obsidian vault as an MOC (Map of Content)
- Use as a private reference for organizing new repositories
- Apply the naming convention (01-, 02-, etc.) to new repos

**Do NOT:**
- Publish to public repositories
- Include in public gists
- Share outside trusted circles

---

## 5. SQLite Table Dumper

**Location:** `scripts/dump_sqlite_table.py`

**Usage:**
```bash
# Basic usage
python3 scripts/dump_sqlite_table.py path/to/database.db output.csv table_name

# Example: Export URLs table
python3 scripts/dump_sqlite_table.py db.sqlite urls.csv urls
```

**Features:**
- Automatic column name detection
- UTF-8 encoding support
- Error handling and reporting
- CSV format output

**Common Use Cases:**
- Export browser history or bookmarks from SQLite databases
- Extract data from VS Code extension databases
- Convert any SQLite table to spreadsheet format
- Create backups of database tables

---

## Quick Reference

| Deliverable | Source File | Destination | Public/Private |
|------------|-------------|-------------|----------------|
| Profile README | docs/PROFILE_README.md | Me10101-01/README.md | Public |
| Website | docs/index.html | Me10101-01.github.io/index.html | Public |
| Visible Repos | docs/VISIBLE_REPOS.md | Reference/Gist | Either |
| Private Taxonomy | docs/PRIVATE_TAXONOMY.md | Obsidian Vault | Private |
| SQLite Dumper | scripts/dump_sqlite_table.py | Use in place | Public |

---

## Notes

- All public templates use the "sovereign operator" theme as specified
- HTML includes rotating animation (13s cycle)
- SQLite dumper has been tested and verified functional
- .gitignore excludes generated CSV files from version control
