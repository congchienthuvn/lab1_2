def create_tables(conn):
    """Tạo bảng tiki_products với các cột riêng biệt chuẩn xác"""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tiki_products (
                id BIGINT PRIMARY KEY,
                name TEXT,
                url_key TEXT,
                price NUMERIC,
                description TEXT,
                images_url TEXT[],
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
    print("Database table schema created successfully with specific columns.")