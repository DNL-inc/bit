-- upgrade --
DROP TABLE IF EXISTS "messages";
CREATE TABLE IF NOT EXISTS "messages" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "text" TEXT NOT NULL,
    "sending_time" TIMESTAMPTZ NOT NULL,
    "creator_id" INT NOT NULL REFERENCES "admin" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "messages";
