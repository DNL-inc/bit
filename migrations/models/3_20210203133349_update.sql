-- upgrade --
CREATE TABLE IF NOT EXISTS "messages" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "text" TEXT NOT NULL,
    "sending_time" TIMESTAMPTZ NOT NULL,
    "creator_id" INT NOT NULL REFERENCES "admin" ("id") ON DELETE CASCADE
);;
ALTER TABLE "users" ADD "welcome_message_id" INT NOT NULL;
-- downgrade --
ALTER TABLE "users" DROP COLUMN "welcome_message_id";
DROP TABLE IF EXISTS "messages";
