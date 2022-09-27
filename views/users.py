from flask_restx import Resource, Namespace
from flask import request

from dao.model.user  import User, UserSchema
from implemented import user_service
from setup_db import db

user_ns = Namespace('users')


@user_ns.route('/')
class UserView(Resource):
    def get(self):
        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200
    def post(self):
        req_json = request.json
        if not (req_json.get('username') and req_json.get('password') and req_json.get('role')):
            return 'Что-то не передали'
        user =user_service.create(req_json)
        return "", 201, {"location": f"/users/{user.id}"}

@user_ns.route('/<int:rid>')
class UserView(Resource):
    def get(self, rid):
        r = user_service.get_one(rid)
        sm_d = UserSchema().dump(r)
        return sm_d, 200

        # Обновляем данные
    def put(self, rid):
        req_json = request.json

        try:
            if 'id' not in req_json:
                req_json['id'] = rid
                user_service.update(req_json)
            return "Данные обновлены", 204
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Неудачное обновление", 500

    # Удаляем
    def delete(self, rid):
        user_service.delete(rid)
        return "Данные удалены", 204

