import json
from database import db_session
from models import UserProfile

def get_current_profile() -> UserProfile:
    """Fetches the active user profile or creates default if missing."""
    profile = db_session.query(UserProfile).first()
    if not profile:
        from seed_data import seed_database
        seed_database()
        profile = db_session.query(UserProfile).first()
    return profile

def update_profile(data: dict) -> UserProfile:
    """Updates user profile fields."""
    profile = get_current_profile()
    if "name" in data:
        profile.name = str(data["name"]).strip()
    if "email" in data:
        profile.email = str(data["email"]).strip()
    if "education" in data:
        profile.education = str(data["education"]).strip()
    if "university" in data:
        profile.university = str(data["university"]).strip()
    if "skills" in data:
        skills = data["skills"]
        if isinstance(skills, list):
            profile.set_skills_list([s.strip() for s in skills if str(s).strip()])
        elif isinstance(skills, str):
            profile.set_skills_list([s.strip() for s in skills.split(",") if s.strip()])
    if "area_of_interest" in data:
        profile.area_of_interest = str(data["area_of_interest"]).strip()
    if "location" in data:
        profile.location = str(data["location"]).strip()
    if "experience" in data:
        profile.experience = str(data["experience"]).strip()
    if "preference" in data:
        profile.preference = str(data["preference"]).strip()
    if "bio" in data:
        profile.bio = str(data["bio"]).strip()

    db_session.commit()
    return profile
