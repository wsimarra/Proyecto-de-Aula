import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from app.main import app, MODEL

client = TestClient(app)

def test_both_periods_are_available():
    r = client.get("/api/meta")
    assert r.status_code == 200
    assert r.json()["periods"] == ["2026-1", "2026-2"]

def test_2026_1_kpis_remain_unchanged():
    data = client.get("/api/dashboard?period=2026-1").json()
    assert data["kpis"]["projects"] == 154
    assert data["kpis"]["students"] == 726
    assert data["kpis"]["teachers"] == 77

def test_2026_2_data_is_loaded_and_filterable():
    data = client.get("/api/dashboard?period=2026-2").json()
    assert data["kpis"]["cohorts"] == 31
    assert data["kpis"]["projects"] == 166
    assert data["kpis"]["programs"] == 2
    assert data["kpis"]["missing_projects"] >= 1

def test_every_excel_source_exists():
    from pathlib import Path
    base = Path(__file__).resolve().parents[1] / "data" / "excel"
    for f in MODEL["files"]:
        stored = f.get("stored_filename") or f["filename"]
        assert (base / stored).exists(), stored
