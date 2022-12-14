from flask_restx import Resource, Namespace
from flask import request

from implemented import user_service
from service.auth import generate_token, approve_token

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        username = req_json.get('username')
        password = req_json.get('password')
        if not username and not password:
            return 'Что-то не передано', 401
        user = user_service.get_by_username(username=username)
        if user:
            return generate_token(
                username=username,
                password=password,
                password_hash=user.password,
                is_refresh=False
            )
    def put(self):
        req_json = request.json
        if not req_json.get('refresh_token'):
            return 'refresh_token не передан', 401

        return approve_token(token=req_json.get('refresh_token')), 200



