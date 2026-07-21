import chardet
from pathlib import Path
# import shutil
import mysql.connector

# import csv
# from pathlib import Path

# p = Path(r"C:\Users\TEJU\Downloads\amazon_sales_dataset_CLEANED.utf8.csv")
# with p.open(newline='', encoding='utf-8') as f:
#     reader = csv.reader(f)
#     rows = sum(1 for _ in reader)
# print("CSV logical rows (including header):", rows)

# === CONFIG ===
CSV_PATH = Path(r"C:/Users/TEJU/Downloads/amazon_sales_dataset_CLEANED.csv")
TABLE_NAME = "amazon_sales"   # change to your actual table name
TEMP_UTF8 = CSV_PATH.with_name(CSV_PATH.stem + ".utf8.csv")

# === 1) sanity checks ===
if not CSV_PATH.exists():
    raise SystemExit(f"CSV not found: {CSV_PATH}")

# === 2) detect encoding from a sample ===
with CSV_PATH.open("rb") as f:
    sample = f.read(200000)
det = chardet.detect(sample)
print("chardet.detect:", det)
src_enc = det.get("encoding") or "utf-8"
print("Detected encoding:", src_enc)

# === 3) convert to UTF-8 if not already UTF-8 ===
if src_enc.lower() not in ("utf-8", "utf_8"):
    print(f"Converting {CSV_PATH} from {src_enc} to UTF-8 -> {TEMP_UTF8}")
    # streaming conversion to avoid memory spikes
    with CSV_PATH.open("rb") as fr, TEMP_UTF8.open("wb") as fw:
        # decode with replace to avoid crashes; you can change errors='strict' if you want to fail on bad bytes
        data = fr.read().decode(src_enc, errors="replace").encode("utf-8")
        fw.write(data)
    csv_to_use = TEMP_UTF8
else:
    print("File already UTF-8; using original file.")
    csv_to_use = CSV_PATH

# === 4) LOAD DATA using mysql-connector-python ===
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sa123456",
    database="test",
    allow_local_infile=True,
    charset="utf8mb4",
    use_unicode=True
)
cur = conn.cursor()

# Use forward slashes in path or escape backslashes. Use absolute path.
csv_abs = str(csv_to_use.resolve()).replace("\\", "/")
print("Using CSV file:", csv_abs)

load_sql = f"""
LOAD DATA LOCAL INFILE '{csv_abs}'
INTO TABLE {TABLE_NAME}
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\\n'
IGNORE 1 LINES;
"""

try:
    cur.execute("TRUNCATE TABLE amazon_sales")
    conn.commit()
    cur.execute(load_sql)

    # Immediately check how many rows the LOAD DATA affected
    cur.execute("SELECT ROW_COUNT()")
    rows_loaded = cur.fetchone()[0]
    print("Rows reported by ROW_COUNT():", rows_loaded)

    conn.commit()

    # Confirm by counting rows in the table
    cur.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    rows_in_db = cur.fetchone()[0]
    print("Total rows in table now:", rows_in_db)

    # Show warnings if any
    cur.execute("SHOW WARNINGS")
    warnings = cur.fetchall()
    if warnings:
        print("SHOW WARNINGS returned", len(warnings), "rows. Example:")
        print(warnings[:5])
    else:
        print("No warnings from MySQL.")
except mysql.connector.Error as err:
    conn.rollback()
    print("MySQL error:", err)
finally:
    cur.close()
    conn.close()

# Optional: remove temporary converted file if you created one
if csv_to_use == TEMP_UTF8:
    print("Converted file saved at:", TEMP_UTF8)
    # Uncomment to delete the temp file automatically:
    # TEMP_UTF8.unlink()

