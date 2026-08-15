from flask import Blueprint,request,jsonify
from supabase_client import supabase
from middleware.auth import require_admin,require_auth

pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/admin/page/dashbord", methods = ["GET"])

@require_auth
def dashbord(user):
    return jsonify({
    "message": "Welcome to admin dashboard",
    "user" : user.email
}),200