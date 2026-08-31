import re

# Synonym and alias map for normalized skill comparison
SKILL_ALIASES = {
    "react": "react",
    "react.js": "react",
    "reactjs": "react",
    "react native": "react native",
    "reactnative": "react native",
    "python": "python",
    "python3": "python",
    "py": "python",
    "js": "javascript",
    "javascript": "javascript",
    "ecmascript": "javascript",
    "ts": "typescript",
    "typescript": "typescript",
    "node": "node.js",
    "nodejs": "node.js",
    "node.js": "node.js",
    "ml": "machine learning",
    "machine learning": "machine learning",
    "ai": "artificial intelligence",
    "artificial intelligence": "artificial intelligence",
    "dl": "deep learning",
    "deep learning": "deep learning",
    "nlp": "natural language processing",
    "natural language processing": "natural language processing",
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "mongo": "mongodb",
    "mongodb": "mongodb",
    "aws": "aws",
    "amazon web services": "aws",
    "gcp": "google cloud",
    "google cloud platform": "google cloud",
    "google cloud": "google cloud",
    "k8s": "kubernetes",
    "kubernetes": "kubernetes",
    "docker": "docker",
    "ci/cd": "ci/cd",
    "cicd": "ci/cd",
    "rest": "rest apis",
    "rest api": "rest apis",
    "rest apis": "rest apis",
    "restful apis": "rest apis",
    "restful api": "rest apis",
    "sql": "sql",
    "html": "html",
    "html5": "html",
    "css": "css",
    "css3": "css",
    "c++": "c++",
    "cpp": "c++",
    "c#": "c#",
    "csharp": "c#",
    "ui/ux": "ui/ux",
    "ui/ux design": "ui/ux",
    "ui ux": "ui/ux",
    "figma": "figma",
    "git": "git",
    "github": "git",
    "gitlab": "git",
    "power bi": "power bi",
    "powerbi": "power bi",
    "tableau": "tableau",
    "pandas": "pandas",
    "numpy": "numpy",
    "tensorflow": "tensorflow",
    "pytorch": "pytorch",
    "keras": "keras",
    "opencv": "opencv",
    "linux": "linux",
    "bash": "bash",
    "shell scripting": "bash"
}

def normalize_skill(skill_str: str) -> str:
    """Normalize a skill name into a clean canonical string for fair comparison."""
    if not skill_str:
        return ""
    clean = skill_str.strip().lower()
    # Normalize multiple whitespace
    clean = re.sub(r'\s+', ' ', clean)
    return SKILL_ALIASES.get(clean, clean)

def calculate_match(user_skills: list, required_skills: list) -> dict:
    """
    Compares the student's skills with the required skills of an opportunity.
    Returns:
      - match_percentage: int (0 to 100)
      - matched_skills: list of required skill strings that student possesses
      - missing_skills: list of required skill strings that student lacks
      - match_tier: 'High Match' (>=75%), 'Moderate Match' (40-74%), 'Growth Fit' (<40%)
    """
    if not required_skills:
        return {
            "match_percentage": 100,
            "matched_skills": [],
            "missing_skills": [],
            "total_required": 0,
            "matched_count": 0,
            "missing_count": 0,
            "match_tier": "High Match"
        }

    # Normalize user skills set
    user_skill_canonical_set = {normalize_skill(s) for s in user_skills if s}
    # Also include original lowercased tokens for partial matches
    user_raw_lowers = [s.strip().lower() for s in user_skills if s]

    matched_skills = []
    missing_skills = []

    for req in required_skills:
        if not req:
            continue
        req_norm = normalize_skill(req)
        req_lower = req.strip().lower()

        # Check exact canonical alias match, exact raw lower match, or substring inclusion
        is_match = (
            req_norm in user_skill_canonical_set
            or req_lower in user_raw_lowers
            or any(req_lower == u for u in user_raw_lowers)
        )

        if is_match:
            matched_skills.append(req)
        else:
            missing_skills.append(req)

    total = len(required_skills)
    matched_count = len(matched_skills)
    match_percentage = round((matched_count / max(total, 1)) * 100)

    if match_percentage >= 75:
        match_tier = "High Match"
    elif match_percentage >= 40:
        match_tier = "Moderate Match"
    else:
        match_tier = "Growth Fit"

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_required": total,
        "matched_count": matched_count,
        "missing_count": len(missing_skills),
        "match_tier": match_tier
    }
