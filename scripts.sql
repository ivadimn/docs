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
	parent_id INTEGER NOT NULL,
	child_id INTEGER NOT NULL,
	PRIMARY KEY (parent_id, child_id),
	CONSTRAINT tree_path_parent_id_FK FOREIGN KEY (parent_id) REFERENCES org(id) ON DELETE CASCADE
	CONSTRAINT tree_path_child_id_FK FOREIGN KEY (child_id) REFERENCES org(id) ON DELETE CASCADE
);

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

CREATE TABLE "dep" (
    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    "code" TEXT NOT NULL,
    "name"  TEXT NOT NULL,
    "created_at" TEXT NOT NULL,
    "closed_at" TEXT
);
CREATE UNIQUE INDEX "dep_code_IDX" ON "dep" (
	"code"
);
CREATE UNIQUE INDEX "dep_name_IDX" ON "dep" (
	"name"
);

CREATE TABLE "dep_word" (
    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    "dep_id" INTEGER NOT NULL,
    "code_word"  TEXT NULL,
    CONSTRAINT dep_word_dep_id_FK FOREIGN KEY (dep_id) REFERENCES dep(id)
);



