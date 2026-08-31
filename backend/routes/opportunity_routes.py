from flask import Blueprint, jsonify, request
from services.opportunity_service import (
    get_all_opportunities_with_matches,
    get_opportunity_details,
    get_recommended,
    get_stats,
    add_opportunity
)

opportunity_bp = Blueprint("opportunity", __name__, url_prefix="/api")

@opportunity_bp.route("/opportunities", methods=["GET"])
def list_opportunities():
    """List opportunities with optional query, filters, and match scores."""
    try:
        query = request.args.get("q", default=None)
        job_type = request.args.get("job_type", default=None)
        location = request.args.get("location", default=None)
        min_match = request.args.get("min_match", default=0)
        sort_by = request.args.get("sort_by", default="match")

        results = get_all_opportunities_with_matches(
            query=query,
            job_type=job_type,
            location=location,
            min_match=min_match,
            sort_by=sort_by
        )
        return jsonify({
            "success": True,
            "count": len(results),
            "data": results
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@opportunity_bp.route("/opportunities/<int:opp_id>", methods=["GET"])
def get_opportunity(opp_id):
    """Fetch single opportunity details with skill match breakdown."""
    try:
        opp = get_opportunity_details(opp_id)
        if not opp:
            return jsonify({"success": False, "error": "Opportunity not found"}), 404
        return jsonify({
            "success": True,
            "data": opp
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@opportunity_bp.route("/opportunities/recommended", methods=["GET"])
def get_recommended_opportunities():
    """Retrieve top matched opportunities."""
    try:
        limit = request.args.get("limit", default=8, type=int)
        job_type = request.args.get("job_type", default=None)
        results = get_recommended(limit=limit, job_type=job_type)
        return jsonify({
            "success": True,
            "count": len(results),
            "data": results
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@opportunity_bp.route("/stats", methods=["GET"])
def get_dashboard_stats():
    """Summary metrics for the dashboard."""
    try:
        stats = get_stats()
        return jsonify({
            "success": True,
            "data": stats
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@opportunity_bp.route("/opportunities", methods=["POST"])
def create_opportunity():
    """Add a new opportunity."""
    try:
        data = request.get_json() or {}
        required_fields = ["title", "company", "location", "job_type", "required_skills", "qualification", "description", "application_link"]
        for f in required_fields:
            if f not in data:
                return jsonify({"success": False, "error": f"Missing required field: {f}"}), 400
        opp = add_opportunity(data)
        return jsonify({
            "success": True,
            "message": "Opportunity created successfully",
            "data": opp.to_dict()
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
