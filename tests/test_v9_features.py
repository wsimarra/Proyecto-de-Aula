from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_students_include_group_definitive_and_followups_unavailable():
    r = client.get("/api/students")
    assert r.status_code == 200
    data = r.json()
    assert len(data["rows"]) == 726
    row = data["rows"][0]
    assert "definitive" in row and "followup2" in row and "followup3" in row
    assert row["followup2"] is None and row["followup3"] is None
    assert row["definitive"] == row["group_final"]

def test_teachers_expose_note_status():
    r = client.get("/api/teachers")
    assert r.status_code == 200
    rows = r.json()["rows"]
    assert len(rows) == 77
    assert all("graded_assignments" in row and "pending_assignments" in row and "status" in row for row in rows)

def test_student_excel_export():
    r = client.get("/api/export/students.xlsx?search=JUAN")
    assert r.status_code == 200
    assert "spreadsheetml" in r.headers.get("content-type", "")
    assert r.content[:2] == b"PK"
