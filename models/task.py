from extensions import db


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    priority = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(32), nullable=False)
    due_date = db.Column(db.Date())
    start = db.Column(db.DateTime())
    end = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    @classmethod
    def get_all(cls, user_id, type):
        return cls.query.filter_by(user_id=user_id, type=type)

    @classmethod
    def get_by_id(cls, task_id):
        return cls.query.filter_by(id=task_id).first()

    @classmethod
    def delete(cls, task_id):
        cls.query.filter_by(id=task_id).delete()
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()


