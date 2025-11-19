#!/usr/bin/env python3
"""
SQLite Table Dumper
Exports any SQLite table to CSV format

Usage:
    python3 dump_sqlite_table.py db.sqlite urls.csv urls
    
Arguments:
    1. db_path: Path to SQLite database file
    2. out_csv: Output CSV file path
    3. table: Table name to export
"""
import sys
import sqlite3
import csv

def dump_sqlite_table(db_path, out_csv, table):
    """Dump a SQLite table to CSV file"""
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        
        # Get column names
        cols = [d[0] for d in cur.execute(f"PRAGMA table_info({table})")]
        
        # Get all rows
        rows = cur.execute(f"SELECT * FROM {table}").fetchall()
        
        # Write to CSV
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(cols)
            w.writerows(rows)
        
        con.close()
        print(f"✓ Wrote {len(rows)} rows to {out_csv}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    
    db_path, out_csv, table = sys.argv[1], sys.argv[2], sys.argv[3]
    success = dump_sqlite_table(db_path, out_csv, table)
    sys.exit(0 if success else 1)
