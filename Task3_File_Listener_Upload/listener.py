import os
import time
import sqlite3
import pandas as pd
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# === Config ===
UPLOAD_DIR = "uploads"
DB_NAME = "database.db"

# === Utility ===
def clean_table_name(filename):
    """Convert filename to a valid SQLite table name"""
    name = os.path.splitext(os.path.basename(filename))[0]
    name = re.sub(r'\W+', '_', name)  # replace non-word chars
    return name.lower()

def read_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.csv':
            return pd.read_csv(file_path, encoding='latin1')
        elif ext in ['.xls', '.xlsx']:
            return pd.read_excel(file_path)
        elif ext == '.json':
            return pd.read_json(file_path)
        else:
            print(f"[!] Skipping unsupported file: {file_path}")
            return None
    except Exception as e:
        print(f"[X] Failed to read {file_path}: {e}")
        return None

# === Main DB Insert ===
def insert_file_to_db(file_path):
    df = read_file(file_path)
    if df is None:
        return

    table_name = clean_table_name(file_path)

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Build column types dynamically
        columns = df.columns
        types = df.dtypes

        sql_columns = []
        for col, dtype in zip(columns, types):
            if pd.api.types.is_integer_dtype(dtype):
                sql_type = 'INTEGER'
            elif pd.api.types.is_float_dtype(dtype):
                sql_type = 'REAL'
            else:
                sql_type = 'TEXT'
            sql_columns.append(f'"{col}" {sql_type}')

        # Create table
        create_query = f'''
            CREATE TABLE IF NOT EXISTS "{table_name}" (
                {', '.join(sql_columns)}
            );
        '''
        cursor.execute(create_query)
        conn.commit()

        # Insert data
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.close()
        print(f"[✓] Inserted {len(df)} rows into table '{table_name}'")

    except Exception as e:
        print(f"[X] Error uploading {file_path} → {e}")

# === Watchdog Handler ===
class UploadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        print(f"[📂] New file detected: {event.src_path}")
        time.sleep(1)  # wait for file copy to complete
        insert_file_to_db(event.src_path)

# === Start Listener ===
def start_listener():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    print(f"📡 Listening for new files in '{UPLOAD_DIR}'...\n")

    event_handler = UploadHandler()
    observer = Observer()
    observer.schedule(event_handler, UPLOAD_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Listener stopped.")
    observer.join()

if __name__ == "__main__":
    start_listener()
