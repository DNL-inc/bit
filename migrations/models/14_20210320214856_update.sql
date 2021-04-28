-- upgrade --
ALTER TABLE "chats" ADD "lang" VARCHAR(2);
-- downgrade --
ALTER TABLE "chats" DROP COLUMN "lang";
