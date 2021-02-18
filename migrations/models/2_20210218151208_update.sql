-- upgrade --
ALTER TABLE "event" DROP COLUMN "event_over";
-- downgrade --
ALTER TABLE "event" ADD "event_over" DATE;
