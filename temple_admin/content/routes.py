from flask import Blueprint, jsonify

from supabase_client import supabase


content_bp = Blueprint("content", __name__)


@content_bp.route("/api/announcement", methods=["GET"])
def get_announcement():
    response = (
        supabase
        .table("announcements")
        .select("*")
        .limit(1)
        .execute()
    )

    if not response.data:
        return jsonify({
            "error": "Announcement not found"
        }), 404

    return jsonify(response.data[0]), 200

@content_bp.route("/api/gallery", methods=["GET"])
def get_gallery():
    response = (
        supabase
        .table("gallery")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return jsonify(response.data), 200
