from datetime import date, timedelta
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import func
from config import DISCLAIMER, DATABASE_PATH, WORKFLOW_STATUSES, DEMO_MODE as DEFAULT_DEMO_MODE
from database.db import init_db, get_session
from database.models import Case, Event, Assessment, FollowUp, ReferenceSafetyInformation, QCReview, AuditLog, TrainingAssessment
from services.case_service import create_case, update_case, update_status, possible_duplicates, reset_demo_data
from services.follow_up_service import create_follow_up, update_follow_up
from services.dashboard_service import filter_by_received_date, dashboard_metrics
from services.assessment_service import compare_expectedness
from services.validation_service import minimum_criteria, missing_criteria, date_issues
from services.narrative_service import narrative
from services.report_service import cases_csv, cases_excel, dataframe_csv
from services.backup_service import backup_database
from sample_data.seed_data import seed
from modules.training import QUESTIONS
from modules.training import evaluate_answers

st.set_page_config(page_title="PV CasePro", page_icon="🛡️", layout="wide")
DEMO_MODE=DEFAULT_DEMO_MODE
try:
    configured_demo=st.secrets.get("PV_CASEPRO_DEMO_MODE")
    if configured_demo is not None: DEMO_MODE=str(configured_demo).strip().lower() not in {"0","false","no"}
except Exception:
    pass
st.markdown("""<style>
.stApp{background:#f4f7fa;color:#152d47}.block-container{padding-top:1.5rem}
[data-testid="stSidebar"]{background:#102d4a}[data-testid="stSidebar"] *{color:#f3f7fa}.stMetric{background:white;border:1px solid #d9e4ed;padding:14px;border-radius:10px}
.disclaimer{background:#fff4d6;border:1px solid #e5c66d;padding:10px 14px;border-radius:7px;font-weight:700;color:#4d421c}
h1,h2,h3{color:#12345a}
</style>""", unsafe_allow_html=True)
st.markdown(f'<div class="disclaimer">{DISCLAIMER}</div>', unsafe_allow_html=True)

init_db(); db=get_session()
if "seeded" not in st.session_state:
    seed(db); st.session_state.seeded=True

st.sidebar.title("PV CasePro")
if DEMO_MODE:
    st.sidebar.info("Read-only public demo")
    pages=["Dashboard","Case library","Reports & export","About"]
else:
    pages=["Dashboard","Case intake","Case edit","Case assessment","Terminology practice","Expectedness & RSI","Follow-up management","Narrative generator","Quality control","Case workflow","Reports & export","Training assessment","Data & backup","About"]
page=st.sidebar.radio("Navigation",pages)
st.sidebar.caption("Fictional training data only")

def all_cases(): return db.query(Case).order_by(Case.created_at.desc()).all()
def case_picker(label="Select case"):
    cases=all_cases()
    if not cases: st.info("No cases available yet."); return None
    return st.selectbox(label,cases,format_func=lambda c:f"{c.case_id} · {c.event_verbatim or 'Event not reported'}")
def text_or_none(x): return x.strip() or None if isinstance(x,str) else x

if page=="Dashboard":
    st.title("Safety operations overview")
    cs=all_cases(); min_d=date.today()-timedelta(days=365)
    start=st.date_input("Received from", value=min_d); end=st.date_input("Through",value=date.today())
    cs=filter_by_received_date(cs,start,end)
    metrics=dashboard_metrics(cs,db.query(FollowUp).filter(FollowUp.status=='Open').count())
    for row in (list(metrics.items())[:5],list(metrics.items())[5:]):
        for slot,(label,value) in zip(st.columns(len(row)),row): slot.metric(label,value)
    col1,col2=st.columns(2)
    if cs:
        df=pd.DataFrame([{"Case ID":c.case_id,"Seriousness":c.seriousness,"Outcome":c.outcome or "Unknown","Status":c.status,"Month":c.received_date.strftime("%Y-%m") if c.received_date else "Unknown","Event":c.training_term or "Uncoded"} for c in cs])
        for slot,field,title in [(col1,"Seriousness","Cases by seriousness"),(col2,"Outcome","Cases by outcome")]: slot.plotly_chart(px.histogram(df,x=field,color=field,title=title),width="stretch")
        for slot,field,title in [(col1,"Status","Cases by workflow status"),(col2,"Month","Cases by month")]: slot.plotly_chart(px.histogram(df,x=field,title=title),width="stretch")
        st.plotly_chart(px.histogram(df,x="Event",title="Cases by reported event category"),width="stretch")
        st.subheader("Recent cases"); st.dataframe(df.head(12),width="stretch",hide_index=True)
    else: st.info("No cases match the selected date range.")
    st.caption(f"Cases requiring follow-up: {metrics['Cases requiring follow-up']} · Completed: {metrics['Completed']}")

elif page=="Case intake":
    st.title("ICSR case intake"); st.caption("Required minimum criteria: identifiable patient, identifiable reporter, suspect product and event.")
    st.caption("Leave fields blank when not provided. If the source explicitly says information is unknown, record 'Unknown'. Never infer missing patient or clinical details.")
    with st.form("intake"):
        a,b=st.columns(2)
        report_type=a.selectbox("Report type",["Initial","Follow-up"]); received=a.date_input("Date first received",value=date.today()); country=b.text_input("Country"); reporter_type=b.selectbox("Reporter type",["Healthcare professional","Consumer","Lawyer","Other","Unknown"])
        reporter=b.text_input("Reporter name or fictional identifier *"); contact=b.text_input("Reporter contact details (optional)"); patient=a.text_input("Patient identifier *"); age_group=a.selectbox("Patient age group",["Unknown","Neonate","Infant","Child","Adolescent","Adult","Elderly"]); age=a.text_input("Age (if reported)"); sex=b.selectbox("Patient sex",["Not provided","Female","Male","Other","Unknown"])
        product=b.text_input("Suspect medicinal product *"); strength=b.text_input("Product strength"); dose=b.text_input("Dose"); route=b.text_input("Route"); frequency=b.text_input("Frequency"); indication=b.text_input("Indication")
        ts=a.date_input("Therapy start date",value=None); te=b.date_input("Therapy stop date",value=None); event=st.text_area("Adverse event verbatim *"); onset=a.date_input("Event onset date",value=None); ended=b.date_input("Event end date",value=None); outcome=st.selectbox("Event outcome",["Unknown","Recovered","Recovering","Not recovered","Recovered with sequelae","Fatal","Not applicable"])
        medical=st.text_area("Relevant medical history"); concom=st.text_area("Concomitant medications"); dechallenge=st.text_input("Dechallenge information"); rechallenge=st.text_input("Rechallenge information"); source=st.text_area("Source narrative"); comments=st.text_area("Additional comments")
        submitted=st.form_submit_button("Save case",type="primary")
    if submitted:
        data=locals().copy(); vals={"report_type":report_type,"received_date":received,"country":text_or_none(country),"reporter_type":reporter_type,"reporter_name":text_or_none(reporter),"reporter_contact":text_or_none(contact),"patient_identifier":text_or_none(patient),"age_group":None if age_group=="Unknown" else age_group,"age":text_or_none(age),"sex":None if sex in ("Unknown","Not provided") else sex,"product":text_or_none(product),"strength":text_or_none(strength),"dose":text_or_none(dose),"route":text_or_none(route),"frequency":text_or_none(frequency),"indication":text_or_none(indication),"therapy_start":ts,"therapy_stop":te,"event_verbatim":text_or_none(event),"event_onset":onset,"event_end":ended,"outcome":None if outcome=="Unknown" else outcome,"medical_history":text_or_none(medical),"concomitant_meds":text_or_none(concom),"dechallenge":text_or_none(dechallenge),"rechallenge":text_or_none(rechallenge),"narrative_source":text_or_none(source),"comments":text_or_none(comments)}
        missing=missing_criteria(vals); issues=date_issues(vals)
        if missing or issues: st.error("Please correct: " + "; ".join(missing+issues))
        else:
            matches=possible_duplicates(db,vals)
            if matches: st.warning("Possible similar cases: "+", ".join(x.case_id for x in matches)+". Verify manually before saving.")
            try: c=create_case(db,vals); st.success(f"Saved {c.case_id}.")
            except Exception as e: db.rollback(); st.error(str(e))

elif page=="Case edit":
    st.title("Edit case information"); c=case_picker()
    if c:
        with st.form("case_edit"):
            patient=st.text_input("Patient identifier",c.patient_identifier or "")
            reporter=st.text_input("Reporter identifier",c.reporter_name or "")
            contact=st.text_input("Reporter contact",c.reporter_contact or "")
            product=st.text_input("Suspect product",c.product or "")
            strength=st.text_input("Strength",c.strength or "")
            dose=st.text_input("Dose",c.dose or "")
            route=st.text_input("Route",c.route or "")
            event=st.text_area("Event verbatim",c.event_verbatim or "")
            onset=st.date_input("Event onset",value=c.event_onset)
            ended=st.date_input("Event end",value=c.event_end)
            outcome=st.text_input("Outcome (blank means unknown)",c.outcome or "")
            comments=st.text_area("Additional comments",c.comments or "")
            save=st.form_submit_button("Save case changes")
        if save:
            try:
                update_case(db,c,{"patient_identifier":text_or_none(patient),"reporter_name":text_or_none(reporter),"reporter_contact":text_or_none(contact),"product":text_or_none(product),"strength":text_or_none(strength),"dose":text_or_none(dose),"route":text_or_none(route),"event_verbatim":text_or_none(event),"event_onset":onset,"event_end":ended,"outcome":text_or_none(outcome),"comments":text_or_none(comments)})
                st.success("Case changes saved and audit logged.")
            except Exception as e: db.rollback(); st.error(str(e))

elif page=="Case library":
    st.title("Synthetic case library")
    search=st.text_input("Search case ID, event, product or status")
    cs=all_cases()
    if search:
        q=search.casefold(); cs=[c for c in cs if q in " ".join(str(v or "") for v in (c.case_id,c.event_verbatim,c.product,c.status,c.outcome)).casefold()]
    st.dataframe(pd.DataFrame([{"Case ID":c.case_id,"Report type":c.report_type,"Received":c.received_date,"Patient":c.patient_identifier,"Product":c.product,"Event":c.event_verbatim,"Seriousness":c.seriousness,"Outcome":c.outcome or "Unknown","Status":c.status} for c in cs]),width="stretch",hide_index=True)
    c=case_picker("View synthetic case")
    if c: st.text_area("Educational case narrative",value=c.reviewed_narrative or narrative(c),height=360,disabled=True)

elif page=="About":
    st.title("About PV CasePro")
    st.markdown(f"> **{DISCLAIMER}**")
    st.write("This portfolio application uses fictional training cases to demonstrate ICSR intake, assessment, follow-up, QC and reporting concepts. It is not a validated system, official terminology product, or real-world reporting tool.")

elif page=="Case assessment":
    st.title("Structured case assessment"); c=case_picker()
    if c:
        st.caption("Severity and seriousness are different. Assessments are educational and may require medical review.")
        st.write("Four criteria:",minimum_criteria({k:getattr(c,k) for k in ["patient_identifier","reporter_name","product","event_verbatim"]}))
        refs=db.query(ReferenceSafetyInformation).filter(func.lower(ReferenceSafetyInformation.product)==(c.product or "").lower()).all()
        if not refs: st.warning("Expectedness cannot be assessed — reference safety information not provided.")
        with st.form("assessment"):
            serious=st.selectbox("Seriousness",["Unknown","Serious","Non-serious"],index=["Unknown","Serious","Non-serious"].index(c.seriousness))
            criteria=st.multiselect("Seriousness criteria",["Death","Life-threatening","Hospitalisation","Prolongation of hospitalisation","Persistent or significant disability","Congenital anomaly","Other medically important condition"],default=(c.serious_criteria or "").split("; ") if c.serious_criteria else [])
            severity=st.selectbox("Event severity",["Unknown","Mild","Moderate","Severe"],index=["Unknown","Mild","Moderate","Severe"].index(c.severity))
            serious_rationale=st.text_area("Seriousness rationale / information supporting classification",value=c.seriousness_rationale or "")
            causality=st.selectbox("Educational causality assessment",["Not assessed","Related","Possibly related","Unlikely related","Unassessable/insufficient information"])
            rationale=st.text_area("Causality rationale",value=c.causality_rationale or "")
            expected_options=["Not assessed","Expected","Unexpected","Unknown — insufficient information"] if refs else ["Not assessed","Unknown — reference safety information not provided"]
            current_expected=c.expectedness if c.expectedness in expected_options else expected_options[-1] if not refs else "Not assessed"
            expected=st.selectbox("Expectedness",expected_options,index=expected_options.index(current_expected))
            reviewer=st.text_area("Medical reviewer comments",value=c.reviewer_comments or ""); save=st.form_submit_button("Save assessment")
        if save:
            if serious=="Serious" and not criteria: st.error("A serious classification needs at least one documented seriousness criterion.")
            elif serious=="Non-serious" and not serious_rationale.strip(): st.error("Document the available basis for a non-serious classification, or select Unknown.")
            else:
                c.seriousness=serious;c.serious_criteria="; ".join(criteria) or None;c.seriousness_rationale=text_or_none(serious_rationale);c.severity=severity;c.causality=causality;c.causality_rationale=text_or_none(rationale);c.expectedness=expected;c.reviewer_comments=text_or_none(reviewer)
                record=db.query(Assessment).filter_by(case_id=c.id).one_or_none()
                if record:
                    record.seriousness=serious;record.seriousness_criteria=c.serious_criteria;record.seriousness_rationale=c.seriousness_rationale;record.severity=severity;record.causality=causality;record.expectedness=expected
                db.commit();st.success("Assessment saved for educational review.")

elif page=="Terminology practice":
    st.title("Medical terminology practice");st.info("Fictional training vocabulary only. This is not official MedDRA terminology and does not provide MedDRA certification.")
    c=case_picker()
    if c:
        st.write("Reported verbatim:",c.event_verbatim or "Not reported")
        with st.form("terms"):
            term=st.selectbox("Training concept",["Unselected","Headache","Nausea","Rash","Dizziness","Vomiting","Other / not represented"]); rationale=st.text_area("Coding rationale",value=c.terminology_rationale or ""); comments=st.text_area("Reviewer comments");save=st.form_submit_button("Save training selection")
        if save:
            c.training_term=None if term=="Unselected" else term;c.terminology_rationale=text_or_none(rationale);c.reviewer_comments=comments or c.reviewer_comments
            record=db.query(Event).filter_by(case_id=c.id).one_or_none()
            if record: record.training_term=c.training_term;record.coding_rationale=c.terminology_rationale
            db.commit();st.success("Training selection saved.")

elif page=="Expectedness & RSI":
    st.title("Expectedness and reference safety information");st.caption("Use only a supplied fictional reference for this training exercise.")
    with st.form("rsi"):
        p=st.text_input("Fictional product");v=st.text_input("Document version");effective=st.date_input("Effective date",value=None);listed=st.text_area("Listed adverse events (separate with commas)");desc=st.text_area("Document description");save=st.form_submit_button("Save fictional reference")
    if save and p and v and listed:
        db.add(ReferenceSafetyInformation(product=p,version=v,effective_date=effective,listed_events=listed,description=desc));db.commit();st.success("Fictional reference saved.")
    c=case_picker()
    if c:
        refs=db.query(ReferenceSafetyInformation).filter(func.lower(ReferenceSafetyInformation.product)==(c.product or "").lower()).all()
        if not refs: st.warning("Expectedness cannot be assessed — reference safety information not provided.")
        else:
            ref=st.selectbox("Reference version",refs,format_func=lambda r:f"{r.product} · {r.version} · {r.effective_date}")
            st.info(compare_expectedness(c.training_term or c.event_verbatim,ref.listed_events.split(",")))

elif page=="Follow-up management":
    st.title("Follow-up management");c=case_picker()
    if c:
        existing=db.query(FollowUp).filter_by(case_id=c.id).order_by(FollowUp.id.desc()).all()
        selected=st.selectbox("Existing follow-up to update",[None]+existing,format_func=lambda x:"Create new follow-up" if x is None else f"#{x.id} · {x.status}")
        with st.form("followup"):
            missing=st.text_area("Missing information",value=selected.missing_information if selected else "")
            questions=st.text_area("Neutral follow-up questions (one per line)",value=(selected.questions or "") if selected else "")
            sent=st.date_input("Date sent",value=selected.date_sent if selected else None)
            response_date=st.date_input("Response date",value=selected.response_date if selected else None)
            response=st.text_area("Response received",value=(selected.response_received or "") if selected else "")
            status=st.selectbox("Status",["Open","Sent","Response received","Closed"],index=["Open","Sent","Response received","Closed"].index(selected.status) if selected else 0)
            comment=st.text_area("Comments",value=(selected.comments or "") if selected else "")
            save=st.form_submit_button("Save follow-up")
        if save and missing:
            data={"missing_information":missing,"questions":questions,"date_sent":sent,"response_date":response_date,"response_received":response,"status":status,"comments":comment}
            try:
                if selected: update_follow_up(db,selected,data)
                else: create_follow_up(db,c.id,data)
                st.success("Follow-up saved. No email was sent.")
            except ValueError as exc: db.rollback(); st.error(str(exc))
    st.subheader("Professional template")
    st.text_area("Template",value="Subject: Request for additional information — [fictional case reference]\n\nDear Reporter,\n\nTo help complete our educational case record, please provide any information available about:\n[neutral questions]\n\nPlease share only information you are authorized to provide. Thank you for your assistance.\n\nKind regards,\nPV CasePro Training Team",height=190)
    st.dataframe(pd.read_sql(db.query(FollowUp).statement,db.bind) if db.query(FollowUp).count() else pd.DataFrame(),width="stretch")

elif page=="Narrative generator":
    st.title("ICSR narrative generator");c=case_picker()
    if c:
        draft=c.reviewed_narrative or narrative(c);edited=st.text_area("Review and edit before saving",value=draft,height=430)
        if st.button("Save reviewed narrative"): c.reviewed_narrative=edited;db.commit();st.success("Reviewed narrative saved separately from the source narrative.")
        st.download_button("Download case narrative",f"{DISCLAIMER}\n\n{edited}",file_name=f"{c.case_id}_narrative.txt")

elif page=="Quality control":
    st.title("Quality control review");c=case_picker()
    if c:
        misses=missing_criteria({k:getattr(c,k) for k in ["patient_identifier","reporter_name","product","event_verbatim"]});dates=date_issues({k:getattr(c,k) for k in ["received_date","event_onset","event_end","therapy_start","therapy_stop"]})
        checks={"Four minimum criteria":("Fail" if misses else "Pass"),"Patient identification":("Fail" if not c.patient_identifier else "Pass"),"Reporter identification":("Fail" if not c.reporter_name else "Pass"),"Product details":("Fail" if not c.product else "Pass"),"Event verbatim":("Fail" if not c.event_verbatim else "Pass"),"Receipt date":("Fail" if not c.received_date else "Pass"),"Event onset date":("Not applicable" if not c.event_onset else "Pass"),"Event chronology":("Fail" if dates else "Pass"),"Outcome":("Not applicable" if not c.outcome else "Pass"),"Seriousness rationale":("Not applicable" if c.seriousness!="Serious" else ("Pass" if c.serious_criteria else "Fail")),"Missing information":("Fail" if misses else "Pass"),"Possible duplicate":("Not applicable"),"Narrative consistency":("Not reviewed"),"Unresolved discrepancies":("Fail" if dates else "Not applicable")}
        if misses: st.warning("Missing: "+", ".join(misses))
        if dates: st.error("Date issues: "+", ".join(dates))
        answers={}
        for label,default in checks.items(): answers[label]=st.selectbox(label,["Pass","Fail","Not applicable"],index=["Pass","Fail","Not applicable"].index(default) if default in ["Pass","Fail","Not applicable"] else 0)
        reviewer=st.text_input("Human reviewer identifier");final=st.selectbox("Final human review status",["Not reviewed","Needs correction","Reviewed for educational use"]);comment=st.text_area("Reviewer comments")
        if st.button("Save QC review"):
            c.qc_errors="; ".join(misses+dates) or None;c.human_review_status=final;db.add(QCReview(case_id=c.id,checklist=str(answers),reviewer=reviewer,final_status=final,comments=comment));db.commit();st.success("QC review recorded. Software checks do not approve cases automatically.")
        st.json(checks)

elif page=="Case workflow":
    st.title("Case workflow and audit history");c=case_picker()
    if c:
        st.write("Current status:",c.status)
        with st.form("workflow"):
            status=st.selectbox("New status",WORKFLOW_STATUSES,index=WORKFLOW_STATUSES.index(c.status));user=st.text_input("User or reviewer identifier","Local user");comment=st.text_area("Transition comment");save=st.form_submit_button("Record status change")
        if save:
            update_status(db,c,status,user,comment);st.success("Workflow transition recorded in audit history.")
        logs=db.query(AuditLog).filter(AuditLog.case_id==c.case_id).order_by(AuditLog.timestamp.desc()).all();st.dataframe(pd.DataFrame([{"Action":x.action,"From":x.previous_value,"To":x.new_value,"When (UTC)":x.timestamp,"User":x.user,"Comment":x.comment} for x in logs]),width="stretch")

elif page=="Reports & export":
    st.title("Reports and export");cs=all_cases();st.dataframe(pd.DataFrame([{"Case ID":c.case_id,"Type":c.report_type,"Received":c.received_date,"Country":c.country,"Product":c.product,"Event":c.event_verbatim,"Seriousness":c.seriousness,"Outcome":c.outcome,"Status":c.status} for c in cs]),width="stretch")
    st.download_button("Export case list CSV",cases_csv(cs),"pv_casepro_cases.csv","text/csv");st.download_button("Export case data Excel",cases_excel(cs),"pv_casepro_cases.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    c=case_picker("Choose case summary")
    if c:
        summary=f"{DISCLAIMER}\n\nPV CasePro educational case summary\nCase ID: {c.case_id}\nType: {c.report_type}\nReceived: {c.received_date}\nCountry: {c.country or 'Not reported'}\nPatient: {c.patient_identifier or 'Not reported'}\nReporter: {c.reporter_name or 'Not reported'}\nProduct: {c.product or 'Not reported'}\nEvent: {c.event_verbatim or 'Not reported'}\nSeriousness: {c.seriousness}\nOutcome: {c.outcome or 'Unknown'}\nWorkflow status: {c.status}\n\n{narrative(c)}"
        st.download_button("Export individual case summary",summary,f"{c.case_id}_summary.txt")
    followups=pd.read_sql(db.query(FollowUp).statement,db.bind) if db.query(FollowUp).count() else pd.DataFrame(columns=["case_id","missing_information","status"])
    qc_rows=pd.read_sql(db.query(QCReview).statement,db.bind) if db.query(QCReview).count() else pd.DataFrame(columns=["case_id","final_status"])
    st.download_button("Export follow-up report CSV",dataframe_csv(followups),"pv_casepro_followups.csv","text/csv")
    st.download_button("Export QC report CSV",dataframe_csv(qc_rows),"pv_casepro_qc.csv","text/csv")

elif page=="Training assessment":
    st.title("PV knowledge assessment");st.caption("Educational quiz only; not a substitute for official training or regulatory guidance.")
    if "quiz_order" not in st.session_state: st.session_state.quiz_order=list(range(len(QUESTIONS)))
    with st.form("quiz"):
        answers=[]
        for i,(q,options,correct,explanation) in enumerate(QUESTIONS): answers.append(st.radio(f"{i+1}. {q}",options,key=f"q{i}"))
        done=st.form_submit_button("Evaluate assessment")
    if done:
        score,details=evaluate_answers(answers)
        db.add(TrainingAssessment(score=score,total=len(QUESTIONS),answers=str(details)));db.commit();st.success(f"Score: {score}/{len(QUESTIONS)} ({score*100//len(QUESTIONS)}%)")
        for x in details: st.write(("✅ " if x["correct"] else "❌ ")+x["question"]+" — "+x["explanation"])
    history=db.query(TrainingAssessment).order_by(TrainingAssessment.completed_at.desc()).limit(10).all();st.subheader("Attempt history");st.dataframe(pd.DataFrame([{"Completed (UTC)":h.completed_at,"Score":h.score,"Total":h.total} for h in history]),width="stretch")

elif page=="Data & backup":
    st.title("Data management");st.caption("Local SQLite database. Use only fictional training information.")
    try: st.download_button("Download database backup",backup_database(DATABASE_PATH),"pv_casepro_backup.db","application/octet-stream")
    except (OSError,RuntimeError) as exc: st.error(f"Could not create database backup: {exc}")
    st.warning("Deleting demo rows permanently removes only records explicitly marked as synthetic demo data.")
    if st.checkbox("I understand this will delete identified demo cases and their dependent records"):
        if st.button("Delete demo data",type="secondary"):
            try: n=reset_demo_data(db,confirmed=True);st.success(f"Deleted {n} synthetic demo cases and their dependent records.")
            except Exception as exc: db.rollback();st.error(f"Demo data could not be reset: {exc}")

db.close()
