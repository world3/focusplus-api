from extensions import db


class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, nullable=False)
    task_title = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(32), nullable=False)
    start = db.Column(db.DateTime(), nullable=False)
    end = db.Column(db.DateTime(), nullable=False)
    status = db.Column(db.String(16), nullable=False)
    txn_date = db.Column(db.Date())
    utc_offset = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @classmethod
    def get_by_user_id(cls, user_id, txn_date):
        return cls.query.filter_by(user_id=user_id, txn_date=txn_date)

    def save(self):
        db.session.add(self)
        db.session.commit()
