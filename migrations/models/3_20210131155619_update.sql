-- upgrade --
ALTER TABLE "users" ADD "welcome_message_id" INT NOT NULL;
-- downgrade --
ALTER TABLE "users" DROP COLUMN "welcome_message_id";
