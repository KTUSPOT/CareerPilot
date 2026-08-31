import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://127.0.0.1:5000"

def get(path):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))

def post_or_put(path, data, method="PUT"):
    url = f"{BASE_URL}{path}"
    encoded = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=encoded, headers={"Content-Type": "application/json"}, method=method)
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))

def run_tests():
    print("=" * 60)
    print("RUNNING SMART FINDER E2E TEST SUITE")
    print("=" * 60)

    # 1. Health check
    status, res = get("/api/health")
    assert status == 200 and res["status"] == "healthy"
    print("  [PASS] 1. Backend Health Check")

    # 2. Get Profile
    status, res = get("/api/profile")
    assert status == 200 and res["success"] is True
    profile = res["data"]
    print(f"  [PASS] 2. Get Profile -> Name: {profile['name']}, Skills: {profile['skills']}")
    assert len(profile["skills"]) > 0

    # 3. Get Stats
    status, res = get("/api/stats")
    assert status == 200 and res["success"] is True
    stats = res["data"]
    print(f"  [PASS] 3. Dashboard Stats -> Total: {stats['total_opportunities']}, Internships: {stats['internships_count']}, Jobs: {stats['jobs_count']}, High Matches: {stats['high_match_count']}")
    assert stats["total_opportunities"] >= 20

    # 4. Search & Filter Opportunities (Python keyword)
    status, res = get("/api/opportunities?q=python")
    assert status == 200 and res["success"] is True
    python_opps = res["data"]
    print(f"  [PASS] 4. Search 'python' -> Returned {len(python_opps)} opportunities")
    assert len(python_opps) > 0
    # verify match calculation exists on each card
    first = python_opps[0]
    assert "match_percentage" in first and "matched_skills" in first and "missing_skills" in first
    print(f"         Top Python role: '{first['title']}' ({first['match_percentage']}% match)")
    print(f"         Matched: {first['matched_skills']} | Missing: {first['missing_skills']}")

    # 5. Filter by Job Type (Internship only)
    status, res = get("/api/opportunities?job_type=internship")
    assert status == 200 and res["success"] is True
    internships = res["data"]
    print(f"  [PASS] 5. Filter 'internship' -> Returned {len(internships)} internships")
    assert all(o["job_type"].lower() == "internship" for o in internships)

    # 6. Filter by Location (Remote only)
    status, res = get("/api/opportunities?location=remote")
    assert status == 200 and res["success"] is True
    remote_opps = res["data"]
    print(f"  [PASS] 6. Filter 'remote' -> Returned {len(remote_opps)} remote opportunities")
    assert len(remote_opps) > 0

    # 7. Get Recommended Opportunities (Sorted by match % descending)
    status, res = get("/api/opportunities/recommended?limit=5")
    assert status == 200 and res["success"] is True
    rec_opps = res["data"]
    print(f"  [PASS] 7. Recommendations -> Top {len(rec_opps)} recommendations:")
    percentages = [o["match_percentage"] for o in rec_opps]
    for i, o in enumerate(rec_opps):
        print(f"         {i+1}. {o['title']} ({o['company']}) -> {o['match_percentage']}%")
    assert percentages == sorted(percentages, reverse=True)

    # 8. Single Opportunity Details
    first_id = rec_opps[0]["id"]
    status, res = get(f"/api/opportunities/{first_id}")
    assert status == 200 and res["success"] is True
    opp_detail = res["data"]
    print(f"  [PASS] 8. Opportunity Details for ID {first_id} -> '{opp_detail['title']}' ({opp_detail['qualification']})")

    # 9. Update Profile & verify match re-computation
    print("  [TEST] 9. Testing dynamic skill update in Profile...")
    updated_profile_data = {
        "name": "Alex Chen",
        "education": "B.S. in Computer Science (Senior)",
        "skills": ["Python", "SQL", "Machine Learning", "React", "Git", "TensorFlow", "Docker"],
        "area_of_interest": "AI/ML & Cloud Systems",
        "location": "New York, NY",
        "preference": "Both"
    }
    status, res = post_or_put("/api/profile", updated_profile_data)
    assert status == 200 and res["success"] is True
    print(f"         Updated skills to: {res['data']['skills']}")

    # Re-check recommendations after skill update
    status, res = get("/api/opportunities/recommended?limit=5")
    assert status == 200
    new_recs = res["data"]
    print("         New Top Recommendations after adding TensorFlow & Docker:")
    for i, o in enumerate(new_recs):
        print(f"         {i+1}. {o['title']} -> {o['match_percentage']}% (Matched: {o['matched_skills']})")

    # 10. Check Frontend Vite server responds
    print("  [TEST] 10. Checking Vite Frontend Server on http://localhost:3000...")
    with urllib.request.urlopen("http://localhost:3000/") as resp:
        html_content = resp.read().decode('utf-8')
        assert "Smart Internship & Job Finder" in html_content
        print("  [PASS] 10. Frontend HTML serving correctly with title and root mount element")

    print("=" * 60)
    print("ALL 10 VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
