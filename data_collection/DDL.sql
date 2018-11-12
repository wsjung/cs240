.mode columns
.headers on
.nullvalue NULL
PRAGMA foreign_keys = ON;

-- drop these tables from schema if they already exist
DROP TABLE if exists Symbol;
DROP TABLE if exists BTC;

CREATE TABLE Symbol (
	symbol TEXT NOT NULL PRIMARY KEY CHECK(len(symbol) <= 5),
	name TEXT NOT NULL
);

CREATE TABLE BTC (
	date TEXT PRIMARY KEY,
	open REAL NOT NULL,
	high REAL NOT NULL,
	low REAL NOT NULL,
	close REAL NOT NULL,
	adjClose REAL NOT NULL,
	volume INTEGER CHECK (volume >= 0)
);