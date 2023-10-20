
# таблицы хранение органиизационной структуры
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


CREATE TABLE "face" (
    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    "snils" TEXT NOT NULL,
    "birthday"  TEXT NOT NULL
);
CREATE UNIQUE INDEX "face_snils_IDX" ON "face" ("snils");

CREATE TABLE "position" (
    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "number"  INT NOT NULL DEFAULT 99
);
CREATE UNIQUE INDEX "position_name_IDX" ON "position" ("name");


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
    "snils" TEXT PRIMARY KEY
    "tn"	INTEGER NOT NULL,
    "firstname"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"fathername" TEXT,
);

CREATE VIEW org_view AS
    SELECT o.id, o.name, "Chief name", o.parent_id
    FROM org o
    WHERE o.closed_at is NULL;