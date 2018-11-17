.mode columns
.headers on
.nullvalue NULL
PRAGMA foreign_keys = ON;

drop table if exists BTC;
drop table if exists BCH;
drop table if exists ETH;
drop table if exists EOS;
drop table if exists XRP;

create table BTC (
	date TEXT PRIMARY KEY,
	open REAL NOT NULL,
	high REAL NOT NULL,
	low REAL NOT NULL,
	close REAL NOT NULL,
	adjClose REAL NOT NULL,
	volume INTEGER
);

create table BCH (
	date TEXT PRIMARY KEY,
	open REAL NOT NULL,
	high REAL NOT NULL,
	low REAL NOT NULL,
	close REAL NOT NULL,
	adjClose REAL NOT NULL,
	volume INTEGER
);

create table ETH (
	date TEXT PRIMARY KEY,
	open REAL NOT NULL,
	high REAL NOT NULL,
	low REAL NOT NULL,
	close REAL NOT NULL,
	adjClose REAL NOT NULL,
	volume INTEGER
);

create table EOS (
	date TEXT PRIMARY KEY,
	open REAL NOT NULL,
	high REAL NOT NULL,
	low REAL NOT NULL,
	close REAL NOT NULL,
	adjClose REAL NOT NULL,
	volume INTEGER
);

create table XRP (
	date TEXT PRIMARY KEY,
	open REAL NOT NULL,
	high REAL NOT NULL,
	low REAL NOT NULL,
	close REAL NOT NULL,
	adjClose REAL NOT NULL,
	volume INTEGER
);
