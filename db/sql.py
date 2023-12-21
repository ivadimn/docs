query = {
    "Position": {
        "_SELECT": """
            SELECT p.id, p.name, p.group_id, gp.name 
                FROM position p LEFT OUTER JOIN group_position gp ON gp.id = p.group_id 
                ORDER BY gp.level; 
        """,
        "_INSERT": "INSERT INTO position (name, group_id) VALUES(?, ?) ;",
        "_UPDATE": "UPDATE position SET name=?, group_id=? WHERE id=? ;",
        "_DELETE": "DELETE FROM position WHERE id=? ;",
        "_SELECT_ONE": """
            SELECT p.id, p.name, p.group_id, gp.name 
                FROM position p LEFT OUTER JOIN group_position gp ON gp.id = p.group_id
                WHERE p.id=? ; 
        """,
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
    "GroupPosition": {
        "_SELECT": "SELECT id, name, level FROM group_position ORDER BY level ; ",
        "_INSERT": "INSERT INTO group_position (name, level) VALUES(?, ?) ;",
        "_UPDATE": "UPDATE group_position SET name=?, level=? WHERE id=? ;",
        "_DELETE": "DELETE FROM group_position WHERE id=? ;",
        "_SELECT_ONE": "SELECT id, name, level FROM group_position WHERE id=? ;",
        "_SELECT_BY_NAME": "SELECT id, name, level FROM group_position WHERE name=? ;",
        "_INSERT_TMP": "",
        "_DELETE_TMP": "",
        "_INSERT_LOADED": "",
    },
    "Org": {
        "_SELECT_FOR_LOAD": """
            SELECT id, code, name, parent_id, created_at, closed_at
                FROM org ; 
        """,
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
        "_SELECT_LEVEL_CHILD": """
            SELECT id, code, name, parent_id, created_at FROM org WHERE parent_id=?; 
        """,
        "_SELECT_PARENTS": """
            SELECT parent_id FROM tree_path WHERE child_id = ? AND parent_id <> child_id ;
        """,
        "_INSERT": "INSERT INTO org (code, name, parent_id) VALUES(?, ?, ?); ",
        "_INSERT_TREE_PATH": "INSERT INTO tree_path (parent_id, child_id) VALUES(?, ?) ;",
        "_UPDATE": "",
        "_DELETE": "",
        "_SELECT_ONE": "SELECT id, code, name, parent_id, created_at FROM org WHERE id=? ;",
        "_SELECT_BY_NAME": "SELECT id, code, name, parent_id, created_at FROM org WHERE name=? ;",
        "_INSERT_TMP": "",
        "_DELETE_TMP": "",
        "_CLOSE": "UPDATE org SET closed_at=datetime('now','localtime') WHERE id=? ;"
    },
    "Face": {
        "_SELECT": """
            SELECT id, snils, birthday FROM face ; 
        """,
        "_INSERT": "INSERT INTO face (snils, birthday) VALUES (?, ?) ;",
        "_UPDATE": "",
        "_DELETE": "",
        "_SELECT_ONE": "SELECT id, code, name, parent_id, created_at FROM org WHERE id=? ;",
        "_SELECT_BY_NAME": "SELECT id, code, name, parent_id, created_at FROM org WHERE name=? ;",
        "_INSERT_TMP": """
             INSERT INTO tmp_face (snils, birthday, tn, firstname, name, fathername, org_name, position) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?) ; 
        """,
        "_DELETE_TMP": "DELETE FROM tmp_face ; ",
        "_INSERT_LOADED": """
            INSERT INTO face (snils, birthday) 
                SELECT snils, birthday 
                FROM tmp_face
                WHERE snils not in ( SELECT snils FROM face) ; 
        """,
    },
    "Pd": {
        "_SELECT": """
            SELECT id, face_id, firstname, name, fathername FROM pd
                WHERE closed_at is NULL; 
        """,
        "_INSERT": """
            INSERT INTO pd (face_id, firstname, name, fathername) 
                VALUES (?, ?, ?, ?) ;
        """,
        "_UPDATE": "",
        "_DELETE": "",
        "_SELECT_ONE": "SELECT id, face_id, firstname, name, fathername FROM pd WHERE id=? ;",
        "_SELECT_BY_NAME": "",
        "_SELECT_TMP": """
            SELECT f.id, t.firstname, t.name, t.fathername
                FROM face f INNER JOIN tmp_face t ON t.snils = f.snils ; 
        """,
        "_DELETE_TMP": "",
        "_INSERT_LOADED": "",
        "_CLOSE": "UPDATE pd SET closed_at=datetime('now','localtime') WHERE id=? ;",
    },
    "Shtat": {
        "_SELECT": """
            SELECT id, org_id, pos_id, tn, pd_id created_at FROM shtat
                WHERE closed_at is NULL; 
        """,
        "_INSERT": """
            INSERT INTO shtat (org_id, pos_id, tn, pd_id ) 
                VALUES (?, ?, ?, ?) ;
        """,
        "_UPDATE": "",
        "_DELETE": "",
        "_SELECT_ONE": "SELECT id, org_id, pos_id, tn, pd_id created_at FROM shtat WHERE id=? ;",
        "_SELECT_BY_NAME": "",
        "_SELECT_TMP": """
            SELECT o.id, pos.id, t.tn, p.id
                FROM face f INNER JOIN tmp_face t ON t.snils = f.snils
                    INNER JOIN "position" pos ON pos.name = t."position"
                    INNER JOIN org o ON o.name = t.org_name 
                    INNER JOIN pd p ON p.face_id = f.id ;
        """,
        "_DELETE_TMP": "",
        "_INSERT_LOADED": "",
        "_CLOSE": "UPDATE shtat SET closed_at=datetime('now','localtime') WHERE id=? ;",
    },
    "Staff": {
        "_SELECT": """
           SELECT pos.name, s.tn, p.firstname, p.name, p.fathername  
               FROM shtat s INNER JOIN "position" pos ON pos.id = s.pos_id
                   INNER JOIN pd p ON p.id = s.pd_id ; 
       """,
        "_SELECT_FACES": """
           SELECT pos.name, s.tn, p.firstname, p.name, p.fathername  
               FROM shtat s INNER JOIN "position" pos ON pos.id = s.pos_id
                   INNER JOIN pd p ON p.id = s.pd_id 
                   WHERE s.org_id=? ; 
       """,
    },

}
