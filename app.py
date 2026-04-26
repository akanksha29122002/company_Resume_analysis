import pandas as pd
import streamlit as st

from candidate_store import add_candidate, load_candidates, purge_expired
from company_store import (
    add_company_record,
    company_context_text,
    load_company_records,
    purge_expired_company_records,
    sample_company_records,
    save_company_records,
)
from resume_analyzer import analyze_resume, extract_pdf_text
from vector_store import (
    local_company_context,
    local_rank_candidates,
    pinecone_enabled,
    search_company_pinecone,
    search_pinecone,
    upsert_candidates_to_pinecone,
    upsert_company_records_to_pinecone,
)


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon=":page_facing_up:",
    layout="wide",
)


SAMPLE_JOB = """Python Developer Intern

We are looking for a candidate with Python, SQL, data analysis, Streamlit,
machine learning basics, Git, communication skills, and project experience.
The candidate should be able to build dashboards, clean data, explain results,
and work with APIs."""


def render_badges(items):
    if not items:
        st.caption("No items detected.")
        return
    st.markdown(" ".join([f"`{item}`" for item in items]))


def extract_uploaded_text(uploaded_resume):
    if not uploaded_resume:
        return ""
    return extract_pdf_text(uploaded_resume)


st.title("AI Resume Analyzer and Company Resume Bank")
st.caption("Companies upload requirement documents, candidates upload resumes, both stay active for 6 months, and automation shortlists ideal matches with candidate potential.")

purged = purge_expired()
purged_company = purge_expired_company_records()
if purged or purged_company:
    st.toast(f"Removed {purged} expired candidates and {purged_company} expired company records.")

with st.sidebar:
    st.header("System Status")
    st.write("Pinecone:", "Enabled" if pinecone_enabled() else "Local fallback")
    st.write("Active candidates:", len(load_candidates()))
    st.write("Company records:", len(load_company_records()))
    st.caption("Set PINECONE_API_KEY and PINECONE_INDEX_NAME to enable vector search.")

single_tab, intake_tab, company_tab, matching_tab, database_tab, setup_tab = st.tabs(
    ["Resume Check", "Candidate Upload", "Company Documents", "Auto Match", "Stored Data", "Apps Script Setup"]
)

with single_tab:
    st.subheader("Single Resume Analysis")
    uploaded_resume = st.file_uploader("Upload resume PDF", type=["pdf"], key="single_resume")
    use_sample_job = st.toggle("Use sample job description", value=True)
    show_text = st.toggle("Show extracted resume text", value=False)

    job_description = st.text_area(
        "Job description",
        value=SAMPLE_JOB if use_sample_job else "",
        height=180,
        placeholder="Paste the target job description here...",
        key="single_job",
    )

    if uploaded_resume:
        try:
            resume_text = extract_uploaded_text(uploaded_resume)
            analysis = analyze_resume(resume_text, job_description)
        except Exception as exc:
            st.error(f"Could not read this PDF: {exc}")
            st.stop()

        score_col, semantic_col, keyword_col, words_col = st.columns(4)
        score_col.metric("ATS Score", f"{analysis['ats_score']}/100")
        semantic_col.metric("Semantic Match", f"{analysis['semantic_match']}%")
        keyword_col.metric("Keyword Match", f"{analysis['keyword_match']}%")
        words_col.metric("Resume Words", analysis["word_count"])
        st.progress(analysis["ats_score"] / 100)

        left, right = st.columns([1.05, 0.95])
        with left:
            st.subheader("Detected Sections")
            section_cols = st.columns(3)
            for index, (section, present) in enumerate(analysis["sections"].items()):
                section_cols[index % 3].checkbox(section, value=present, disabled=True, key=f"single_{section}")

            st.subheader("Skills Found")
            for category, skills in analysis["skills_by_category"].items():
                with st.expander(category, expanded=bool(skills)):
                    render_badges(skills)

            st.subheader("Job Skills Missing From Resume")
            render_badges(analysis["missing_skills"])

        with right:
            st.subheader("Strengths")
            for item in analysis["strengths"]:
                st.success(item)
            st.subheader("Weaknesses")
            for item in analysis["weaknesses"]:
                st.warning(item)
            st.subheader("Suggestions")
            for item in analysis["suggestions"]:
                st.write(f"- {item}")

        if show_text:
            st.subheader("Extracted Resume Text")
            st.text_area("Preview", resume_text[:5000], height=300)
    else:
        st.info("Upload one PDF resume to analyze it immediately.")

with intake_tab:
    st.subheader("Candidate Resume Upload")
    st.caption("Candidates or HR can upload resumes here. Each resume remains active for 6 months and can be matched against company requirements.")

    with st.form("candidate_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        name = col1.text_input("Candidate name")
        email = col1.text_input("Email")
        phone = col2.text_input("Phone")
        role_applied = col2.text_input("Role applied")
        candidate_pdf = st.file_uploader("Resume PDF", type=["pdf"], key="candidate_pdf")
        pasted_resume = st.text_area("Or paste resume text", height=160)
        intake_job = st.text_area("Optional role/job description for initial scoring", value=SAMPLE_JOB, height=150)
        submitted = st.form_submit_button("Add Candidate")

    if submitted:
        try:
            resume_text = pasted_resume.strip() or extract_uploaded_text(candidate_pdf)
            if not resume_text:
                st.error("Please upload a resume PDF or paste resume text.")
            else:
                analysis = analyze_resume(resume_text, intake_job or role_applied)
                candidate = add_candidate(
                    name=name,
                    email=email,
                    phone=phone,
                    role_applied=role_applied,
                    resume_text=resume_text,
                    source="streamlit-intake",
                    latest_score=analysis["ats_score"],
                    latest_role=role_applied,
                )
                synced = upsert_candidates_to_pinecone([candidate])
                st.success(f"Candidate added. Initial score: {analysis['ats_score']}/100. Pinecone synced: {'yes' if synced else 'no'}.")
        except Exception as exc:
            st.error(f"Could not add candidate: {exc}")

with company_tab:
    st.subheader("Company Document Upload")
    st.caption("Companies can upload requirement PDFs or paste establishment, growth, technology, project, culture, and hiring details. Each record remains active for 6 months.")

    with st.form("company_record_form", clear_on_submit=True):
        company_name = st.text_input("Company name", value="DemoTech Solutions")
        col1, col2 = st.columns(2)
        record_type = col1.selectbox(
            "Record type",
            ["Establishment", "Growth", "Department", "Project", "Technology", "Requirement", "Culture", "Financial", "Other"],
        )
        date_or_period = col2.text_input("Date or period", placeholder="Example: 2019, Q1 2025, Current")
        title = st.text_input("Title", placeholder="Example: AI practice launched")
        company_doc = st.file_uploader("Company document PDF", type=["pdf"], key="company_doc_pdf")
        details = st.text_area(
            "Full details or extra notes",
            height=160,
            placeholder="Write company establishment story, growth, products, clients, hiring needs, tech stack, expansion, achievements, or requirements. If a PDF is uploaded, its text will be stored with these notes.",
        )
        tags = st.text_input("Tags", placeholder="python, ai, sales-growth, healthcare, cloud")
        add_company = st.form_submit_button("Save Company Record")

    if add_company:
        try:
            document_text = extract_uploaded_text(company_doc)
        except Exception as exc:
            document_text = ""
            st.warning(f"Could not extract company PDF text: {exc}")
        full_details = "\n\n".join([part for part in [document_text, details.strip()] if part])
        if not full_details.strip():
            st.error("Please upload a company PDF or add company details before saving.")
        else:
            record = add_company_record(company_name, record_type, title, date_or_period, full_details, tags)
            synced = upsert_company_records_to_pinecone([record])
            st.success(f"Company document saved for 6 months. Pinecone synced: {'yes' if synced else 'no'}.")

    col1, col2, col3 = st.columns(3)
    if col1.button("Load Sample Company History"):
        records = load_company_records()
        records.extend(sample_company_records())
        save_company_records(records)
        st.success("Sample establishment, growth, and requirement records added.")
    if col2.button("Sync Company Records to Pinecone"):
        count = upsert_company_records_to_pinecone(load_company_records())
        if count:
            st.success(f"Synced {count} company records to Pinecone.")
        else:
            st.warning("Pinecone is not configured, so records remain in local storage.")
    if col3.button("Refresh Company Records"):
        st.rerun()

    query = st.text_input("Search company knowledge", placeholder="Example: AI growth, Python requirement, company establishment")
    if query:
        context_rows = []
        if pinecone_enabled():
            context_rows = search_company_pinecone(query, limit=8)
        if not context_rows:
            context_rows = local_company_context(query, limit=8)
        if context_rows:
            st.dataframe(pd.DataFrame(context_rows), use_container_width=True)
        else:
            st.info("No company records found yet.")

    company_records = load_company_records()
    if company_records:
        st.markdown("**Stored Company Timeline and Requirements**")
        st.dataframe(pd.DataFrame(company_records), use_container_width=True)
    else:
        st.info("Add company records manually or load sample company history.")

with matching_tab:
    st.subheader("Automatic Ideal Match Finder")
    st.caption("Paste a requirement or rely on stored company documents. The app finds the best active resumes and tells the company who is ideal and what their potential is.")
    role_description = st.text_area(
        "Paste new company requirement",
        value=SAMPLE_JOB,
        height=220,
        key="role_matching_description",
    )
    limit = st.slider("Candidates to show", min_value=3, max_value=25, value=10)
    use_pinecone = st.toggle("Use Pinecone search when available", value=True)
    include_company_context = st.toggle("Include company growth and requirement context", value=True)

    if st.button("Find Ideal Matches"):
        effective_role_description = role_description
        if include_company_context:
            context = company_context_text()
            if context:
                effective_role_description = f"{role_description}\n\nCompany context:\n{context}"

        rows = []
        if use_pinecone and pinecone_enabled():
            rows = search_pinecone(effective_role_description, limit=limit)
        if not rows:
            rows = local_rank_candidates(effective_role_description, limit=limit)

        if rows:
            df = pd.DataFrame(rows)
            visible = [
                "match_score",
                "potential",
                "recommendation",
                "ats_score",
                "semantic_match",
                "name",
                "email",
                "phone",
                "role_applied",
                "missing_skills",
                "strengths",
                "expires_at",
            ]
            st.dataframe(df[[col for col in visible if col in df.columns]], use_container_width=True)
            ideal = df[df["potential"].isin(["Ideal Match", "Strong Potential"])] if "potential" in df.columns else pd.DataFrame()
            if not ideal.empty:
                top = ideal.iloc[0]
                st.success(
                    f"Best candidate to send to company: {top.get('name', 'Candidate')} "
                    f"({top.get('potential', 'Potential')}, score {top.get('match_score', 0)}/100). "
                    f"{top.get('recommendation', '')}"
                )
            st.download_button(
                "Download shortlist CSV",
                df.to_csv(index=False).encode("utf-8"),
                file_name="candidate_shortlist.csv",
                mime="text/csv",
            )
        else:
            st.info("No active candidates found. Add resumes through Company Intake or Apps Script first.")

with database_tab:
    st.subheader("Stored Active Data")
    st.caption("Candidate resumes and company documents are kept active for approximately 6 months.")
    candidates = load_candidates()
    if st.button("Sync Active Candidates to Pinecone"):
        count = upsert_candidates_to_pinecone(candidates)
        if count:
            st.success(f"Synced {count} candidates to Pinecone.")
        else:
            st.warning("Pinecone is not configured, so the app is using local search.")

    if candidates:
        df = pd.DataFrame(candidates)
        columns = [
            "name",
            "email",
            "phone",
            "role_applied",
            "latest_score",
            "latest_role",
            "source",
            "uploaded_at",
            "expires_at",
            "status",
        ]
        st.dataframe(df[[col for col in columns if col in df.columns]], use_container_width=True)
        st.download_button(
            "Export Candidate Database CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name="active_candidates.csv",
            mime="text/csv",
        )
    else:
        st.info("No active candidate records yet.")

    company_records = load_company_records()
    st.markdown("**Active Company Documents and Requirements**")
    if company_records:
        st.dataframe(pd.DataFrame(company_records), use_container_width=True)
    else:
        st.info("No active company documents yet.")

with setup_tab:
    st.subheader("Automatic Resume Intake With Google Apps Script")
    st.write("Create a Google Form with fields named exactly: Name, Email, Phone, Role Applied, Resume Upload, Resume Text.")
    st.write("Attach the Apps Script in `apps_script/Code.gs` to the linked Google Sheet and create an installable `On form submit` trigger.")
    st.code(
        """Required deployment variables:

PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=resume-candidates
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
INTAKE_TOKEN=choose_a_secret_token

Webhook endpoint for Apps Script:
https://YOUR-RENDER-APP.onrender.com/ingest""",
        language="text",
    )
    st.write("Use the Company Growth tab to store establishment history, company expansion, departments, projects, tech stack, culture, and requirement changes. These records can be synced to Pinecone and used as context during candidate ranking.")
