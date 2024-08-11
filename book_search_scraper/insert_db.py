import psycopg2
import json

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname='yousuu',
    user='postgres',
    password='00000000',
    host='localhost',
    port='5432'
)

cur = conn.cursor()

# Load the NDJSON file
with open('books.ndjson', 'r', encoding='utf-8') as f:
    for line in f:
        json_data = json.loads(line)
        cur.execute("INSERT INTO tui_json (data) VALUES (%s)",
                    [json.dumps(json_data)])

# Commit and close
conn.commit()
cur.close()
conn.close()
