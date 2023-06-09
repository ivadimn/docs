CREATE TABLE "org" (
    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    "code" TEXT NOT NULL,
    "name"  TEXT NOT NULL,
    "code_word" TEXT,
    "parent_id" INT,
    "created_at" TEXT NOT NULL,
    "closed_at" TEXT
);
CREATE UNIQUE INDEX "org_code_IDX" ON "org" ("code" );
CREATE UNIQUE INDEX "org_name_IDX" ON "org" ("name" );

CREATE TABLE "org_tree" (
    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    "org_id" INT NOT NULL,
    "parent_id"  INT,
    CONSTRAINT org_tree_org_id_FK FOREIGN KEY (org_id) REFERENCES org(id)
    CONSTRAINT org_tree_parent_id_FK FOREIGN KEY (parent_id) REFERENCES org(id)
);



CREATE TABLE "face" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"snils"	TEXT NOT NULL,
	"inn"	TEXT NOT NULL,
	"birthday" TEXT NOT NULL
);
CREATE UNIQUE INDEX "face_snils_IDX" ON "face" ("snils" );
CREATE UNIQUE INDEX "face_inn_IDX" ON "face" ("inn" );

CREATE TABLE "pd" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT NOT NULL,
	"comment"	TEXT
);

CREATE UNIQUE INDEX "pd_name_IDX" ON "pd" (
	"name"
);

CREATE TABLE "category" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"code"	TEXT NOT NULL,
	"name"	TEXT NOT NULL
);

CREATE UNIQUE INDEX "category_code_IDX" ON "category" (
	"code"
);
CREATE UNIQUE INDEX "category_name_IDX" ON "category" (
	"name"
);

CREATE TABLE "goal" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"code"	TEXT NOT NULL,
	"name"	TEXT NOT NULL
);

CREATE UNIQUE INDEX "goal_code_IDX" ON "goal" (
	"code"
);
CREATE UNIQUE INDEX "goal_name_IDX" ON "goal" (
	"name"
);