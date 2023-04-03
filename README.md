# AidBot
![A chatbot for finding volunteer help using semantic text search](./assets/aidbot.gif)


[<img align="left" alt="Visual Studio Code" width="24px" src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/2048px-Telegram_logo.svg.png" /> @Aid_Ai_Bot](https://t.me/Aid_Ai_bot)

 ## Description

TODO: write description here

TODO: write user stories [here](./assets/UserStories.md)

 ## Sources 
 We should focus on creating some simplest working project first, and improving quality later if needed. Therefore, we start with parsing just one website and we can extend our sources later:
 - [x] https://uahelpers.com/
 
 ## Database
 ### pgvector
Finding similar vectors directly by calculating cosine similarity to each element in database is pretty heavy. Moreover, getting the whole column with each query is not gonna be very efficient. For doing such "find similar" searches the *vector databases* are used usually, they provide some smart alghorithms of indexing for fast searching. 

Postgres can actually work as vector database using [this project](https://github.com/pgvector/pgvector). It allows storing vector embeddings in table and using cosine similarity in queries with some fast indexing.

pgvector compiled for Windows is provided in pgvector directory. *vector.dll* must be putted into **./lib** folder in PostgreSQL directory, and all *.sql* files and *vector.control* file must be putted into **./share/extension** folder in PostgreSQL directory. 

Once you do it, extension can be connected to database as `CREATE EXTENSION IF NOT EXISTS vector` and then you can create column with type **vector()**, for example: `CREATE TABLE table_name (id bigserial primary key, embedding vector(1568))`. 

After table is filled with some data, you can create *index* as `CREATE INDEX ON table_name USING ivfflat (embedding vector_cosine_ops)`. Indexes are used to speed up search by a lot

Then you can search in your database simply by using ORDER BY: `SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 1;`

 ### pgvector-python
[pgvector-python](https://github.com/pgvector/pgvector-python) is used for convinient work with vectors in database using python. All you need to do to use it after it's installed is
```
from pgvector.psycopg import register_vector
register_vector(conn)
```
It will allow you to provide numpy arrays into conn.execute command, for example:
```
conn.execute(
   'INSERT INTO table_name (embedding) VALUES (%s)', 
   np.random.rand(1568).astype(np.float32)
)
```
You can see more detailed example in [an example file](./examples/pgvector-python-example.py).
