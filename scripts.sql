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