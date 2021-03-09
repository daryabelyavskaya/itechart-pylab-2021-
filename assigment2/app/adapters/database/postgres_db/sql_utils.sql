CREATE DATABASE posts;
CREATE TABLE posts
(
    uniqueId         VARCHAR PRIMARY KEY,
    postUrl          VARCHAR,
    userId           SMALLINT,
    postKarma        INTEGER,
    commentKarma     INTEGER,
    postDate         DATE,
    numberOfComments INTEGER,
    numberOfvotes    INTEGER,
    postCategory     VARCHAR,
    postAddedDate    DATE
);

CREATE TABLE users
(
    userId      SERIAL PRIMARY KEY,
    username    VARCHAR,
    userKarma   INTEGER,
    userCakeDay DATE
);

CREATE OR REPLACE FUNCTION check_number_of_row() RETURNS TRIGGER AS
$body$
BEGIN
    IF (SELECT count(*) FROM posts) > 1000 THEN
        RAISE EXCEPTION 'INSERT statement exceeding maximum number of rows for this table';
    END IF;
END;
$body$
    LANGUAGE plpgsql;
CREATE TRIGGER tr_check_number_of_row
    BEFORE INSERT
    ON posts
    FOR EACH ROW
EXECUTE PROCEDURE check_number_of_row();
