from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')  # Inversely, it tell SqlAlchemy there is items related to
    # the Store ie. a back reference.  Furthermore, adding lazy='dynamic' will make the it a query builder as such you
    # would need self.items.all() since it can be expensive to create an object for each item

    def __init__(self, name: str):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}  # Need to use all() in
        # self.items as lazy='dynamic' prevents too many items (expensive) thus all() is used as a query builder

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
