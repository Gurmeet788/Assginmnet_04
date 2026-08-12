from flask import Blueprint,request,jsonify
from supabase_client import supabase

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/sigup", methods =["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    response = supabase.auth.sign_up({
        "email":email,
        "password":password
    })
    return jsonify({
        "message":"sigup succesfully",
        "user_id":response.user.id
    }),201

@auth_bp.route("/auth/login",methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    response = supabase.auth.sign_in_with_password({
        "email":email,
        "password":password
    })

    return jsonify({
        "message": "login Succesfully",
        "access_token" : response.session.access_token,
        "user_id":response.user.id
    }),200