-- upgrade --
ALTER TABLE "users" ADD "notification_time" INT NOT NULL  DEFAULT 0;
-- downgrade --
ALTER TABLE "users" DROP COLUMN "notification_time";
