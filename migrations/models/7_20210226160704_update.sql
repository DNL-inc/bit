-- upgrade --
CREATE TABLE IF NOT EXISTS "notification" (
    "id" SERIAL NOT NULL PRIMARY KEY
);;
CREATE TABLE "notification_event" ("event_id" INT NOT NULL REFERENCES "event" ("id") ON DELETE CASCADE,"notification_id" INT NOT NULL REFERENCES "notification" ("id") ON DELETE CASCADE);
CREATE TABLE "notification_users" ("user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,"notification_id" INT NOT NULL REFERENCES "notification" ("id") ON DELETE CASCADE);
-- downgrade --
DROP TABLE IF EXISTS "notification_event";
DROP TABLE IF EXISTS "notification_users";
DROP TABLE IF EXISTS "notification";
