# Smart Internship & Job Finder (Phase 1 MVP)

A full-stack web application that empowers students to manage their profile and skills, explore curated internships and jobs, and receive real-time skill-matching scores and personalized recommendations.

---

## Key Features

1. **User Profile Module**:
   - Save and update student name, education, university, location, experience level, area of interest, opportunity preferences (Internships, Jobs, or Both), and bio.
   - Interactive skill management: add custom skills with auto-tagging, 1-click add from in-demand suggestions, and skill removal.
   - Instant SQLite database persistence.

2. **Opportunity Collection Module**:
   - Pre-seeded with 22 rich, realistic opportunities across Web Development, Data Science, AI/ML, Cloud/DevOps, UI/UX, Cybersecurity, and QA.
   - Comprehensive opportunity schema: Title, Company, Location, Remote/Hybrid status, Job Type (Internship vs Job), Required Skills array, Qualification, Description, Salary/Stipend, Source, and Direct Application Link.
   - Modular architecture ready for future Phase 2 automated scrapers / external job APIs.

3. **Opportunity Search & Discovery Module**:
   - Real-time search across role titles, company names, descriptions, and required skills.
   - Filter by Job Type (Internships Only, Full-Time Jobs Only).
   - Filter by Location (Remote, Hybrid, On-site, City).
   - Filter by Minimum Match Compatibility (e.g. High Match >= 75%).
   - Sort by Highest Match %, Newly Added, Role Title, or Company Name.
   - Modal and dedicated page views for deep opportunity analysis with direct application links.

4. **Basic Matching Engine**:
   - Intelligent skill matching with normalized canonical aliases (e.g., `React.js` ↔ `React`, `py` ↔ `Python`, `NodeJS` ↔ `Node.js`, `ML` ↔ `Machine Learning`).
   - Computes exact match percentages: $\frac{\text{Matched Skills}}{\text{Total Required Skills}} \times 100\%$.
   - Clearly separates **Matched Skills** (green checkmark pills) from **Missing Skills** (dashed amber pills).
   - Click any missing skill pill on any opportunity to instantly add it to your profile and boost your match scores!
   - Dedicated **Recommended for You** ranking and **Skill Gap Insights** banner.

5. **5 Complete Views**:
   - **Dashboard**: Student overview, 4 metric cards, profile snapshot, and top recommended roles.
   - **Profile**: Full student profile editor with interactive skill tags and live match impact indicators.
   - **Opportunities**: Complete browsable catalog with search, multi-filters, and details modal.
   - **Opportunity Details**: In-depth view featuring skill breakdown, qualifications, compensation, and direct apply link.
   - **Recommended Opportunities**: Top-ranked recommendations with skill gap analysis.

---

## Tech Stack

- **Frontend**: React 18, Vite, Vanilla CSS Design System with Glassmorphism and Lucide Icons.
- **Backend**: Python 3.13, Flask 3.0, Flask-CORS, SQLAlchemy 2.0.
- **Database**: SQLite (`smart_finder.db`).

---

## Project Structure

```
CareerPi/
├── backend/
│   ├── app.py                 # Flask app factory, CORS & blueprint registration
│   ├── config.py              # Configuration & SQLite URI
│   ├── database.py            # SQLAlchemy engine & session setup
│   ├── models.py              # UserProfile & Opportunity models
│   ├── seed_data.py           # 22 curated sample opportunities & default profile
│   ├── services/
│   │   ├── matcher.py         # Normalized skill comparison & match calculator
│   │   ├── profile_service.py # Profile persistence & CRUD
│   │   └── opportunity_service.py # Search, filtering, recommendations & stats
│   ├── routes/
│   │   ├── profile_routes.py  # /api/profile REST endpoints
│   │   └── opportunity_routes.py # /api/opportunities & /api/stats REST endpoints
│   ├── requirements.txt       # Backend dependencies
│   └── run.py                 # Server startup entrypoint
│
├── frontend/
│   ├── index.html             # Google fonts & meta configuration
│   ├── vite.config.js         # Vite proxy configuration to Flask API
│   ├── package.json           # React dependencies & scripts
│   └── src/
│       ├── main.jsx           # App mounting
│       ├── App.jsx            # Routing & layout
│       ├── index.css          # Glassmorphic responsive design system
│       ├── api/
│       │   └── client.js      # REST API client
│       ├── context/
│       │   └── AppContext.jsx # Global profile, stats, navigation & toast state
│       ├── components/
│       │   ├── Navbar.jsx
│       │   ├── StatsCard.jsx
│       │   ├── MatchBadge.jsx
│       │   ├── SkillsBreakdown.jsx
│       │   ├── OpportunityCard.jsx
│       │   ├── OpportunityModal.jsx
│       │   ├── FilterBar.jsx
│       │   └── Toast.jsx
│       └── pages/
│           ├── Dashboard.jsx
│           ├── Profile.jsx
│           ├── Opportunities.jsx
│           ├── OpportunityDetails.jsx
│           └── Recommended.jsx
│
├── test_suite.py              # 10-step end-to-end automated verification script
└── README.md                  # Project documentation
```

---

## Instructions to Run Locally

### 1. Start the Flask Backend

In a terminal window:

```bash
cd backend
pip install -r requirements.txt
python run.py
```

The backend starts at `http://127.0.0.1:5000`. On first launch, it will automatically initialize the SQLite database and seed 22 realistic job and internship listings.

### 2. Start the React Frontend

In a second terminal window:

```bash
cd frontend
npm install
npm run dev
```

The frontend development server starts at `http://localhost:3000`.

### 3. Run Automated Tests

To run the complete 10-step end-to-end test suite verifying all REST APIs and matching logic:

```bash
python test_suite.py
```

---

## REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Backend health check |
| `GET` | `/api/profile` | Retrieve active student profile |
| `PUT` | `/api/profile` | Update profile information and skills |
| `GET` | `/api/opportunities` | List opportunities with search (`?q=`), type (`?job_type=`), location (`?location=`), min match (`?min_match=`), and sort (`?sort_by=`) |
| `GET` | `/api/opportunities/<id>` | Retrieve full opportunity details with matched/missing skills |
| `GET` | `/api/opportunities/recommended` | Retrieve top matched opportunities sorted descending |
| `GET` | `/api/stats` | Dashboard statistics (counts, top match score, avg match) |
| `POST` | `/api/opportunities` | Add new opportunity (for Phase 2 API integrations) |
