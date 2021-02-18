-- upgrade --
CREATE TABLE IF NOT EXISTS "faculty" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "groups" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "course" INT NOT NULL,
    "faculty_id" INT NOT NULL REFERENCES "faculty" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "subgroup" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "group_id" INT NOT NULL REFERENCES "groups" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "event" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "link" VARCHAR(255) NOT NULL,
    "type" VARCHAR(255) NOT NULL,
    "datetime_end" DATE,
    "day" VARCHAR(9),
    "group_id" INT NOT NULL REFERENCES "groups" ("id") ON DELETE CASCADE,
    "subgroup_id" INT REFERENCES "subgroup" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "event"."day" IS 'monday: monday\ntuesday: tuesday\nwednesday: wednesday\nthursday: thursday\nfriday: friday\nsaturday: saturday\nsunday: sunday';
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "tele_id" INT NOT NULL UNIQUE,
    "username" VARCHAR(255)  UNIQUE,
    "firstname" VARCHAR(255),
    "lastname" VARCHAR(255),
    "lang" VARCHAR(2),
    "welcome_message_id" INT NOT NULL,
    "group_id" INT REFERENCES "groups" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "admin" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "role" VARCHAR(8),
    "group_id" INT REFERENCES "groups" ("id") ON DELETE SET NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "faculty_id" INT REFERENCES "faculty" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "admin"."role" IS 'ordinary: ordinary\nimproved: improved\nsupreme: supreme';
CREATE TABLE IF NOT EXISTS "chats" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "tele_id" INT NOT NULL UNIQUE,
    "group_id" INT NOT NULL REFERENCES "groups" ("id") ON DELETE CASCADE,
    "creator_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "messages" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "text" TEXT NOT NULL,
    "sending_time" TIMESTAMPTZ NOT NULL,
    "creator_id" INT NOT NULL REFERENCES "admin" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "users_subgroup" (
    "users_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "subgroup_id" INT NOT NULL REFERENCES "subgroup" ("id") ON DELETE CASCADE
);
