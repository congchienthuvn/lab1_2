def create_tables(conn):
    """Tạo bảng chứa dữ liệu Tiki JSON nếu chưa tồn tại"""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tiki_products (
                id SERIAL PRIMARY KEY,
                data JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
    print("Database schema initialized successfully.")