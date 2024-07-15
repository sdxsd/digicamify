DROP TABLE IF EXISTS post;

CREATE TABLE post (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT UNIQUE NOT NULL,
	posted TIMESTAMP NOT NULL,
	filename TEXT UNIQUE NOT NULL,
	deletion_pass TEXT
);
