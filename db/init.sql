CREATE DATABASE sciq;
use sciq;

CREATE TABLE User (
  username VARCHAR(16),
  password VARCHAR(50)
);

INSERT INTO User
  (username, password)
VALUES
  ('hamza', '5f4dcc3b5aa765d61d8327deb882cf99');
