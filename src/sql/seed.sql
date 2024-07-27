PRAGMA foreign_keys = OFF;

DELETE FROM users;

PRAGMA foreign_keys = ON;

INSERT INTO users (username, hash)
VALUES
("test1", "test_hash")