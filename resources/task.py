from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus
from marshmallow import ValidationError

from models.task import Task
from schemas.task import TaskSchema

task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)


class TaskListResource(Resource):
    @jwt_required
    def get(self, type):
        if type not in ['active', 'backlog', 'trash', 'archive']:
            return  {'message': 'Invalid task type: ' + type }, HTTPStatus.BAD_REQUEST

        current_user = get_jwt_identity()
        tasks = Task.get_all(current_user, type)
        result = task_list_schema.dump(tasks)
        # return task_list_schema.dump(tasks), HTTPStatus.OK
        return result, HTTPStatus.OK

    @jwt_required
    def post(self, type):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        try:
            data = task_schema.load(data=json_data)
        except ValidationError as errors:
            return {'message': 'Validation errors', 'errors': errors.messages}, HTTPStatus.BAD_REQUEST

        task = Task(**data)
        task.user_id = current_user
        task.type = type
        task.save()

        return task_schema.dump(task), HTTPStatus.CREATED


class TaskResource(Resource):
    @jwt_required
    def get(self, task_id):
        task = Task.get_by_id(task_id=task_id)
        if task is None:
            return {'message': 'task not found'}, HTTPStatus.NOT_FOUND

        return task_schema.dump(task), HTTPStatus.OK

    @jwt_required
    def put(self, task_id):
        json_data = request.get_json()
        try:
            data = task_schema.load(data=json_data)
        except ValidationError as errors:
            return {'message': 'Validation errors', 'errors': errors.messages}, HTTPStatus.BAD_REQUEST

        task = Task.get_by_id(task_id)
        if task is None:
            return {'message': 'task not found'}, HTTPStatus.NOT_FOUND

        task.title = data['title']
        task.description = data['description']
        task.priority = data['priority']
        task.type = data['type']
        task.status = data['status']
        task.due_date = data['due_date']
        task.start = data['start']
        task.end = data['end']
        task.save()

        return task_schema.dump(task), HTTPStatus.OK

    @jwt_required
    def delete(self, task_id):
        task = Task.get_by_id(task_id)
        if task is None:
            return {'message': 'task not found'}, HTTPStatus.NOT_FOUND

        dumped = task_schema.dump(task)
        Task.delete(task_id)

        return dumped, HTTPStatus.OK



