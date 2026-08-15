from flask import Blueprint,request,jsonify
from supabase_client import supabase
from middleware.auth import require_auth
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/sigup", methods =["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    try:
        response = supabase.auth.sign_up({
            "email":email,
            "password":password
            })
    except Exception:

        return jsonify({
            "error": "Invalid input/format"
        }),400   

    return jsonify({
        "message":"sigup succesfully",
        "user_id":response.user.id
    }),201

@auth_bp.route("/auth/login",methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    try:
        response = supabase.auth.sign_in_with_password({
            "email":email,
            "password":password
            })
    except Exception:
        return jsonify({
            "error": "Invalid login credentials"
        }),404    

    return jsonify({
        "message": "login Succesfully",
        "access_token" : response.session.access_token,
        "user_id":response.user.id
    }),200


@auth_bp.route("/api/auth/logout", methods=["POST"])
@require_auth
def logout(user):
    try:
        supabase.auth.sign_out()

        return "", 204

    except Exception:
        return jsonify({
            "error": "Logout failed"
        }), 500