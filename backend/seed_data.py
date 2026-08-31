import json
from database import db_session
from models import Opportunity, UserProfile

SAMPLE_OPPORTUNITIES = [
    {
        "title": "Machine Learning Research Intern",
        "company": "Apex AI Research",
        "location": "San Francisco, CA",
        "is_remote": "Remote",
        "job_type": "Internship",
        "required_skills": ["Python", "SQL", "Machine Learning", "TensorFlow"],
        "qualification": "Pursuing B.S./M.S. in CS, Data Science, or related field",
        "description": "Collaborate with senior researchers to train and benchmark deep learning models for natural language processing and computer vision. You will write clean Python code, optimize SQL pipelines for large datasets, and contribute to production ML workflows.",
        "salary_or_stipend": "$45 - $55 / hr",
        "source": "Apex Career Hub",
        "application_link": "https://apexai.example.com/careers/ml-intern"
    },
    {
        "title": "Junior Python Backend Developer",
        "company": "CloudScale Systems",
        "location": "New York, NY",
        "is_remote": "Hybrid",
        "job_type": "Job",
        "required_skills": ["Python", "SQL", "Flask", "REST APIs", "Git"],
        "qualification": "B.S. in Computer Science or equivalent practical experience",
        "description": "Join our core backend engineering squad to build resilient RESTful microservices. You will architect SQLite/PostgreSQL schemas, design modular Flask APIs, and implement automated unit test suites.",
        "salary_or_stipend": "$85,000 - $105,000 / yr",
        "source": "CloudScale Careers",
        "application_link": "https://cloudscale.example.com/jobs/junior-python-dev"
    },
    {
        "title": "Frontend React Engineering Intern",
        "company": "TechNova Labs",
        "location": "Austin, TX",
        "is_remote": "Remote",
        "job_type": "Internship",
        "required_skills": ["React", "JavaScript", "HTML", "CSS", "Git"],
        "qualification": "Current undergraduate student in STEM discipline",
        "description": "Build high-performance, responsive web interfaces for our enterprise SaaS product. You will work closely with product designers, implement modern React hooks, and write modular CSS components.",
        "salary_or_stipend": "$35 - $45 / hr",
        "source": "TechNova Portal",
        "application_link": "https://technova.example.com/apply/react-intern"
    },
    {
        "title": "Data Science Associate",
        "company": "Insight Analytics Corp",
        "location": "Boston, MA",
        "is_remote": "Hybrid",
        "job_type": "Job",
        "required_skills": ["Python", "SQL", "Machine Learning", "Pandas", "Tableau"],
        "qualification": "Bachelor's degree in Statistics, Computer Science, or Data Analytics",
        "description": "Transform multi-gigabyte raw business datasets into actionable machine learning models and executive dashboards. You will perform exploratory data analysis, build predictive pipelines with Pandas and Scikit-Learn, and visualize insights in Tableau.",
        "salary_or_stipend": "$90,000 - $115,000 / yr",
        "source": "Insight Talent Network",
        "application_link": "https://insightanalytics.example.com/roles/data-science-assoc"
    },
    {
        "title": "Full Stack Web Developer Intern",
        "company": "NextGen Apps",
        "location": "Seattle, WA",
        "is_remote": "Hybrid",
        "job_type": "Internship",
        "required_skills": ["React", "JavaScript", "Node.js", "MongoDB", "Git"],
        "qualification": "Junior or Senior student in Computer Science or Software Engineering",
        "description": "Work across our entire web stack from frontend UI components in React to backend API routes in Node.js. Learn how to architect end-to-end features and deploy scalable full-stack applications.",
        "salary_or_stipend": "$40 - $50 / hr",
        "source": "NextGen Careers",
        "application_link": "https://nextgenapps.example.com/careers/fullstack-intern"
    },
    {
        "title": "UI/UX & Frontend Development Intern",
        "company": "PixelCraft Studios",
        "location": "San Francisco, CA",
        "is_remote": "Remote",
        "job_type": "Internship",
        "required_skills": ["Figma", "UI/UX", "HTML", "CSS", "React"],
        "qualification": "Portfolio demonstrating web design, wireframing, and basic frontend coding",
        "description": "Bridge the gap between design and frontend code. Translate high-fidelity Figma prototypes into pixel-perfect, accessible React components with clean CSS animations and micro-interactions.",
        "salary_or_stipend": "$30 - $40 / hr",
        "source": "PixelCraft Jobs",
        "application_link": "https://pixelcraft.example.com/internships/design-frontend"
    },
    {
        "title": "Junior Cloud & DevOps Engineer",
        "company": "InfraWorx Technologies",
        "location": "Denver, CO",
        "is_remote": "Remote",
        "job_type": "Job",
        "required_skills": ["Docker", "Kubernetes", "Linux", "Git", "CI/CD"],
        "qualification": "Degree in IT, Computer Engineering, or Cloud Certification",
        "description": "Maintain high-availability Kubernetes clusters, automate deployment pipelines using GitHub Actions, and assist developers in containerizing modern distributed microservices.",
        "salary_or_stipend": "$88,000 - $110,000 / yr",
        "source": "InfraWorx Portal",
        "application_link": "https://infraworx.example.com/jobs/junior-devops"
    },
    {
        "title": "AI & Prompt Engineering Intern",
        "company": "Cognition Works",
        "location": "New York, NY",
        "is_remote": "Hybrid",
        "job_type": "Internship",
        "required_skills": ["Python", "Natural Language Processing", "PyTorch", "Git"],
        "qualification": "Student interested in Large Language Models and NLP systems",
        "description": "Experiment with state-of-the-art transformer models and RAG (Retrieval-Augmented Generation) architectures. Build evaluation harnesses in Python and fine-tune open-source models.",
        "salary_or_stipend": "$42 - $52 / hr",
        "source": "Cognition Careers",
        "application_link": "https://cognitionworks.example.com/interns/ai-nlp"
    },
    {
        "title": "Cybersecurity Analyst Trainee",
        "company": "CyberShield Defense",
        "location": "Washington, DC",
        "is_remote": "On-site",
        "job_type": "Job",
        "required_skills": ["Linux", "Python", "Git", "SQL"],
        "qualification": "Degree in Cybersecurity, Information Systems, or relevant certifications (CompTIA Security+)",
        "description": "Monitor security event logs, analyze network traffic anomalies, and automate threat detection scripts using Python and Bash. Learn incident response protocols in an active Security Operations Center.",
        "salary_or_stipend": "$78,000 - $95,000 / yr",
        "source": "CyberShield Portal",
        "application_link": "https://cybershield.example.com/careers/sec-analyst"
    },
    {
        "title": "Mobile App Developer Intern (React Native)",
        "company": "AppFlow Studios",
        "location": "Chicago, IL",
        "is_remote": "Remote",
        "job_type": "Internship",
        "required_skills": ["React Native", "JavaScript", "React", "Git", "REST APIs"],
        "qualification": "Experience building iOS/Android cross-platform apps",
        "description": "Develop consumer-facing mobile features using React Native. Integrate RESTful endpoints, improve app startup performance, and deploy builds to test environments.",
        "salary_or_stipend": "$32 - $42 / hr",
        "source": "AppFlow Careers",
        "application_link": "https://appflow.example.com/jobs/react-native-intern"
    },
    {
        "title": "Junior QA Automation Engineer",
        "company": "QualiTest Solutions",
        "location": "Atlanta, GA",
        "is_remote": "Hybrid",
        "job_type": "Job",
        "required_skills": ["Python", "SQL", "Git"],
        "qualification": "B.S. in Computer Science or Software Quality Engineering",
        "description": "Design and execute automated integration and regression test suites. Write Python test scripts, validate database integrity via SQL queries, and ensure releases meet strict performance benchmarks.",
        "salary_or_stipend": "$75,000 - $90,000 / yr",
        "source": "QualiTest Portal",
        "application_link": "https://qualitest.example.com/careers/qa-engineer"
    },
    {
        "title": "Database & BI Analyst Intern",
        "company": "DataMatrix Global",
        "location": "Dallas, TX",
        "is_remote": "Remote",
        "job_type": "Internship",
        "required_skills": ["SQL", "PostgreSQL", "Power BI", "Python"],
        "qualification": "Undergraduate student in Business Analytics or Information Systems",
        "description": "Design analytical relational databases, write complex SQL aggregations, and build executive Power BI reporting dashboards for Fortune 500 client accounts.",
        "salary_or_stipend": "$28 - $36 / hr",
        "source": "DataMatrix Careers",
        "application_link": "https://datamatrix.example.com/internships/bi-analyst"
    },
    {
        "title": "Entry-Level Backend Engineer",
        "company": "Helix Core Systems",
        "location": "San Jose, CA",
        "is_remote": "Hybrid",
        "job_type": "Job",
        "required_skills": ["Python", "PostgreSQL", "Docker", "REST APIs", "Git"],
        "qualification": "Recent graduate with Computer Science or Computer Engineering degree",
        "description": "Build high-throughput data processing engines and secure APIs. You will implement caching layers, write clean database migrations, and collaborate with frontend engineers.",
        "salary_or_stipend": "$95,000 - $120,000 / yr",
        "source": "Helix Core Portal",
        "application_link": "https://helixcore.example.com/jobs/entry-backend"
    },
    {
        "title": "Computer Vision & Deep Learning Intern",
        "company": "Visionary AI Labs",
        "location": "Pittsburgh, PA",
        "is_remote": "Hybrid",
        "job_type": "Internship",
        "required_skills": ["Python", "OpenCV", "PyTorch", "Machine Learning", "Deep Learning"],
        "qualification": "Student with coursework in Image Processing and Neural Networks",
        "description": "Develop edge-deployed object detection and image segmentation pipelines. Work with OpenCV and PyTorch to preprocess video streams and benchmark inference speeds.",
        "salary_or_stipend": "$40 - $50 / hr",
        "source": "Visionary AI Portal",
        "application_link": "https://visionaryai.example.com/apply/cv-intern"
    },
    {
        "title": "Junior Frontend Web Developer",
        "company": "Aurora Digital Studio",
        "location": "Los Angeles, CA",
        "is_remote": "Remote",
        "job_type": "Job",
        "required_skills": ["TypeScript", "React", "CSS", "HTML", "Git"],
        "qualification": "B.S. in CS or interactive media design bootcamp graduate",
        "description": "Create responsive, accessible web applications using TypeScript and React. Work with UX designers to deliver sleek micro-animations and intuitive customer checkout funnels.",
        "salary_or_stipend": "$80,000 - $98,000 / yr",
        "source": "Aurora Digital Careers",
        "application_link": "https://auroradigital.example.com/jobs/junior-frontend"
    },
    {
        "title": "Product Operations & Tech Intern",
        "company": "SprintScale Tech",
        "location": "New York, NY",
        "is_remote": "Hybrid",
        "job_type": "Internship",
        "required_skills": ["SQL", "Python", "Data Analysis", "Git"],
        "qualification": "Strong analytical problem solving and communication skills",
        "description": "Work directly with Product Managers and Lead Engineers to analyze feature adoption metrics, query product telemetry in SQL, and automate operational workflows with Python scripts.",
        "salary_or_stipend": "$32 - $40 / hr",
        "source": "SprintScale Portal",
        "application_link": "https://sprintscale.example.com/interns/prod-ops"
    },
    {
        "title": "Cloud Infrastructure Intern",
        "company": "Skyward Cloud Solutions",
        "location": "Raleigh, NC",
        "is_remote": "Remote",
        "job_type": "Internship",
        "required_skills": ["Linux", "AWS", "Docker", "Python", "Bash"],
        "qualification": "Enrolled in Computer Science, Systems Engineering, or Cloud Computing",
        "description": "Assist our cloud architects in provisioning AWS infrastructure via Terraform, configuring Linux servers, and optimizing containerized workloads for cost efficiency.",
        "salary_or_stipend": "$34 - $44 / hr",
        "source": "Skyward Careers",
        "application_link": "https://skywardcloud.example.com/apply/infra-intern"
    },
    {
        "title": "Junior Software Engineer (Full Stack)",
        "company": "Vanguard Web Dynamics",
        "location": "Philadelphia, PA",
        "is_remote": "Hybrid",
        "job_type": "Job",
        "required_skills": ["React", "Python", "Flask", "SQL", "Git"],
        "qualification": "Bachelor's degree in Software Engineering or equivalent experience",
        "description": "Join an agile engineering team building modern web portals. You will build React frontends and Python Flask microservices, writing end-to-end tests and deploying code weekly.",
        "salary_or_stipend": "$85,000 - $108,000 / yr",
        "source": "Vanguard Web Portal",
        "application_link": "https://vanguardweb.example.com/careers/jr-fullstack"
    },
    {
        "title": "Site Reliability Engineering (SRE) Intern",
        "company": "ScalePulse Systems",
        "location": "San Francisco, CA",
        "is_remote": "Remote",
        "job_type": "Internship",
        "required_skills": ["Python", "Linux", "Docker", "Git"],
        "qualification": "Enrolled in CS or Computer Engineering with passion for systems reliability",
        "description": "Learn how high-scale distributed systems stay resilient. Build monitoring dashboards, investigate latency spikes, and write automation scripts to handle failover gracefully.",
        "salary_or_stipend": "$42 - $52 / hr",
        "source": "ScalePulse Careers",
        "application_link": "https://scalepulse.example.com/jobs/sre-intern"
    },
    {
        "title": "Junior Data Engineer",
        "company": "Nexus Data Streams",
        "location": "Minneapolis, MN",
        "is_remote": "Remote",
        "job_type": "Job",
        "required_skills": ["Python", "SQL", "PostgreSQL", "Docker", "Git"],
        "qualification": "B.S. in Computer Science, Data Engineering, or equivalent",
        "description": "Build reliable ETL data pipelines connecting diverse API sources to centralized data warehouses. Optimize SQL queries and ensure high data quality and schema validation.",
        "salary_or_stipend": "$88,000 - $110,000 / yr",
        "source": "Nexus Data Careers",
        "application_link": "https://nexusdata.example.com/roles/jr-data-engineer"
    },
    {
        "title": "Software Engineering Intern (Summer 2026)",
        "company": "Crestview Financial Tech",
        "location": "New York, NY",
        "is_remote": "On-site",
        "job_type": "Internship",
        "required_skills": ["Python", "SQL", "Git", "REST APIs"],
        "qualification": "Rising Senior in Computer Science, Math, or Engineering",
        "description": "10-week summer internship working with institutional trading platforms. Build data analysis tools, develop internal API endpoints, and present your project to engineering executives.",
        "salary_or_stipend": "$50 - $60 / hr",
        "source": "Crestview FinTech Portal",
        "application_link": "https://crestviewfin.example.com/internships/summer-swe"
    },
    {
        "title": "Junior Web Application Developer",
        "company": "SparkByte Technologies",
        "location": "Austin, TX",
        "is_remote": "Hybrid",
        "job_type": "Job",
        "required_skills": ["JavaScript", "React", "HTML", "CSS", "SQL"],
        "qualification": "B.S. in Computer Science or self-taught developer with strong portfolio",
        "description": "Develop intuitive customer experiences for our e-commerce platform. Implement responsive styling, manage state using modern React patterns, and integrate with backend payment gateways.",
        "salary_or_stipend": "$80,000 - $96,000 / yr",
        "source": "SparkByte Portal",
        "application_link": "https://sparkbyte.example.com/careers/jr-web-dev"
    }
]

DEFAULT_PROFILE = {
    "name": "Alex Chen",
    "email": "alex.chen@university.edu",
    "education": "B.S. in Computer Science (Senior)",
    "university": "State University of Technology",
    "skills": ["Python", "SQL", "Machine Learning", "React", "Git"],
    "area_of_interest": "Software Engineering & Data Science",
    "location": "New York, NY",
    "experience": "1 Year (Academic Projects & Summer Internship)",
    "preference": "Both",
    "bio": "Motivated senior computer science student with hands-on project experience in Python web development, SQL data pipelines, and modern React interfaces. Seeking summer 2026 internships and entry-level positions."
}

def seed_database():
    """Populates initial profile and sample opportunities if not already present."""
    # Ensure profile exists
    profile = db_session.query(UserProfile).first()
    if not profile:
        profile = UserProfile(
            name=DEFAULT_PROFILE["name"],
            email=DEFAULT_PROFILE["email"],
            education=DEFAULT_PROFILE["education"],
            university=DEFAULT_PROFILE["university"],
            skills=json.dumps(DEFAULT_PROFILE["skills"]),
            area_of_interest=DEFAULT_PROFILE["area_of_interest"],
            location=DEFAULT_PROFILE["location"],
            experience=DEFAULT_PROFILE["experience"],
            preference=DEFAULT_PROFILE["preference"],
            bio=DEFAULT_PROFILE["bio"]
        )
        db_session.add(profile)
        db_session.commit()

    # Seed opportunities if table is empty
    opp_count = db_session.query(Opportunity).count()
    if opp_count == 0:
        for item in SAMPLE_OPPORTUNITIES:
            opp = Opportunity(
                title=item["title"],
                company=item["company"],
                location=item["location"],
                is_remote=item.get("is_remote", "Hybrid"),
                job_type=item["job_type"],
                required_skills=json.dumps(item["required_skills"]),
                qualification=item["qualification"],
                description=item["description"],
                salary_or_stipend=item.get("salary_or_stipend"),
                source=item.get("source", "Direct Portal"),
                application_link=item["application_link"]
            )
            db_session.add(opp)
        db_session.commit()
