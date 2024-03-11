import sqlite3

class EntityDatabase():
    def __init__(self):
        self.conn = sqlite3.connect("entities.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        # Format: | ID | Relation | Count |
        self.cursor.execute("CREATE TABLE IF NOT EXISTS relations (id INTEGER PRIMARY KEY AUTOINCREMENT, relation TEXT, count INTEGER)")
        # Format: | Entity | Relations | Count |
        # ...where Relations is a list of relation ids the entity is involved in
        self.cursor.execute("CREATE TABLE IF NOT EXISTS entities (entity TEXT PRIMARY KEY, relations TEXT, count INTEGER)")

    def upload_relation(self, relation):
        """
        Upload relation with unique id, and return id for entity linking
        """
        self.cursor.execute("SELECT count FROM relations WHERE relation=?", (relation,))
        count = self.cursor.fetchone()
        if count:
            count = count[0]
            self.cursor.execute("UPDATE relations SET count = count + 1 WHERE relation=?", (relation,))
        else:
            self.cursor.execute("INSERT INTO relations (relation, count) VALUES (?, 1)", (relation,))
        self.conn.commit()
        # Return the ID of the currently selected row
        return self.cursor.lastrowid

    def upload_entity(self, entity, relation_id):
        """
        Upload entity or add relation_id to associated relations
        """
        self.cursor.execute("SELECT relations FROM entities WHERE entity=?", (entity,))
        relations = self.cursor.fetchone()
        if relations:
            if relation_id in relations[0].split(", "):
                relations = relations
            else:
                relations = f"{relations[0]}, {relation_id}"
            self.cursor.execute("UPDATE entities SET relations = ?, count = count + 1 WHERE entity=?", (relations, entity))
        else:
            self.cursor.execute("INSERT INTO entities (entity, relations, count) VALUES (?, ?, 1)", (entity, relation_id))
        self.conn.commit()

    def get_entities_and_relations(self):
        """
        Return entities and linked relations in dict format:
        {entity: {count: int, relations: [{relation: str, count: int}, ...]}, ...}
        """
        entity_dict = {}
        self.cursor.execute("SELECT * FROM entities")
        entities = self.cursor.fetchall()
        for entity, relations, count in entities:
            entity_dict[entity] = {"count": count}
            relation_ids = "(" + relations + ")"
            self.cursor.execute(f"SELECT relation, count FROM relations WHERE id IN {relation_ids}")
            relations = self.cursor.fetchall()
            relations = [{"relation": relation[0], "count": relation[1]} for relation in relations]
            entity_dict[entity]["relations"] = relations
        return entity_dict
    
    def delete_all(self):
        self.cursor.execute("DELETE FROM relations")
        self.cursor.execute("DELETE FROM entities")
        self.conn.commit()