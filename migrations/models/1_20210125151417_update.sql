-- upgrade --
CREATE TABLE IF NOT EXISTS "chats" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "tele_id" INT NOT NULL UNIQUE,
    "group_id" INT NOT NULL REFERENCES "groups" ("id") ON DELETE CASCADE,
    "creator_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "chats";
