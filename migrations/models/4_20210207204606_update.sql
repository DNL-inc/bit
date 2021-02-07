-- upgrade --
ALTER TABLE "faculty" ADD CONSTRAINT "uid_faculty_title_8991f5" UNIQUE ("title");
-- downgrade --
ALTER TABLE "faculty" DROP CONSTRAINT "uid_faculty_title_8991f5";
