from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_students_include_group_definitive_and_followups_unavailable():
    r = client.get("/api/students?period=2026-1")
    assert r.status_code == 200
    data = r.json()
    assert len(data["rows"]) == 726
    row = data["rows"][0]
    assert "definitive" in row and "followup2" in row and "followup3" in row
    assert row["followup2"] == 4.2 and row["followup3"] == 4.6
    assert row["definitive"] == 4.4

def test_teachers_expose_note_status():
    r = client.get("/api/teachers?period=2026-1")
    assert r.status_code == 200
    rows = r.json()["rows"]
    assert len(rows) == 77
    assert all("graded_assignments" in row and "pending_assignments" in row and "status" in row for row in rows)

def test_student_excel_export():
    r = client.get("/api/export/students.xlsx?search=JUAN")
    assert r.status_code == 200
    assert "spreadsheetml" in r.headers.get("content-type", "")
    assert r.content[:2] == b"PK"
