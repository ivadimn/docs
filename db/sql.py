query = {
    "Position": {
        "_SELECT": "SELECT id, name, group_id FROM position ; ",
        "_INSERT": "INSERT INTO position (name) VALUES(?) ;",
        "_UPDATE": "UPDATE position SET name=?, group_id=? WHERE id=? ;",
        "_DELETE": "DELETE FROM position WHERE id=? ;",
        "_SELECT_ONE": "SELECT id, name, group_id FROM position WHERE id=? ;",
        "_SELECT_BY_NAME": "SELECT id, name, group_id FROM position WHERE name=? ;",
        "_INSERT_TMP": "INSERT INTO tmp_pos (name) VALUES(?) ;",
        "_DELETE_TMP": "DELETE FROM tmp_pos ; ",
        "_INSERT_LOADED": """
            INSERT INTO position (name) 
            SELECT name 
                FROM tmp_pos
                WHERE name not in ( SELECT name FROM position) ;
        """,
    },
    "Org": {
        "_SELECT": """
            SELECT id, code, name, parent_id, created_at 
                FROM org 
                WHERE closed_at is NULL ; 
        """,
        "_SELECT_FIRST_LEVEL": """
            SELECT id, code, name, parent_id, created_at 
                FROM org 
                WHERE parent_id is NULL and closed_at is NULL 
                ORDER BY code ; 
        """,
        "_SELECT_PARENTS": """
            SELECT parent_id FROM tree_path WHERE child_id = ? AND parent_id <> child_id ;
        """,
        "_INSERT": "INSERT INTO org (code, name, parent_id, created_at, closed_at) VALUES(?, ?, ?, ?, ?); ",
        "_INSERT_TREE_PATH": "INSERT INTO tree_path (parent_id, child_id) VALUES(?, ?) ;",
        "_UPDATE": "",
        "_DELETE": "",
        "_SELECT_ONE": "SELECT id, code, name, parent_id, created_at FROM org WHERE id=? ;",
        "_SELECT_BY_NAME": "SELECT id, code, name, parent_id, created_at FROM org WHERE name=? ;",
        "_INSERT_TMP": "",
        "_DELETE_TMP": "DELETE FROM org WHERE id=?; ",
        "_INSERT_LOADED": "",
        "_CLOSE": "UPDATE org SET closed_at=? WHERE id=? ;"
    },
}