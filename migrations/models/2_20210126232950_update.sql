-- upgrade --
COMMENT ON COLUMN "admin"."role" IS 'odinary: ordinary
improved: improved
supreme: supreme';
-- downgrade --
COMMENT ON COLUMN "admin"."role" IS 'odinary: odinary
improved: improved
supreme: supreme';
