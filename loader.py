import json
from pathlib import Path
import psycopg
from config import load_config
from models import create_tables


def import_tiki_data(data_dir_path="data"):
    # Tải cấu hình từ database.ini
    config = load_config()
    data_dir = Path(data_dir_path)

    if not data_dir.exists():
        print(f"Error: Directory '{data_dir.absolute()}' does not exist.")
        return

    try:

        with psycopg.connect(**config) as conn:
            # Khởi tạo bảng từ file models.py
            create_tables(conn)

            total_files = 0
            total_records = 0

            with conn.cursor() as cur:
                for json_file in sorted(data_dir.glob("*.json")):
                    try:
                        with open(json_file, "r", encoding="utf-8") as f:
                            content = json.load(f)

                            if isinstance(content, list):
                                for item in content:
                                    cur.execute(
                                        "INSERT INTO tiki_products (data) VALUES (%s);",
                                        [json.dumps(item)]
                                    )
                                    total_records += 1
                            elif isinstance(content, dict):
                                cur.execute(
                                    "INSERT INTO tiki_products (data) VALUES (%s);",
                                    [json.dumps(content)]
                                )
                                total_records += 1

                        total_files += 1
                        print(f"Imported file: {json_file.name}")
                    except Exception as e:
                        print(f"Failed to read file {json_file.name}: {e}")

                conn.commit()
                print(f"\nCOMPLETED: Successfully inserted {total_records} records from {total_files} files.")

    except Exception as e:
        print(f"Database connection error: {e}")