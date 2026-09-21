
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
app=FastAPI(title="Proyectos de Aula V5 – Lógica, Auditoría y Destacados")

def norm(s):
    if s is None: return ""
    s=unicodedata.normalize("NFKD",str(s).strip().upper()).encode("ascii","ignore").decode("ascii")
    return re.sub(r"\s+"," ",s)

def match(v, wanted):
    return not wanted or str(v)==str(wanted)

def _is_generic_project_title(title):
    """True when the title is only a placeholder such as Proyecto 7 or GRUPO#7."""
    t=norm(title)
    return bool(re.fullmatch(r"(?:PROYECTO\s*\d+|GRUPO\s*#?\s*\d+)", t))

def _project_exclusion_reason(project):
    group=norm(project.get("group"))
    if not group or group in {"0", "G0", "GRUPO 0", "GRUPO#0"}:
        return "Grupo 0 (sin proyecto)"
    grade=project.get("final_grade")
    try:
        if grade is not None and float(grade) > 0:
            return ""
    except (TypeError, ValueError):
        pass
    title=str(project.get("title") or "").strip()
    if not title:
        return "Sin título de proyecto"
    if _is_generic_project_title(title):
        return "Título genérico (sin proyecto documentado)"
    return ""

def _is_valid_project(project):
    """Aplica la regla institucional de identificación de proyectos."""
    return _project_exclusion_reason(project)==""

VALID_PROJECTS=[p for p in MODEL["projects"] if _is_valid_project(p)]
INVALID_PROJECTS=[p for p in MODEL["projects"] if not _is_valid_project(p)]
COLLECTIVE_LEADERS=MODEL.get("collective_leaders",[])


def selected(filters):
    # Cohort-level filters
    cs=[c for c in MODEL["cohorts"]
        if match(c["period"],filters.get("period"))
        and match(c["program"],filters.get("program"))
        and match(c["semester"],filters.get("semester"))
        and match(c["section"],filters.get("section"))]
    cids={c["id"] for c in cs}
    projects=[p for p in VALID_PROJECTS if p["cohort_id"] in cids]
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
            "subjects":len(MODEL["subjects"]),"projects":len(VALID_PROJECTS),
            "periods":sorted({c["period"] for c in MODEL["cohorts"]}),
            "programs":sorted({c["program"] for c in MODEL["cohorts"]}),
            "collective_leaders":len(COLLECTIVE_LEADERS),
            "unique_collective_leaders":len({r["leader_name"] for r in COLLECTIVE_LEADERS})}

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
    try:
        cid=int(cohort_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Cohorte no válida.")
    project=next((p for p in VALID_PROJECTS if p["cohort_id"]==cid and str(p["group"])==str(group)),None)
    if project is None:
        raise HTTPException(status_code=404, detail="El grupo indicado no corresponde a un proyecto válido.")
    data=await file.read()
    if len(data)>20*1024*1024:
        raise HTTPException(status_code=400, detail="El PDF supera el límite de 20 MB.")
    if not data.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="El archivo no contiene una firma PDF válida.")
    out.write_bytes(data)
    key=f"{cohort_id}:{group}"
    PROJECT_DOCUMENTS[key]=f"/pdfs/{filename}"
    DOCS_PATH.write_text(json.dumps(PROJECT_DOCUMENTS,ensure_ascii=False,indent=2),encoding="utf-8")
    return {"ok":True,"pdf_url":PROJECT_DOCUMENTS[key],"filename":filename}

def _leader_filtered_records(period="", program="", semester="", section="", leader="", subject=""):
    rows=COLLECTIVE_LEADERS[:]
    rows=[r for r in rows if match(r.get("period"),period) and match(r.get("program"),program)
          and match(r.get("semester"),semester) and match(r.get("section"),section)
          and (not leader or norm(r.get("leader_name"))==norm(leader))
          and (not subject or norm(r.get("leader_subject"))==norm(subject))]
    return rows

def _leader_options(period="", program="", semester="", section="", leader="", subject=""):
    fields=["period","program","semester","section","leader","subject"]
    base={"period":period,"program":program,"semester":semester,"section":section,"leader":leader,"subject":subject}
    out={}
    for field in fields:
        kwargs={k:v for k,v in base.items() if k!=field}
        rows=_leader_filtered_records(**kwargs)
        if field=="period": vals=sorted({r["period"] for r in rows})
        elif field=="program": vals=sorted({r["program"] for r in rows})
        elif field=="semester": vals=sorted({r["semester"] for r in rows})
        elif field=="section": vals=sorted({r["section"] for r in rows},key=lambda x:int(x) if str(x).isdigit() else str(x))
        elif field=="leader": vals=sorted({r["leader_name"] for r in rows},key=norm)
        else: vals=sorted({r["leader_subject"] for r in rows},key=norm)
        out[field]=vals
    return out

def collective_leaders(period="", program="", semester="", section="", leader="", subject=""):
    rows=_leader_filtered_records(period,program,semester,section,leader,subject)
    p_by_c=defaultdict(list)
    for p in VALID_PROJECTS: p_by_c[p["cohort_id"]].append(p)
    e_by_c=defaultdict(set)
    for e in MODEL["enrollments"]:
        e_by_c[e["cohort_id"]].add(e["student_id"])
    result=[]
    for r in rows:
        result.append({**r,"project_count":len(p_by_c.get(r["cohort_id"],[])),"student_count":len(e_by_c.get(r["cohort_id"],set()))})
    result.sort(key=lambda x:(x["semester"],int(x["section"]) if str(x["section"]).isdigit() else str(x["section"]),norm(x["leader_name"])))
    selected_leader=leader.strip() if leader else ""
    detail_rows=[]
    if selected_leader:
        for r in result:
            if norm(r["leader_name"])==norm(selected_leader):
                detail_rows.append(r)
    else:
        # When a single row is selected through section, show its leader detail.
        if len(result)==1:
            selected_leader=result[0]["leader_name"]
            detail_rows=result
    detail={}
    if selected_leader:
        detail_rows=[r for r in rows if norm(r["leader_name"])==norm(selected_leader)]
        detail_rows=[{**r,"project_count":len(p_by_c.get(r["cohort_id"],[])),"student_count":len(e_by_c.get(r["cohort_id"],set()))} for r in detail_rows]
        detail_rows.sort(key=lambda x:(x["semester"],int(x["section"]) if str(x["section"]).isdigit() else str(x["section"])))
        detail_students={e["student_id"] for e in MODEL["enrollments"] if e["cohort_id"] in {r["cohort_id"] for r in detail_rows}}
        detail={"name":selected_leader,"sections":len(detail_rows),"projects":sum(r["project_count"] for r in detail_rows),"students":len(detail_students),"rows":detail_rows}
    return {"rows":result,"detail":detail,"options":_leader_options(period,program,semester,section,leader,subject),"total":len(result),"unique_leaders":len({r["leader_name"] for r in result}),"projects_total":len(VALID_PROJECTS),"students_total":len(MODEL["students"])}

@app.get("/api/collective-leaders")
def api_collective_leaders(period="", program="", semester="", section="", leader="", subject=""):
    return collective_leaders(period,program,semester,section,leader,subject)

@app.get("/api/audit")
def audit():
    excluded=[]
    reason_counts=defaultdict(int)
    for p in INVALID_PROJECTS:
        reason=_project_exclusion_reason(p)
        c=next((x for x in MODEL["cohorts"] if x["id"]==p["cohort_id"]),{})
        item={
            "cohort_id":p["cohort_id"], "filename":c.get("filename", ""),
            "semester":c.get("semester", ""), "section":c.get("section", ""),
            "group":p.get("group", ""), "title":p.get("title", ""),
            "reason":reason
        }
        excluded.append(item); reason_counts[reason]+=1
    mism=[f for f in MODEL["files"] if f.get("sheet_section")!=f.get("section")]
    return {"files":MODEL["files"],"model":{
      "period":"2026-1 · Primer periodo","source":"Archivos Excel locales",
      "note_rule":"Promedio de TERCER CORTE (TER-CORTE) en DEFINITIVAS para el grupo.",
      "title_rule":"Título tomado de LIDER, sección TITULOS DE LOS PROYECTOS DE AULA, según posición G01–G12.",
      "students_rule":"Estudiante = nombre normalizado; no sustituye un ID institucional cuando la fuente no lo proporciona.",
      "project_count_rule":"Proyecto válido: grupo distinto de 0 y nota final mayor que 0; si la nota es 0, se conserva únicamente cuando LIDER documenta un título sustantivo.",
      "project_highlight":"Mayor nota final del grupo por semestre entre proyectos válidos; los empates se conservan.",
      "valid_projects":len(VALID_PROJECTS),
      "excluded_projects":len(INVALID_PROJECTS),
      "excluded_project_keys":[f"{p['cohort_id']}:{p['group']}" for p in INVALID_PROJECTS],
      "excluded":excluded,
      "excluded_by_reason":dict(reason_counts),
      "section_rule":"La sección operativa se toma del nombre del archivo (SEM-XX-SEC-YY) y se contrasta con LIDER!H2.",
      "section_mismatches":len(mism),
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
