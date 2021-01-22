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
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "tele_id" INT NOT NULL UNIQUE,
    "username" VARCHAR(255)  UNIQUE,
    "firstname" VARCHAR(255),
    "lastname" VARCHAR(255),
    "lang" VARCHAR(255),
    "group_id" INT REFERENCES "groups" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "admin" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "role" VARCHAR(8),
    "faculty_id" INT REFERENCES "faculty" ("id") ON DELETE SET NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "group_id" INT REFERENCES "groups" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "admin"."role" IS 'odinary: odinary\nimproved: improved\nsupreme: supreme';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "users_subgroup" (
    "users_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "subgroup_id" INT NOT NULL REFERENCES "subgroup" ("id") ON DELETE CASCADE
);
