from extensions import db


class Setting(db.Model):
    __tablename__ = 'setting'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(128), nullable=False)
    value = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @classmethod
    def get_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    @classmethod
    def save(cls, settings):
        for setting in settings:
            db.session.add(setting)

        db.session.commit()
