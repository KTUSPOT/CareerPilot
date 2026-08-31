from sqlalchemy import or_
from database import db_session
from models import Opportunity
from services.matcher import calculate_match
from services.profile_service import get_current_profile

def get_all_opportunities_with_matches(query=None, job_type=None, location=None, min_match=0, sort_by="match"):
    """
    Retrieves opportunities, calculates real-time match stats against current user's profile,
    and applies search, filtering, and sorting.
    """
    profile = get_current_profile()
    user_skills = profile.get_skills_list() if profile else []

    all_opps = db_session.query(Opportunity).all()
    results = []

    query_str = query.strip().lower() if query else None
    job_type_str = job_type.strip().lower() if job_type else None
    loc_str = location.strip().lower() if location else None
    try:
        min_match_val = int(min_match)
    except (ValueError, TypeError):
        min_match_val = 0

    for opp in all_opps:
        # Calculate matching breakdown
        match_info = calculate_match(user_skills, opp.get_skills_list())

        # Filtering: Job Type
        if job_type_str and job_type_str != "all":
            if opp.job_type.lower() != job_type_str:
                continue

        # Filtering: Location / Remote
        if loc_str and loc_str != "all":
            loc_match = (
                loc_str in opp.location.lower()
                or (loc_str == "remote" and opp.is_remote.lower() == "remote")
                or (loc_str == "hybrid" and opp.is_remote.lower() == "hybrid")
                or (loc_str == "on-site" and opp.is_remote.lower() == "on-site")
            )
            if not loc_match:
                continue

        # Filtering: Search Query (Title, Company, Skills, Description)
        if query_str:
            title_match = query_str in opp.title.lower()
            company_match = query_str in opp.company.lower()
            desc_match = query_str in opp.description.lower()
            skill_match = any(query_str in s.lower() for s in opp.get_skills_list())
            if not (title_match or company_match or desc_match or skill_match):
                continue

        # Filtering: Min Match
        if match_info["match_percentage"] < min_match_val:
            continue

        results.append(opp.to_dict(match_info=match_info))

    # Sorting
    if sort_by == "match":
        results.sort(key=lambda x: x["match_percentage"], reverse=True)
    elif sort_by == "title":
        results.sort(key=lambda x: x["title"].lower())
    elif sort_by == "company":
        results.sort(key=lambda x: x["company"].lower())
    elif sort_by == "newest":
        results.sort(key=lambda x: x.get("created_at") or "", reverse=True)

    return results

def get_opportunity_details(opp_id: int):
    """Fetches details for a single opportunity including match calculations."""
    opp = db_session.query(Opportunity).filter(Opportunity.id == opp_id).first()
    if not opp:
        return None

    profile = get_current_profile()
    user_skills = profile.get_skills_list() if profile else []
    match_info = calculate_match(user_skills, opp.get_skills_list())

    return opp.to_dict(match_info=match_info)

def get_recommended(limit=8, job_type=None):
    """Returns top opportunities ranked descending by match percentage."""
    profile = get_current_profile()
    user_skills = profile.get_skills_list() if profile else []

    all_opps = db_session.query(Opportunity).all()
    results = []

    user_pref = profile.preference.lower() if profile and profile.preference else "both"
    target_type = job_type.lower() if job_type and job_type.lower() != "all" else None

    for opp in all_opps:
        # If user explicitly filtered job_type, respect it; otherwise if user profile preference is specific ('internship' or 'job'), give priority or filter
        if target_type:
            if opp.job_type.lower() != target_type:
                continue

        match_info = calculate_match(user_skills, opp.get_skills_list())
        results.append(opp.to_dict(match_info=match_info))

    # Sort descending by match percentage
    results.sort(key=lambda x: x["match_percentage"], reverse=True)
    return results[:limit]

def get_stats():
    """Computes summary statistics for Dashboard view."""
    profile = get_current_profile()
    user_skills = profile.get_skills_list() if profile else []

    all_opps = db_session.query(Opportunity).all()
    total_opps = len(all_opps)
    internships_count = sum(1 for o in all_opps if o.job_type.lower() == "internship")
    jobs_count = sum(1 for o in all_opps if o.job_type.lower() == "job")

    matches = [calculate_match(user_skills, o.get_skills_list())["match_percentage"] for o in all_opps]
    high_match_count = sum(1 for m in matches if m >= 75)
    moderate_match_count = sum(1 for m in matches if 40 <= m < 75)
    max_match = max(matches) if matches else 0
    avg_match = round(sum(matches) / max(len(matches), 1)) if matches else 0

    return {
        "total_opportunities": total_opps,
        "internships_count": internships_count,
        "jobs_count": jobs_count,
        "high_match_count": high_match_count,
        "moderate_match_count": moderate_match_count,
        "max_match": max_match,
        "avg_match": avg_match,
        "user_skill_count": len(user_skills)
    }

def add_opportunity(data: dict) -> Opportunity:
    """Helper to add new opportunity (for Phase 2 API ingestion/admin)."""
    opp = Opportunity(
        title=data["title"],
        company=data["company"],
        location=data["location"],
        is_remote=data.get("is_remote", "Hybrid"),
        job_type=data["job_type"],
        required_skills=data.get("required_skills", []),
        qualification=data["qualification"],
        description=data["description"],
        salary_or_stipend=data.get("salary_or_stipend"),
        source=data.get("source", "Direct Submission"),
        application_link=data["application_link"]
    )
    if isinstance(data.get("required_skills"), list):
        opp.set_skills_list(data["required_skills"])
    db_session.add(opp)
    db_session.commit()
    return opp
