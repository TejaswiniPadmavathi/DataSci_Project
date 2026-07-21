# detect encoding with chardet
import chardet
raw = open('input.csv','rb').read(200000)
print(chardet.detect(raw))
# If detected as cp1252 or latin1, convert:
# Use iconv on Linux/macOS: iconv -f WINDOWS-1252 -t UTF-8 input.csv -o input.utf8.csv

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='sa123456',
    database='test',
    allow_local_infile=True,
    charset='utf8mb4',
    use_unicode=True
)
cur = conn.cursor()

sql = r"""
LOAD DATA LOCAL INFILE 'C:\Users\TEJU\Downloads\amazon_sales_dataset_CLEANED.csv'
INTO TABLE your_table
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
"""
cur.execute(sql)
conn.commit()
cur.close()
conn.close()

cur.execute("SELECT COUNT(*) FROM amazon_sale")
rows_in_db = cur.fetchone()[0]
print("Rows in DB:", rows_in_db)
