
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json, re, unicodedata, csv, io
from collections import defaultdict

BASE=Path(__file__).resolve().parents[1]
PDF_DIR=BASE/"data"/"pdfs"
PDF_DIR.mkdir(parents=True, exist_ok=True)
MODEL=json.loads((BASE/"data"/"model.json").read_text(encoding="utf-8"))
DOCS_PATH=BASE/"data"/"project_documents.json"
PROJECT_DOCUMENTS=json.loads(DOCS_PATH.read_text(encoding="utf-8")) if DOCS_PATH.exists() else {}
app=FastAPI(title="Proyectos de Aula V4 – Destacados y PDF")

def norm(s):
    if s is None: return ""
    s=unicodedata.normalize("NFKD",str(s).strip().upper()).encode("ascii","ignore").decode("ascii")
    return re.sub(r"\s+"," ",s)

def match(v, wanted):
    return not wanted or str(v)==str(wanted)

def selected(filters):
    # Cohort-level filters
    cs=[c for c in MODEL["cohorts"]
        if match(c["period"],filters.get("period"))
        and match(c["program"],filters.get("program"))
        and match(c["semester"],filters.get("semester"))
        and match(c["section"],filters.get("section"))]
    cids={c["id"] for c in cs}
    projects=[p for p in MODEL["projects"] if p["cohort_id"] in cids]
    # group filter
    if filters.get("group"):
        projects=[p for p in projects if p["group"]==filters["group"]]
        cids={p["cohort_id"] for p in projects}
        cs=[c for c in cs if c["id"] in cids]
    # subject/docente filters narrow cohorts/people but don't remove a project if the cohort matches;
    # student/teacher pages use the contextual assignment relation.
    assignments=[a for a in MODEL["assignments"] if a["cohort_id"] in cids]
    if filters.get("teacher"):
        tids={t["id"] for t in MODEL["teachers"] if norm(t["name"])==norm(filters["teacher"])}
        assignments=[a for a in assignments if a["teacher_id"] in tids]
        cids={a["cohort_id"] for a in assignments}
        cs=[c for c in cs if c["id"] in cids]
        projects=[p for p in projects if p["cohort_id"] in cids]
    if filters.get("subject"):
        sids={s["id"] for s in MODEL["subjects"] if norm(s["name"])==norm(filters["subject"])}
        assignments=[a for a in assignments if a["subject_id"] in sids]
        cids={a["cohort_id"] for a in assignments}
        cs=[c for c in cs if c["id"] in cids]
        projects=[p for p in projects if p["cohort_id"] in cids]
    return cs,projects,assignments

def names_by_ids(table, ids):
    m={x["id"]:x["name"] for x in table}
    return [m[i] for i in ids if i in m]

def contextual_options(filters):
    # For each dropdown, calculate values available with the other filters.
    fields=["period","program","semester","section","group","teacher","subject"]
    out={}
    for field in fields:
        f={k:v for k,v in filters.items() if k!=field and v not in ("",None)}
        cs,projects,assignments=selected(f)
        cids={c["id"] for c in cs}
        if field=="period":
            vals=sorted({c["period"] for c in cs})
        elif field=="program":
            vals=sorted({c["program"] for c in cs})
        elif field=="semester":
            vals=sorted({c["semester"] for c in cs})
        elif field=="section":
            vals=sorted({c["section"] for c in cs},key=lambda x:int(x) if str(x).isdigit() else str(x))
        elif field=="group":
            vals=sorted({p["group"] for p in projects})
        elif field=="teacher":
            vals=names_by_ids(MODEL["teachers"],{a["teacher_id"] for a in assignments})
            vals=sorted(set(vals),key=norm)
        else:
            vals=names_by_ids(MODEL["subjects"],{a["subject_id"] for a in assignments})
            vals=sorted(set(vals),key=norm)
        out[field]=vals
    return out

def _project_members(project):
    """Return unique student names belonging to the project group."""
    ids={e["student_id"] for e in MODEL["enrollments"]
         if e["cohort_id"]==project["cohort_id"] and e["group_code"]==project["group"]}
    return sorted(names_by_ids(MODEL["students"],ids), key=norm)

def highlights(filters):
    """Top 5 global projects and highlighted project(s) per semester in the selected context."""
    cs,projects,assignments=selected(filters)
    cmap={c["id"]:c for c in cs}
    documents=PROJECT_DOCUMENTS
    enriched=[]
    for p in projects:
        c=cmap.get(p["cohort_id"])
        if not c or p.get("final_grade") is None:
            continue
        key=f'{p["cohort_id"]}:{p["group"]}'
        enriched.append({
            **p,
            "program":c.get("program"),"period":c.get("period"),
            "semester":c.get("semester"),"section":c.get("section"),
            "members":_project_members(p),
            "pdf_url":documents.get(key,"")
        })
    ranked=sorted(enriched,key=lambda x:(-x["final_grade"],x["semester"],str(x["section"]),x["group"],norm(x["title"])))
    top5=ranked[:5]
    by_semester=[]
    for sem in sorted({x["semester"] for x in enriched}):
        items=[x for x in enriched if x["semester"]==sem]
        top=max(x["final_grade"] for x in items)
        # Preserve ties rather than arbitrarily choosing one project.
        by_semester.extend([x for x in items if abs(x["final_grade"]-top)<1e-9])
    by_semester.sort(key=lambda x:(x["semester"],-x["final_grade"],str(x["section"]),x["group"]))
    return {
        "criteria":"Mayor promedio final del grupo según TERCER CORTE de DEFINITIVAS.",
        "top5":top5,
        "by_semester":by_semester,
        "total_ranked":len(enriched)
    }

def dashboard(filters):
    cs,projects,assignments=selected(filters)
    cids={c["id"] for c in cs}
    # assignments determine teacher count; enrollment determines student count
    es=[e for e in MODEL["enrollments"] if e["cohort_id"] in cids]
    students=sorted({e["student_id"] for e in es})
    teachers=sorted({a["teacher_id"] for a in assignments})
    grades=[p["final_grade"] for p in projects if p["final_grade"] is not None]
    project_with_grade=sum(p["final_grade"] is not None for p in projects)
    # subject averages
    sids={a["subject_id"] for a in assignments}
    g=[x for x in MODEL["grades"] if x["cohort_id"] in cids and x["subject_id"] in sids]
    bysub=defaultdict(list)
    for x in g: bysub[x["subject_id"]].append(x["grade"])
    smap={s["id"]:s["name"] for s in MODEL["subjects"]}
    subject_avg=[{"name":smap[sid],"avg":round(sum(vals)/len(vals),2),"n":len(vals)}
                 for sid,vals in bysub.items() if vals]
    subject_avg.sort(key=lambda x:x["avg"],reverse=True)
    # semester summary
    bysem=[]
    for sem in sorted({c["semester"] for c in cs}):
        ps=[p for p in projects if next((c for c in cs if c["id"]==p["cohort_id"]),{}).get("semester")==sem]
        vals=[p["final_grade"] for p in ps if p["final_grade"] is not None]
        bysem.append({"semester":sem,"projects":len(ps),"avg":round(sum(vals)/len(vals),2) if vals else None})
    # highlights with ties
    highlights=[]
    for sem in sorted({x["semester"] for x in bysem}):
        ps=[p for p in projects if next((c for c in cs if c["id"]==p["cohort_id"]),{}).get("semester")==sem and p["final_grade"] is not None]
        if ps:
            top=max(p["final_grade"] for p in ps)
            for p in ps:
                if abs(p["final_grade"]-top)<1e-9:
                    c=next(c for c in cs if c["id"]==p["cohort_id"])
                    highlights.append({**p,"section":c["section"],"program":c["program"]})
    cmap={c["id"]:c for c in cs}
    enriched=[]
    for p in projects:
        c=cmap.get(p["cohort_id"],{})
        enriched.append({**p,"program":c.get("program"),"period":c.get("period"),"semester":c.get("semester"),"section":c.get("section")})
    return {
      "filters":filters,"options":contextual_options(filters),
      "kpis":{
        "projects":len(projects),"students":len(students),"teachers":len(teachers),
        "programs":len({c["program"] for c in cs}),"cohorts":len(cs),
        "avg_final":round(sum(grades)/len(grades),2) if grades else None,
        "coverage":round(project_with_grade/len(projects)*100,1) if projects else 0,
        "graded_projects":project_with_grade,"missing_projects":len(projects)-project_with_grade
      },
      "by_semester":bysem,"highlights":highlights,"subject_avg":subject_avg,
      "projects":enriched,
      "teacher_names":names_by_ids(MODEL["teachers"],teachers)
    }

@app.get("/")
def home(): return FileResponse(BASE/"static"/"index.html")

@app.get("/api/meta")
def meta():
    return {"files":len(MODEL["files"]),"cohorts":len(MODEL["cohorts"]),
            "students":len(MODEL["students"]),"teachers":len(MODEL["teachers"]),
            "subjects":len(MODEL["subjects"]),"projects":len(MODEL["projects"]),
            "periods":sorted({c["period"] for c in MODEL["cohorts"]}),
            "programs":sorted({c["program"] for c in MODEL["cohorts"]})}

@app.get("/api/options")
def options(period="",program="",semester="",section="",group="",teacher="",subject=""):
    return contextual_options({"period":period,"program":program,"semester":semester,"section":section,"group":group,"teacher":teacher,"subject":subject})

@app.get("/api/dashboard")
def api_dashboard(period="",program="",semester="",section="",group="",teacher="",subject=""):
    return dashboard({"period":period,"program":program,"semester":semester,"section":section,"group":group,"teacher":teacher,"subject":subject})

@app.get("/api/students")
def students(period="",program="",semester="",section="",group="",teacher="",subject=""):
    f={"period":period,"program":program,"semester":semester,"section":section,"group":group,"teacher":teacher,"subject":subject}
    cs,projects,assignments=selected(f); cids={c["id"] for c in cs}
    pids={(p["cohort_id"],p["group"]) for p in projects}
    es=[e for e in MODEL["enrollments"] if e["cohort_id"] in cids and (not f.get("group") or e["group_code"]==f.get("group"))]
    smap={s["id"]:s["name"] for s in MODEL["students"]}; cmap={c["id"]:c for c in MODEL["cohorts"]}
    # final grade per student from grades in DEFINITIVAS third-cut aggregate isn't stored; use project-group final grade as group context.
    pmap={(p["cohort_id"],p["group"]):p for p in projects}
    rows=[]
    for e in es:
        c=cmap[e["cohort_id"]]; p=pmap.get((e["cohort_id"],e["group_code"]))
        rows.append({"student":smap[e["student_id"]],"semester":c["semester"],"section":c["section"],
                     "group":e["group_code"],"project":p["title"] if p else "—",
                     "group_final":round(p["final_grade"],2) if p and p["final_grade"] is not None else None})
    # deduplicate student+cohort+group
    uniq={(r["student"],r["semester"],r["section"],r["group"]):r for r in rows}
    return {"rows":sorted(uniq.values(),key=lambda r:(r["semester"],r["section"],r["group"],norm(r["student"])))}

@app.get("/api/teachers")
def teachers(period="",program="",semester="",section="",group="",teacher="",subject=""):
    f={"period":period,"program":program,"semester":semester,"section":section,"group":group,"teacher":teacher,"subject":subject}
    cs,projects,assignments=selected(f); cids={c["id"] for c in cs}
    cmap={c["id"]:c for c in cs}; tmap={t["id"]:t["name"] for t in MODEL["teachers"]}; smap={s["id"]:s["name"] for s in MODEL["subjects"]}
    rows=[]
    for tid in sorted({a["teacher_id"] for a in assignments}):
        aa=[a for a in assignments if a["teacher_id"]==tid]
        rows.append({"teacher":tmap[tid],"subjects":sorted({smap[a["subject_id"]] for a in aa},key=norm),
                     "cohorts":len({a["cohort_id"] for a in aa}),
                     "projects":len([p for p in projects if p["cohort_id"] in {a["cohort_id"] for a in aa}]),
                     "groups":len({(p["cohort_id"],p["group"]) for p in projects if p["cohort_id"] in {a["cohort_id"] for a in aa}})})
    return {"rows":sorted(rows,key=lambda r:norm(r["teacher"]))}

@app.get("/api/highlights")
def api_highlights(period="",program="",semester="",section="",group="",teacher="",subject=""):
    return highlights({"period":period,"program":program,"semester":semester,"section":section,"group":group,"teacher":teacher,"subject":subject})

@app.post("/api/highlights/{cohort_id}/{group}/pdf")
async def upload_highlight_pdf(cohort_id: str, group: str, file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF.")
    safe_group=re.sub(r"[^A-Za-z0-9_-]+","_",str(group)).strip("_") or "grupo"
    safe_cohort=re.sub(r"[^A-Za-z0-9_-]+","_",str(cohort_id)).strip("_") or "cohorte"
    filename=f"{safe_cohort}_{safe_group}.pdf"
    out=PDF_DIR/filename
    data=await file.read()
    if len(data)>20*1024*1024:
        raise HTTPException(status_code=400, detail="El PDF supera el límite de 20 MB.")
    out.write_bytes(data)
    key=f"{cohort_id}:{group}"
    PROJECT_DOCUMENTS[key]=f"/pdfs/{filename}"
    DOCS_PATH.write_text(json.dumps(PROJECT_DOCUMENTS,ensure_ascii=False,indent=2),encoding="utf-8")
    return {"ok":True,"pdf_url":PROJECT_DOCUMENTS[key],"filename":filename}

@app.get("/api/audit")
def audit():
    mism=[]
    for f in MODEL["files"]:
        # only mismatch captured by ETL in model build if present
        pass
    return {"files":MODEL["files"],"model":{
      "period":"2026-1 · Primer periodo","source":"Archivos Excel locales",
      "note_rule":"Nota final del grupo = promedio de la columna TERCER CORTE de DEFINITIVAS (E), cuando existe.",
      "title_rule":"Título del proyecto = sección TITULOS DE LOS PROYECTOS DE AULA de LIDER, filas 29–40, por posición de grupo.",
      "students_rule":"Estudiante = nombre normalizado; no se usa como identificador institucional definitivo si el archivo no trae ID único.",
      "project_highlight":"Mayor promedio final de grupo por semestre; empates se conservan.",
      "section_rule":"La sección operativa se toma del nombre del archivo (SEM-XX-SEC-YY). Se audita contra LIDER!H2.",
      "onedrive":"Preparado para sustituir la fuente local por Microsoft Graph/SharePoint."
    }}

@app.get("/api/export/projects.csv")
def export_projects(period="",program="",semester="",section="",group="",teacher="",subject=""):
    d=dashboard({"period":period,"program":program,"semester":semester,"section":section,"group":group,"teacher":teacher,"subject":subject})
    out=io.StringIO(); w=csv.writer(out); w.writerow(["Programa","Periodo","Semestre","Seccion","Grupo","Proyecto","Estudiantes","Nota final grupo","Estado"])
    cmap={c["id"]:c for c in MODEL["cohorts"]}
    for p in d["projects"]:
        c=cmap[p["cohort_id"]]; w.writerow([c["program"],c["period"],c["semester"],c["section"],p["group"],p["title"],p["student_count"],p["final_grade"] if p["final_grade"] is not None else "", "CON NOTA" if p["final_grade"] is not None else "SIN NOTA"])
    return Response(out.getvalue(),media_type="text/csv",headers={"Content-Disposition":"attachment; filename=proyectos_aula.csv"})

app.mount("/static",StaticFiles(directory=BASE/"static"),name="static")
app.mount("/pdfs",StaticFiles(directory=PDF_DIR),name="pdfs")
