import json
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False, default="Alex Chen")
    email = Column(String(120), nullable=True, default="alex.chen@university.edu")
    education = Column(String(200), nullable=False, default="B.S. in Computer Science (Senior)")
    university = Column(String(200), nullable=True, default="State University of Technology")
    skills = Column(Text, nullable=False, default=json.dumps(["Python", "SQL", "Machine Learning", "React", "Git"]))
    area_of_interest = Column(String(200), nullable=False, default="Software Engineering & Data Science")
    location = Column(String(120), nullable=False, default="New York, NY")
    experience = Column(String(120), nullable=False, default="1 Year (Academic Projects & Summer Internship)")
    preference = Column(String(50), nullable=False, default="Both")  # 'Internship', 'Job', or 'Both'
    bio = Column(Text, nullable=True, default="Passionate computer science student looking for exciting opportunities to build impactful software products and data pipelines.")
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def get_skills_list(self):
        try:
            return json.loads(self.skills) if self.skills else []
        except Exception:
            return [s.strip() for s in self.skills.split(",") if s.strip()]

    def set_skills_list(self, skills_list):
        self.skills = json.dumps(skills_list if isinstance(skills_list, list) else [])

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "education": self.education,
            "university": self.university,
            "skills": self.get_skills_list(),
            "area_of_interest": self.area_of_interest,
            "location": self.location,
            "experience": self.experience,
            "preference": self.preference,
            "bio": self.bio,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Opportunity(Base):
    __tablename__ = 'opportunities'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    company = Column(String(150), nullable=False)
    location = Column(String(150), nullable=False)
    is_remote = Column(String(50), default="Hybrid") # On-site, Remote, Hybrid
    job_type = Column(String(50), nullable=False)   # 'Internship' or 'Job'
    required_skills = Column(Text, nullable=False)   # JSON array
    qualification = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    salary_or_stipend = Column(String(100), nullable=True)
    source = Column(String(100), nullable=False, default="Direct Portal")
    application_link = Column(String(300), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def get_skills_list(self):
        try:
            return json.loads(self.required_skills) if self.required_skills else []
        except Exception:
            return [s.strip() for s in self.required_skills.split(",") if s.strip()]

    def set_skills_list(self, skills_list):
        self.required_skills = json.dumps(skills_list if isinstance(skills_list, list) else [])

    def to_dict(self, match_info=None):
        data = {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "is_remote": self.is_remote,
            "job_type": self.job_type,
            "required_skills": self.get_skills_list(),
            "qualification": self.qualification,
            "description": self.description,
            "salary_or_stipend": self.salary_or_stipend,
            "source": self.source,
            "application_link": self.application_link,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        if match_info is not None:
            data.update(match_info)
        return data
