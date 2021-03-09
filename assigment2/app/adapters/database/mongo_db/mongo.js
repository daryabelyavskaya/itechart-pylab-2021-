use posts
db.createCollection("posts")
db.posts.createIndex({"uniqueId": 'text'},{unique:true})