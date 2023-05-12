# AidBot - Telegram bot project for finding volunteer help using semantic search
# Copyright (C) 2023
# Anastasia Mayorova aka EternityRei  <anastasiamayorova2003@gmail.com>
#    Andrey Vlasenko aka    chelokot   <andrey.vlasenko.work@gmail.com>

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

# import psycopg
# from pgvector_lib.psycopg import register_vector
# import numpy as np
# import config
#
# conn = psycopg.connect(f"dbname={config.dbname} user={config.user} password={config.password}")
# conn.autocommit = True
# conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
#
# conn.execute('DROP TABLE IF EXISTS test_table')
# conn.execute('CREATE TABLE test_table (id bigserial primary key, embedding vector(1568))')
# register_vector(conn)
#
# sql = 'INSERT INTO test_table (embedding) VALUES' + ','.join(['(%s)'] * 5)
# params = [
#     np.random.rand(1568).astype(np.float32) for i in range(5)
# ]
# conn.execute(sql, params)
#
# conn.execute('CREATE INDEX ON test_table USING ivfflat (embedding vector_cosine_ops)')
#
# result = conn.execute(
#     'SELECT id FROM test_table ORDER BY embedding <=> %s LIMIT 15',
#     (np.random.rand(1568).astype(np.float32),)
# ).fetchall()
# print(result)
