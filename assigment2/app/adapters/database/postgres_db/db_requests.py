class SqlStatement:
    UPDATE_POST = """UPDATE posts
                SET
                uniqueId = %s,
                postUrl = %s,
                postKarma = %s,
                commentKarma = %s,
                postDate = %s,
                numberOfComments = %s,
                numberOfVotes = %s,
                postCategory = %s,
                postAddedDate = %s
                WHERE uniqueId = %s ;"""
    UPDATE_USER = """UPDATE users
                     SET username= %s ,userKarma= %s, userCakeDay= %s
                     WHERE userId = %s"""
    GET_DATA = 'SELECT * FROM posts LEFT JOIN users ON posts.userId=users.userId ;'
    GET_POST = 'SELECT * FROM posts LEFT JOIN users ON posts.userId=users.userId WHERE uniqueId= %s ;'
    DELETE_POST = 'DELETE FROM posts WHERE uniqueId= %s ;'
    DELETE_USER = 'DELETE FROM users WHERE userId= %s ;'
    INSERT_POST = """INSERT INTO posts (
                    uniqueId,
                    postUrl,
                    postKarma,
                    commentKarma,
                    postDate,
                    numberOfComments,
                    numberOfvotes,
                    postCategory,
                    userId,
                    postAddedDate
                )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ;"""
    INSERT_USER = """INSERT INTO users (username,userKarma,userCakeDay)
                     VALUES (%s,%s,%s) ;"""
    GET_USER_ID = 'SELECT userId FROM users WHERE username= %s;'
