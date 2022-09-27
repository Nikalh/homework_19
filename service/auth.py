from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES, TOKEN_EXPIRE_DAY
import hashlib
import base64
import calendar
import datetime

import jwt


def __generate_password_digest(password):
    return hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),  # Convert the password to bytes
        salt=PWD_HASH_SALT,
        iterations=PWD_HASH_ITERATIONS
    )


def generate_password_has(password):
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compare_password(password_user, password_hash):
    """
    Сравнение паролей
    :param password_user: пароль пользователя
    :param password_hash: пароль в хеше
    :return:
    """
    return generate_password_has((password_user)) == password_hash


def generate_token(username, password_hash, password, is_refresh=True):
    if username is None:
        return None
    if not is_refresh:
        if not compare_password(password_user=password, password_hash=password_hash):
            return None

        data = {
            "username": username,
            "password": password
        }

        # время действия токена 15 минут
        min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        data['exp'] = calendar.timegm(min15.timetuple())
        access_token = jwt.encode(data, key=SECRET_KEY, algorithm=ALGORITHM)

        # время действия токена дней
        min_day = datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRE_DAY)
        data['exp'] = calendar.timegm(min_day.timetuple())
        refresh_token = jwt.encode(data, key=SECRET_KEY, algorithm=ALGORITHM)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token

        }


def approve_token(token):
    data = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)

    username = data.get('username')
    password = data.get('password')

    return generate_token(username=username, password=password, password_hash=None, is_refresh=True)
