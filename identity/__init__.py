from functools import wraps
from flask import session, abort

def require_logged_in(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('logged_in') != True:
            abort(401)
        return f(*args, **kwargs)
    return wrapper