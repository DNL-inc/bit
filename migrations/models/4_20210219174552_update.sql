-- upgrade --
ALTER TABLE "event" ADD "time" TIMESTAMPTZ;
-- downgrade --
ALTER TABLE "event" DROP COLUMN "time";
