-- upgrade --
ALTER TABLE "event" ADD "event_over" DATE;
-- downgrade --
ALTER TABLE "event" DROP COLUMN "event_over";
