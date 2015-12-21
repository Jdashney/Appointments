DROP TABLE IF EXISTS apts;
CREATE TABLE apts (
  id INTEGER PRIMARY KEY autoincrement,
  name TEXT not null,
  aptdate TEXT not null,
  batch INTEGER
);
