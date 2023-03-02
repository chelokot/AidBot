# AidBot

A chatbot for finding volunteer help using semantic text search

## General TODO
- [x] 1. Create simple bot
- [ ] 2. Fill database from parsed volunteer site (see [Sources section](#sources) for more details)
- [ ] 3. Create Database - Postgres and connect it to Python bot
 
- [ ] 4. Process database with OpenAI 
- [ ] 5. Store embeddings in the database (see [Database section](#database) for more details)
 
 ### Bot functionality:
- [ ] 6. Adding propositions to database
- [ ] 7. Search: by given text - send it to OpenAI api to get embedding and find best proposition using OpenAI embeddings from database
- [ ] 8. Remove/edit propositions
- [ ] 9. Getting geolocation from user and connecting it to proposition in database/to user
- [ ] 10. Use this geolocation while searching

 #### Notifications
- [ ] 11. Get notification from bot if some new proposition is useful for your previous search
- [ ] 12. (Maybe) send notification to proposition author when some new aid search is related to it

 #### Possible improvements
 - [ ] 13. We can use more metadata given by website for better search (like categories) or maybe even using [ChatGPT(gpt-3.5-turbo) API](https://openai.com/blog/introducing-chatgpt-and-whisper-apis) for some decision making
 - [ ] 14. ChatGPT API can also be used to reply in more natural way or provide some advices for user request
 
 ## Sources 
 We should focus on creating some simplest working project first, and improving quality later if needed. Therefore, we start with parsing just one website and we can extend our sources later.
 - [ ] https://uahelpers.com/
 
 ## Database
Finding similar vectors directly by calculating cosine similarity to each element in database is pretty heavy. Moreover, getting the whole column with each query is not gonna be very efficient. For doing such "find similar" searches the *vector databases* are used usually, they provide some smart alghorithms of indexing for fast searching. 

Postgres can actually work as vector database using [this project](https://github.com/pgvector/pgvector). It allows storing vector embeddings in table and using cosine similarity in queries with some fast indexing.
 
