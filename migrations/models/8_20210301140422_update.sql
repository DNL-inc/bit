-- upgrade --
DROP TABLE IF EXISTS "notification_users";
DROP TABLE IF EXISTS "notification_event";
ALTER TABLE "notification" ADD "event_id" INT NOT NULL;
ALTER TABLE "notification" ADD "user_id" INT NOT NULL;
ALTER TABLE "notification" ADD CONSTRAINT "fk_notifica_event_c9f85dcc" FOREIGN KEY ("event_id") REFERENCES "event" ("id") ON DELETE CASCADE;
ALTER TABLE "notification" ADD CONSTRAINT "fk_notifica_users_c30cb5cd" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "notification" DROP CONSTRAINT "fk_notifica_users_c30cb5cd";
ALTER TABLE "notification" DROP CONSTRAINT "fk_notifica_event_c9f85dcc";
ALTER TABLE "notification" DROP COLUMN "event_id";
ALTER TABLE "notification" DROP COLUMN "user_id";
CREATE TABLE "notification_users" ("user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,"notification_id" INT NOT NULL REFERENCES "notification" ("id") ON DELETE CASCADE);
CREATE TABLE "notification_event" ("event_id" INT NOT NULL REFERENCES "event" ("id") ON DELETE CASCADE,"notification_id" INT NOT NULL REFERENCES "notification" ("id") ON DELETE CASCADE);
