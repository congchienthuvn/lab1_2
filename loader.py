import json
from pathlib import Path
import psycopg
from config import load_config
from models import create_tables


def import_tiki_data(data_dir_path="data"):
    config = load_config()
    data_dir = Path(data_dir_path)

    if not data_dir.exists():
        print(f"Error: Directory '{data_dir.absolute()}' does not exist.")
        return

    try:
        with psycopg.connect(**config) as conn:
            create_tables(conn)

            total_files = 0
            total_records = 0

            for json_file in sorted(data_dir.glob("*.json")):
                # Sử dụng savepoint cho từng file để tránh lỗi lan truyền transaction
                with conn.transaction():
                    try:
                        with open(json_file, "r", encoding="utf-8") as f:
                            content = json.load(f)

                            if isinstance(content, dict):
                                items = [content]
                            elif isinstance(content, list):
                                items = content
                            else:
                                continue

                            file_records = 0
                            with conn.cursor() as cur:
                                for item in items:
                                    prod_id = item.get("id")
                                    if not prod_id:
                                        continue

                                    name = item.get("name")
                                    url_key = item.get("url_key")
                                    price = item.get("price")
                                    description = item.get("description")
                                    images_url = item.get("images_url", [])

                                    cur.execute("""
                                        INSERT INTO tiki_products (id, name, url_key, price, description, images_url)
                                        VALUES (%s, %s, %s, %s, %s, %s)
                                        ON CONFLICT (id) DO UPDATE SET
                                            name = EXCLUDED.name,
                                            url_key = EXCLUDED.url_key,
                                            price = EXCLUDED.price,
                                            description = EXCLUDED.description,
                                            images_url = EXCLUDED.images_url;
                                    """, (prod_id, name, url_key, price, description, images_url))

                                    file_records += 1

                        total_records += file_records
                        total_files += 1
                        print(f"Successfully imported file: {json_file.name} ({file_records} records)")
                    except Exception as e:
                        print(f"Failed to read/import file {json_file.name}: {e}")

            print(f"\nCOMPLETED: Successfully imported total {total_records} records from {total_files} files.")

    except Exception as e:
        print(f"Database connection error: {e}")