
def define_models(db):
    """
    Define tables in SQLite database
    """
    class Relation(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        relation = db.Column(db.String(100), unique=True, nullable=False)
        count = db.Column(db.Integer, nullable=False)

    class Entity(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        entity = db.Column(db.String(100), unique=True, nullable=False)
        relations = db.Column(db.String(1000), nullable=True)
        count = db.Column(db.Integer, nullable=False)

    return Relation, Entity


class EntityDatabase:
    def __init__(self, db, app):
        self.db = db
        self.Relation, self.Entity = define_models(db)
        with app.app_context():
            self.db.create_all()

    def upload_relation(self, relation):
        """
        Upload relation with unique id, and return id for entity linking
        """
        relation_obj = self.Relation.query.filter_by(relation=relation).first()
        if relation_obj:
            relation_obj.count += 1
        else:
            relation_obj = self.Relation(relation=relation, count=1)
            self.db.session.add(relation_obj)
        self.db.session.commit()
        return relation_obj.id

    def upload_entity(self, entity_name, relation_id):
        """
        Upload entity or add relation_id to associated relations
        """
        entity = self.Entity.query.filter_by(entity=entity_name).first()
        if entity:
            relation_ids = [int(id) for id in entity.relations.split(
                ', ')] if entity.relations else []
            if relation_id not in relation_ids:
                relation_ids.append(relation_id)
                entity.relations = ', '.join(str(id) for id in relation_ids)
            entity.count += 1
        else:
            entity = self.Entity(entity=entity_name,
                                 relations=str(relation_id), count=1)
            self.db.session.add(entity)
        self.db.session.commit()

    def get_entities_and_relations(self):
        """
        Return entities and linked relations in dict format:
        {entity: {count: int, relations: [{relation: str, count: int}, ...]}, ...}
        """
        entity_dict = {}
        entities = self.Entity.query.all()
        for entity in entities:
            entity_dict[entity.entity] = {"count": entity.count}
            relation_ids = [int(id) for id in entity.relations.split(
                ', ')] if entity.relations else []
            relations = [self.Relation.query.filter_by(
                id=id).first() for id in relation_ids]
            entity_dict[entity.entity]["relations"] = [
                {"relation": relation.relation, "count": relation.count} for relation in relations]
        return entity_dict

    def delete_all(self):
        self.Relation.query.delete()
        self.Entity.query.delete()
        self.db.session.commit()
