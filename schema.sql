--
-- File generated with SQLiteStudio v3.3.3 on Tue Jun 13 16:32:54 2023
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Logins
CREATE TABLE Logins(
    ID_Login INTEGER PRIMARY KEY,
    plattform TEXT,
    password TEXT,
    User_ID INTEGER,
    FOREIGN KEY (User_ID) REFERENCES Users (ID_User) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Table: Users
CREATE TABLE Users(
    ID_User INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
