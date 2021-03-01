-- upgrade --
ALTER TABLE "users" ADD "notification" BOOL NOT NULL  DEFAULT False;
-- downgrade --
ALTER TABLE "users" DROP COLUMN "notification";
