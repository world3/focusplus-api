from extensions import db

class Stat(db.Model):
    __tablename__ = 'stat'

    id = db.Column(db.Integer, primary_key=True)
    stat_key = db.Column(db.String(8), nullable=False, index=True)
    pomos = db.Column(db.String(256), nullable=False)
    breaks = db.Column(db.String(256), nullable=False)
    totalPomos = db.Column(db.Integer, nullable=False)
    totalBreaks = db.Column(db.Integer, nullable=False)
    interruptions = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    @classmethod
    def get_range(cls, user_id, start_day, end_day):
        return cls.query.filter(
            Stat.user_id == user_id,
            Stat.stat_key >= start_day,
            Stat.stat_key <= end_day
        )

    def save(self):
        db.session.add(self)
        db.session.commit()

