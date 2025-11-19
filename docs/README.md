# Documentation & Templates

This directory contains templates and documentation for the Strategickhaos empire public presence.

## Files

### PROFILE_README.md
Template for the Me10101-01 GitHub profile README.  
**Deployment:** Copy to a new repository at `https://github.com/Me10101-01/Me10101-01/README.md`

### index.html
Template for Me10101-01.github.io website.  
**Deployment:** Copy to `https://github.com/Me10101-01/Me10101-01.github.io/index.html`

### VISIBLE_REPOS.md
Public-facing repository table for reference or pinned gists.

### PRIVATE_TAXONOMY.md
Private product line taxonomy for Obsidian vault or internal documentation.  
**Note:** This should remain private and never be published to public repos.

## SQLite Utility

The `dump_sqlite_table.py` script (located in `/scripts/`) provides functionality to export SQLite tables to CSV format.

**Usage:**
```bash
python3 scripts/dump_sqlite_table.py db.sqlite output.csv table_name
```

**Features:**
- Extract and organize table data to CSV/JSON
- Quick SQL operations for deduplication and filtering
- Automated reporting capabilities
