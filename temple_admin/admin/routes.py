from flask import Blueprint, request, jsonify

from middleware.auth import require_auth, require_admin
from supabase_client import supabase_admin


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/api/admin/admins", methods=["POST"])
@require_auth
@require_admin
def create_admin(user):
    data = request.get_json() or {}

    email = data.get("email")

    if not email:
        return jsonify({
            "error": "Email is required"
        }), 400

    try:
        users = supabase_admin.auth.admin.list_users()

        target_user = next(
            (u for u in users if u.email == email),
            None
        )

        if target_user is None:
            return jsonify({
                "error": "User not found"
            }), 404

        supabase_admin.auth.admin.update_user_by_id(
            target_user.id,
            {
                "app_metadata": {
                    "role": "admin"
                }
            }
        )

        return jsonify({
            "message": "User promoted to admin",
            "user_id": target_user.id
        }), 200

    except Exception:
        return jsonify({
            "error": "Failed to promote user"
        }), 500