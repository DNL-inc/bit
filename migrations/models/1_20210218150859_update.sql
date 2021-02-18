-- upgrade --
ALTER TABLE "event" RENAME COLUMN "datetime_end" TO "event_over";
-- downgrade --
ALTER TABLE "event" RENAME COLUMN "event_over" TO "datetime_end";
