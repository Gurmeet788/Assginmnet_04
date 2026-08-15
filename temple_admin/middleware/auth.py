from functools import wraps

from flask import request, jsonify

from supabase_client import supabase


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "error": "Authorization header is missing"
            }), 401

        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({
                "error": "Invalid Authorization header"
            }), 401

        token = parts[1]

        try:
            user_response = supabase.auth.get_user(token)

        except Exception:
            return jsonify({
                "error": "Invalid or expired token"
            }), 401

        return f(user_response.user, *args, **kwargs)

    return decorated


def require_admin(f):
    @wraps(f)
    def decorated(user, *args, **kwargs):
         role = user.app_metadata.get("role")
         if role != "admin":
            return jsonify({
                "error": "Admin access required"
                }), 403
         return f(user, *args, **kwargs)

    return decorated