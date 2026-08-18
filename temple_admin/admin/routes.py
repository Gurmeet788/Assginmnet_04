from flask import Blueprint, request, jsonify

from middleware.auth import require_auth, require_admin
from supabase_client import supabase_admin, supabase
from urllib.parse import unquote

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
    

@admin_bp.route("/api/admin/announcement", methods=["PATCH"])
@require_auth
@require_admin
def update_announcement(user):
    data = request.get_json() or {}

    announcement_id = data.get("id")

    if not announcement_id:
        return jsonify({
            "error": "Announcement id is required"
        }), 400

    updates = {}

    if "title" in data:
        updates["title"] = data["title"]

    if "content" in data:
        updates["content"] = data["content"]

    if not updates:
        return jsonify({
            "error": "Nothing to update"
        }), 400

    response = (
        supabase
        .table("announcements")
        .update(updates)
        .eq("id", announcement_id)
        .execute()
    )

    if not response.data:
        return jsonify({
            "error": "Announcement not found"
        }), 404

    return jsonify({
        "message": "Announcement updated successfully",
        "announcement": response.data[0]
    }), 200

@admin_bp.route("/api/admin/gallery", methods=["POST"])
@require_auth
@require_admin
def upload_gallery_image(user):
    image = request.files.get("image")
    caption = request.form.get("caption")

    if not image:
        return jsonify({
            "error": "Image is required"
        }), 400

    filename = image.filename
    image_bytes = image.read()

    supabase_admin.storage \
        .from_("gallery") \
        .upload(filename, image_bytes)

    image_url = (
        supabase_admin
        .storage
        .from_("gallery")
        .get_public_url(filename)
    )

    gallery_response = (
        supabase_admin
        .table("gallery")
        .insert({
            "image_url": image_url,
            "caption": caption
        })
        .execute()
    )

    if not gallery_response.data:
        return jsonify({
            "error": "Failed to save gallery record"
        }), 500

    return jsonify({
        "message": "Image uploaded successfully",
        "gallery": gallery_response.data[0]
    }), 201

@admin_bp.route("/api/admin/gallery/<gallery_id>", methods=["DELETE"])
@require_auth
@require_admin
def delete_gallery_image(user, gallery_id):

    # 1. Find gallery record
    response = (
        supabase_admin
        .table("gallery")
        .select("id, image_url")
        .eq("id", gallery_id)
        .execute()
    )

    if not response.data:
        return jsonify({
            "error": "Gallery image not found"
        }), 404

    gallery_item = response.data[0]
    image_url = gallery_item["image_url"]

    # 2. Extract storage filename
    filename = image_url.split("/gallery/")[-1]
    filename = unquote(filename)
    
    print("IMAGE URL:", image_url)
    print("FILENAME:", filename)
    # 3. Delete actual image from Storage
    supabase_admin.storage \
        .from_("gallery") \
        .remove([filename])

    # 4. Delete database record
    supabase_admin \
        .table("gallery") \
        .delete() \
        .eq("id", gallery_id) \
        .execute()

    return jsonify({
        "message": "Gallery image deleted successfully"
    }), 200