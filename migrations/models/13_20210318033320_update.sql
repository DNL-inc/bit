-- upgrade --
ALTER TABLE "chats" ADD "title" VARCHAR(255) NOT NULL;
-- downgrade --
ALTER TABLE "chats" DROP COLUMN "title";
