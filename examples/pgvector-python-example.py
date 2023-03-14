import psycopg
from pgvector.psycopg import register_vector
import numpy as np

conn = psycopg.connect("dbname=DBNAME user=USER password=PASSWORD")
conn.autocommit = True
conn.execute('CREATE EXTENSION IF NOT EXISTS vector')

conn.execute('DROP TABLE IF EXISTS test_table')
conn.execute('CREATE TABLE test_table (id bigserial primary key, embedding vector(1568))')
register_vector(conn)

sql = 'INSERT INTO test_table (embedding) VALUES' + ','.join(['(%s)'] * 5)
params = [
    np.random.rand(1568).astype(np.float32) for i in range(5)
]
conn.execute(sql, params)

conn.execute('CREATE INDEX ON test_table USING ivfflat (embedding vector_cosine_ops)')

result = conn.execute(
    'SELECT id FROM test_table ORDER BY embedding <=> %s LIMIT 15', 
    (np.random.rand(1568).astype(np.float32),)
).fetchall()
print(result)