CREATE TABLE "org" (
    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    "code" TEXT NOT NULL,
    "name"  TEXT NOT NULL,
    "parent_id" INT,
    "created_at" TEXT NOT NULL,
    "closed_at" TEXT
);
CREATE UNIQUE INDEX "org_code_IDX" ON "org" ("code" );
CREATE UNIQUE INDEX "org_name_IDX" ON "org" ("name" );

CREATE TABLE tree_path (
	"parent_id" INTEGER NOT NULL,
	"child_id" INTEGER NOT NULL,
	PRIMARY KEY (parent_id, child_id),
	CONSTRAINT tree_path_parent_id_FK FOREIGN KEY (parent_id) REFERENCES org(id) ON DELETE CASCADE
	CONSTRAINT tree_path_child_id_FK FOREIGN KEY (child_id) REFERENCES org(id) ON DELETE CASCADE
);


CREATE TABLE "dep_word" (
    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    "dep_id" INTEGER NOT NULL,
    "code_word"  TEXT NULL,
    CONSTRAINT dep_word_dep_id_FK FOREIGN KEY (dep_id) REFERENCES org(id)
);

CREATE TABLE "face" (
    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    "snils" TEXT NOT NULL,
    "birthday"  TEXT NOT NULL
);
CREATE UNIQUE INDEX "face_snils_IDX" ON "face" ("snils");

CREATE TABLE "pd" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"face_id" INT NOT NULL,
	"firstname"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"fathername" TEXT,
	"created_at" TEXT NOT NULL,
	"closed_at" TEXT
);

CREATE TABLE "tmp_face" (
    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    "snils" TEXT NOT NULL,
    "birthday"  TEXT NOT NULL
);
CREATE UNIQUE INDEX "tmp_face_snils_IDX" ON "tmp_face" ("snils");
