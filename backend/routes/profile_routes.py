from flask import Blueprint, jsonify, request
from services.profile_service import get_current_profile, update_profile

profile_bp = Blueprint("profile", __name__, url_prefix="/api/profile")

@profile_bp.route("", methods=["GET"])
def get_profile():
    """Retrieve active user profile."""
    try:
        profile = get_current_profile()
        return jsonify({
            "success": True,
            "data": profile.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@profile_bp.route("", methods=["PUT", "POST"])
def edit_profile():
    """Update profile data."""
    try:
        data = request.get_json() or {}
        profile = update_profile(data)
        return jsonify({
            "success": True,
            "message": "Profile updated successfully",
            "data": profile.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
