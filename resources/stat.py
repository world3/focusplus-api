from datetime import datetime, timedelta, date
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus
import json

from models.stat import Stat
from schemas.stat import StatSchema
from models.history import History

stat_list_schema = StatSchema(many=True)


class StatListResource(Resource):
    @jwt_required
    def get(self, start, end):
        current_user = get_jwt_identity()
        stats = Stat.get_range(current_user, start, end)

        start_date = datetime.strptime(start, '%Y%m%d').date()
        end_date = datetime.strptime(end, '%Y%m%d').date()
        if (end_date - start_date).days + 1 > stats.count():
            stat_dict = {stat.stat_key: stat for stat in stats}
            for stat_date in self.date_range(start_date, end_date):
                key = stat_date.strftime('%Y%m%d')
                if key not in stat_dict:
                    stat = self.create_statistics(current_user, key)

            stats = Stat.get_range(current_user, start, end)

        return stat_list_schema.dump(stats), HTTPStatus.OK

    @classmethod
    def create_statistics(cls, user_id, stat_date):
        histories = History.get_by_user_id(user_id, stat_date)
        pomos = [0] * 24
        breaks = [0] * 24
        total_pomos = 0
        total_breaks = 0
        interruptions = 0
        day_start = datetime.strptime(stat_date, '%Y%m%d')
        for history in histories:
            start_time = history.start
            end_time = history.end
            index = ((start_time - day_start).seconds + history.utc_offset * 60) // 3600
            minutes = (end_time - start_time).seconds // 60
            if history.type == 'Pomodoro':
                pomos[index] += minutes
                total_pomos += minutes
                if history.status == 'Interrupted':
                    interruptions += 1
            else:
                breaks[index] += minutes
                total_breaks += minutes

        stat = Stat(stat_key=stat_date, pomos=json.dumps(pomos), breaks=json.dumps(breaks), totalPomos=total_pomos,
                    totalBreaks=total_breaks, interruptions=interruptions, user_id=user_id)
        stat.save()

        return stat

    @classmethod
    def date_range(cls, start_date, end_date):
        for i in range((end_date - start_date).days + 1):
            yield start_date + timedelta(i)
