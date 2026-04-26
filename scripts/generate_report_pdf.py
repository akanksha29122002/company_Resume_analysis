from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    Image,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT = Path("2202113_Akanksha_Kumari_Slashmark_Report.pdf")
LOGO = Path("assets/nit_patna_logo_reference.png")


PROJECT_TITLE = "Company Resume Analysis and Ideal Match Finder using Pinecone RAG"
STUDENT_NAME = "Akanksha Kumari"
ROLL_NO = "2202113"
DEPARTMENT = "Electrical Engineering"
INSTITUTE = "National Institute of Technology Patna"
COMPANY = "Slashmark"
INTERNSHIP_ROLE = "Machine Learning Engineer Intern at Slashmark"
DOMAIN = "Machine Learning Internship"
INTERN_EMAIL = "akankshainfinity1@gmail.com"
INTERN_ID = "SM82389"
BATCH_DURATION = "Dec 15, 2025 to April 15, 2026"
SUPERVISOR = "Slashmark Technical Team"


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontName="Times-Bold",
        fontSize=22,
        leading=27,
        spaceAfter=18,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverText",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontName="Times-Bold",
        fontSize=16,
        leading=22,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="ChapterTitle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontName="Times-Bold",
        fontSize=16,
        leading=21,
        spaceAfter=18,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyJustify",
        parent=styles["BodyText"],
        alignment=TA_JUSTIFY,
        fontName="Times-Roman",
        fontSize=11.5,
        leading=16,
        spaceAfter=9,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyCenter",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontName="Times-Roman",
        fontSize=12,
        leading=17,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="SubHeading",
        parent=styles["Heading2"],
        alignment=TA_LEFT,
        fontName="Times-Bold",
        fontSize=13,
        leading=17,
        spaceBefore=6,
        spaceAfter=8,
    )
)


class BoxDiagram(Flowable):
    def __init__(self, labels):
        super().__init__()
        self.labels = labels
        self.width = 470
        self.height = 90

    def draw(self):
        box_w = 82
        box_h = 42
        gap = 14
        x = 0
        y = 25
        for index, label in enumerate(self.labels):
            self.canv.setStrokeColor(colors.HexColor("#1f4e79"))
            self.canv.setFillColor(colors.HexColor("#eaf2f8"))
            self.canv.roundRect(x, y, box_w, box_h, 5, stroke=1, fill=1)
            self.canv.setFillColor(colors.black)
            self.canv.setFont("Times-Bold", 8.5)
            lines = label.split("|")
            for i, line in enumerate(lines):
                self.canv.drawCentredString(x + box_w / 2, y + 25 - (i * 10), line)
            if index < len(self.labels) - 1:
                ax = x + box_w
                self.canv.line(ax + 2, y + box_h / 2, ax + gap - 2, y + box_h / 2)
                self.canv.line(ax + gap - 8, y + box_h / 2 + 4, ax + gap - 2, y + box_h / 2)
                self.canv.line(ax + gap - 8, y + box_h / 2 - 4, ax + gap - 2, y + box_h / 2)
            x += box_w + gap


def p(text, style="BodyJustify"):
    return Paragraph(text, styles[style])


def bullets(items):
    return ListFlowable(
        [ListItem(p(item), leftIndent=12) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=20,
    )


def add_page_number(canvas, doc):
    page = canvas.getPageNumber()
    if page == 1:
        return
    canvas.saveState()
    canvas.setFont("Times-Roman", 9)
    canvas.drawCentredString(A4[0] / 2, 0.45 * inch, str(page - 1))
    canvas.restoreState()


def cover_page():
    story = []
    story.append(Spacer(1, 0.45 * inch))
    story.append(p("NATIONAL INSTITUTE OF TECHNOLOGY<br/>PATNA", "CoverTitle"))
    if LOGO.exists():
        story.append(Image(str(LOGO), width=1.45 * inch, height=1.45 * inch))
    story.append(Spacer(1, 0.35 * inch))
    story.append(p("RESEARCH PROJECT-II", "CoverText"))
    story.append(Spacer(1, 0.20 * inch))
    story.append(p(INTERNSHIP_ROLE, "CoverText"))
    story.append(p(f"Batch: &nbsp; {BATCH_DURATION}", "BodyCenter"))
    story.append(Spacer(1, 0.35 * inch))
    story.append(p("Submitted by", "CoverText"))
    story.append(p(f"Name: {STUDENT_NAME}", "CoverText"))
    story.append(p(f"Roll No: {ROLL_NO}", "BodyCenter"))
    story.append(Spacer(1, 0.20 * inch))
    story.append(p(f"Department: {DEPARTMENT}", "CoverText"))
    story.append(Spacer(1, 0.42 * inch))
    story.append(p("Under the supervision of", "CoverText"))
    story.append(p(SUPERVISOR, "BodyCenter"))
    story.append(p(f"({COMPANY})", "BodyCenter"))
    story.append(Spacer(1, 0.25 * inch))
    story.append(p("SLASHMARK", "CoverText"))
    story.append(PageBreak())
    return story


def certificate_pages():
    return [
        p("CERTIFICATE", "ChapterTitle"),
        p(
            f"This is to certify that {STUDENT_NAME} ({ROLL_NO}) has carried out the internship "
            f"work entitled \"{PROJECT_TITLE}\" under the domain of {DOMAIN}. "
            "This technical report is a bonafide record of the work completed for the partial "
            "fulfillment of the internship and academic requirements.",
        ),
        Spacer(1, 2.2 * inch),
        Table(
            [
                ["Dr. Amitesh Kumar", "Dr. Vimlesh Kumar"],
                ["(Professor In-Charge)", "(Head of Department)"],
                ["Department of EE, NIT Patna", "Department of EE, NIT Patna"],
            ],
            colWidths=[2.6 * inch, 2.6 * inch],
            style=TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONT", (0, 0), (-1, 0), "Times-Bold", 11),
                    ("FONT", (0, 1), (-1, -1), "Times-Roman", 10),
                ]
            ),
        ),
        PageBreak(),
        p("CERTIFICATE", "ChapterTitle"),
        p("To Whom It May Concern", "BodyCenter"),
        Spacer(1, 0.25 * inch),
        p("<b>Formal Data:</b>"),
        p(f"Student's Name: {STUDENT_NAME}"),
        p(f"Roll Number: {ROLL_NO}"),
        p(f"Institution: {INSTITUTE}"),
        p(f"Company: {COMPANY}"),
        Spacer(1, 0.2 * inch),
        p("<b>Evaluation of Work:</b>"),
        p(
            f"The student has worked on the internship project \"{PROJECT_TITLE}\". The project demonstrates "
            "the use of Streamlit, FastAPI, Google Apps Script, Pinecone vector database, and a "
            "retrieval-augmented matching workflow for company requirements and candidate resumes. "
            "The work reflects independent learning, analytical ability, and practical application "
            "of software engineering concepts.",
        ),
        Spacer(1, 1.6 * inch),
        p("For EE Department, NIT Patna"),
        PageBreak(),
    ]


def prelim_pages():
    return [
        p("DECLARATION AND COPYRIGHT TRANSFER", "ChapterTitle"),
        p(
            f"I, {STUDENT_NAME}, a registered candidate of the B.Tech program under the Department "
            f"of {DEPARTMENT}, {INSTITUTE}, declare that this report titled \"{PROJECT_TITLE}\" is "
            "my original work. The project has not been submitted to any other institute or "
            "university for a similar award. Any external material used for understanding concepts "
            "has been referenced properly.",
        ),
        p(
            "I hereby transfer the exclusive copyright for this project report to NIT Patna while "
            "reserving the right to use parts of the work for academic learning, future project "
            "development, presentations, and interviews with proper acknowledgement.",
        ),
        Spacer(1, 1.0 * inch),
        p("Signature: __________________________"),
        p("Date: _______________________________"),
        PageBreak(),
        p("ACKNOWLEDGEMENT", "ChapterTitle"),
        p(
            f"I would like to express my sincere gratitude to the Department of {DEPARTMENT}, "
            f"{INSTITUTE}, for providing me the opportunity to complete this internship report. "
            f"I am thankful to {COMPANY} for the project exposure and for helping me understand "
            "how software systems can support real-world hiring and recruitment workflows.",
        ),
        p(
            "This project has been a valuable learning experience. It helped me connect classroom "
            "knowledge with industry-level implementation involving web development, APIs, vector "
            "databases, automation, and retrieval-augmented systems.",
        ),
        PageBreak(),
        p("ABSTRACT", "ChapterTitle"),
        p(
            "Recruitment is a critical activity for every company, but shortlisting suitable "
            "candidates from a large number of resumes can be time-consuming and inconsistent. "
            "Companies often have changing requirements, historical growth plans, technology "
            "preferences, and department-specific needs. A useful recruitment system should be "
            "able to store both company requirement documents and candidate resumes, compare them "
            "automatically, and recommend ideal matches with clear reasoning.",
        ),
        p(
            f"This project, \"{PROJECT_TITLE}\", is a web-based system developed using Streamlit, "
            "FastAPI, Python, Google Apps Script, and Pinecone. Companies can upload their "
            "requirement documents, establishment details, growth information, technology stack, "
            "and hiring needs. Candidates can upload resumes. Both data types remain active for "
            "approximately six months. The system converts the text into vector representations "
            "and stores them in Pinecone as a vector database.",
        ),
        p(
            "The project follows a retrieval-augmented generation style workflow. When a new "
            "requirement is entered, the system retrieves relevant company context, augments the "
            "requirement, searches active candidate resumes, calculates match scores, and labels "
            "candidate potential as Ideal Match, Strong Potential, Moderate Potential, or Low Match. "
            "Google Apps Script is used for automatic intake and score calculation through Google "
            "Forms and Google Sheets.",
        ),
        p(
            "The result is a practical recruitment support system that helps companies identify "
            "suitable candidates faster and with better explanation."
        ),
        PageBreak(),
    ]


def lists_and_toc():
    toc = [
        ["Certificate", "1"],
        ["Declaration and Copyright Transfer", "3"],
        ["Acknowledgement", "4"],
        ["Abstract", "5"],
        ["Chapter 1: Introduction", "8"],
        ["Chapter 2: Literature Review", "10"],
        ["Chapter 3: Problem Statement", "12"],
        ["Chapter 4: Technology Overview", "13"],
        ["Chapter 5: System Design", "16"],
        ["Chapter 6: Data Storage and Vector Database", "18"],
        ["Chapter 7: RAG Workflow", "20"],
        ["Chapter 8: Apps Script Automation", "22"],
        ["Chapter 9: Implementation", "24"],
        ["Chapter 10: Results and Testing", "26"],
        ["Chapter 11: User Interface Description", "28"],
        ["Chapter 12: API and Automation Design", "30"],
        ["Chapter 13: Deployment and User Guide", "32"],
        ["Chapter 14: Security and Data Lifecycle", "34"],
        ["Chapter 15: Conclusion and Future Scope", "36"],
        ["Appendix A: Module Description", "38"],
        ["Appendix B: Sample Workflow", "40"],
        ["Appendix C: API Endpoints", "42"],
        ["References", "44"],
    ]
    table = Table(toc, colWidths=[4.4 * inch, 0.8 * inch])
    table.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (-1, -1), "Times-Roman", 11),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return [
        p("LIST OF FIGURES", "ChapterTitle"),
        p("Fig. 5.1: System architecture of company resume analysis portal"),
        p("Fig. 7.1: RAG workflow using Pinecone vector database"),
        p("Fig. 8.1: Google Apps Script automation flow"),
        p("Fig. 10.1: Candidate match and potential result table"),
        p("Fig. 11.1: Deployment workflow"),
        p("Fig. 12.1: Six-month data lifecycle"),
        PageBreak(),
        p("LIST OF TABLES", "ChapterTitle"),
        p("Table 4.1: Technology stack used in the project"),
        p("Table 6.1: Pinecone metadata design"),
        p("Table 10.1: Candidate potential categories"),
        p("Table 11.1: Deployment configuration"),
        p("Table 12.1: Security and privacy controls"),
        PageBreak(),
        p("TABLE OF CONTENTS", "ChapterTitle"),
        table,
        PageBreak(),
    ]


def chapter(title, paragraphs):
    story = [p(title, "ChapterTitle")]
    for item in paragraphs:
        if isinstance(item, Flowable):
            story.append(item)
        elif isinstance(item, list):
            story.append(bullets(item))
        else:
            story.append(p(item))
    story.append(PageBreak())
    return story


def project_chapters():
    tech_table = Table(
        [
            [cell("Technology", True), cell("Purpose", True)],
            [cell("Python"), cell("Core programming language for backend logic and NLP processing")],
            [cell("Streamlit"), cell("Interactive web dashboard for companies and candidates")],
            [cell("FastAPI"), cell("API backend for automated intake and RAG matching")],
            [cell("Pinecone"), cell("Vector database for storing and searching resume/company vectors")],
            [cell("Google Apps Script"), cell("Automation layer for Google Forms and Sheets")],
            [cell("pypdf"), cell("Text extraction from uploaded PDF documents")],
        ],
        colWidths=[1.6 * inch, 4.0 * inch],
    )
    tech_table.setStyle(default_table_style())

    pinecone_table = Table(
        [
            [cell("Record Type", True), cell("Stored Metadata", True)],
            [
                cell("candidate_resume"),
                cell("Name, email, phone, role, upload date, expiry date, active status, and resume preview"),
            ],
            [
                cell("company_knowledge"),
                cell("Company name, document type, title, details, tags, expiry date, and active status"),
            ],
        ],
        colWidths=[1.7 * inch, 3.9 * inch],
    )
    pinecone_table.setStyle(default_table_style())

    potential_table = Table(
        [
            [cell("Score Range", True), cell("Potential Label", True), cell("Action", True)],
            [cell("80-100"), cell("Ideal Match"), cell("Send to company as high priority")],
            [cell("65-79"), cell("Strong Potential"), cell("Shortlist and review missing skills")],
            [cell("50-64"), cell("Moderate Potential"), cell("Keep as backup or training candidate")],
            [cell("Below 50"), cell("Low Match"), cell("Do not prioritize for current requirement")],
        ],
        colWidths=[1.2 * inch, 1.5 * inch, 2.9 * inch],
    )
    potential_table.setStyle(default_table_style())

    deployment_table = Table(
        [
            [cell("Component", True), cell("Deployment Target", True), cell("Purpose", True)],
            [cell("Streamlit App"), cell("Streamlit Community Cloud"), cell("Recruiter and candidate dashboard")],
            [cell("FastAPI Backend"), cell("Render"), cell("Webhook endpoints for Apps Script automation")],
            [cell("Pinecone Index"), cell("Pinecone Cloud"), cell("Vector search for resumes and company documents")],
            [cell("Google Apps Script"), cell("Google Workspace"), cell("Automatic calculation from Forms and Sheets")],
        ],
        colWidths=[1.6 * inch, 1.7 * inch, 2.4 * inch],
    )
    deployment_table.setStyle(default_table_style())

    security_table = Table(
        [
            [cell("Control", True), cell("Description", True)],
            [cell("Active Status"), cell("Only records marked active are considered during matching.")],
            [cell("Expiry Date"), cell("Candidate and company records expire after about 183 days.")],
            [cell("API Token"), cell("Apps Script requests use an intake token for basic endpoint protection.")],
            [cell("Metadata Filters"), cell("Pinecone queries separate candidate_resume and company_knowledge records.")],
            [cell("Local Fallback"), cell("The project can work locally even when Pinecone keys are unavailable.")],
        ],
        colWidths=[1.8 * inch, 3.9 * inch],
    )
    security_table.setStyle(default_table_style())

    api_table = Table(
        [
            [cell("Endpoint", True), cell("Method", True), cell("Purpose", True)],
            [cell("/health"), cell("GET"), cell("Checks whether the backend service is active.")],
            [cell("/ingest"), cell("POST"), cell("Receives candidate resume data and returns ATS score.")],
            [cell("/company-ingest"), cell("POST"), cell("Receives company requirement documents and stores vectors.")],
            [cell("/rag-match"), cell("POST"), cell("Retrieves context and returns best candidate recommendation.")],
        ],
        colWidths=[1.4 * inch, 0.9 * inch, 3.4 * inch],
    )
    api_table.setStyle(default_table_style())

    return (
        chapter(
            "CHAPTER 1: INTRODUCTION",
            [
                "Recruitment has become increasingly data-driven as companies receive a large number of resumes for every open role. Manual shortlisting is slow and may miss good candidates because recruiters must compare resumes with changing requirements, company growth direction, department needs, and technical expectations.",
                "The proposed project provides a platform where companies can upload their requirement documents and candidates can upload their resumes. The system stores both types of documents for approximately six months and automatically compares active resumes with active company requirements.",
                "The application is designed as a practical hiring support tool. It does not only calculate an ATS-style score; it also identifies candidate potential and provides a recommendation that helps the company decide whether a candidate should be shortlisted.",
                "The project also demonstrates the role of Machine Learning Engineering in building intelligent data-driven applications. Although the project uses lightweight deterministic embeddings for deployment simplicity, the architecture is designed so that transformer-based embeddings can be integrated later without changing the overall workflow.",
                "The system is useful for companies such as Slashmark because internship or hiring programs often collect many applications. A searchable vector database allows the company to revisit applications whenever a suitable requirement appears within the active data period.",
                ["Company documents and candidate resumes are stored in one portal.", "Pinecone is used as the vector database.", "A RAG-style workflow retrieves company context before matching candidates.", "Google Apps Script supports automatic calculation through Google Forms and Sheets."],
            ],
        )
        + chapter(
            "CHAPTER 2: LITERATURE REVIEW",
            [
                "Resume screening systems traditionally use keyword matching and rule-based filters. These systems are simple but often fail to understand the relationship between a company's actual requirement and a candidate's overall profile.",
                "Modern recruitment platforms use natural language processing to extract skills, sections, education, experience, and contact details from resumes. Such methods help recruiters process a large number of applications faster.",
                "Vector databases have recently become important in information retrieval systems. A vector database stores numerical representations of text and allows semantic search. Pinecone is one such managed vector database that can store and retrieve similar documents efficiently.",
                "Retrieval-Augmented Generation (RAG) systems combine retrieval with reasoning. In this project, the system first retrieves relevant company requirement records, then uses this context to rank candidate resumes. This makes the matching process more company-aware.",
                "Automation tools such as Google Apps Script can connect Google Forms and Google Sheets with external APIs. This helps create a low-cost automated recruitment workflow where form submissions can trigger scoring and matching without manual coding by the user.",
                "Several modern applicant tracking systems also use ranking logic based on skills, experience, education, and keywords. However, many of them do not include the company's historical documents and growth context. This project attempts to bridge that gap by storing company documents as searchable knowledge records.",
                "The project is inspired by concepts from information retrieval, natural language processing, and machine learning operations. It shows how separate modules such as data intake, preprocessing, vector storage, API services, and dashboard visualization can work together as a complete product.",
            ],
        )
        + chapter(
            "CHAPTER 3: PROBLEM STATEMENT",
            [
                "Companies often collect resumes through forms, email, and job portals. However, these resumes are not always organized in a way that can be searched when a new requirement arrives.",
                "Another problem is that company requirements change over time. A company may establish new teams, expand into new technologies, or start new projects. Candidate matching should consider these company documents instead of looking only at a single job description.",
                "The main problem addressed in this project is to build a system that stores company documents and candidate resumes, keeps them active for six months, and automatically recommends ideal candidates whenever a company requirement is available.",
                "The system should also be explainable. A company should not only see a candidate name, but should also understand why the candidate is recommended, what potential category the candidate belongs to, and which missing skills should be reviewed before selection.",
                "Therefore, the project combines automated resume analysis, company document storage, Pinecone-based retrieval, RAG-style matching, and Apps Script automation into one workflow.",
            ],
        )
        + chapter(
            "CHAPTER 4: TECHNOLOGY OVERVIEW",
            [
                "The project uses a combination of frontend, backend, document processing, vector search, and automation technologies. Streamlit provides the web interface, FastAPI exposes endpoints for automation, Pinecone stores vectors, and Google Apps Script connects Google Forms and Sheets.",
                tech_table,
                "This combination makes the project suitable for a final-year submission because it demonstrates practical software engineering, cloud deployment, automation, and applied NLP concepts.",
                "Streamlit was selected because it makes it possible to build a functional dashboard quickly using Python. FastAPI was selected because it provides a clean way to expose automation endpoints for Google Apps Script. Pinecone was selected because it is designed for scalable vector search and metadata filtering.",
                "The project has been kept modular. If a future version uses sentence-transformers or OpenAI embeddings, the embedding function can be replaced while keeping the dashboard, API endpoints, and storage format almost unchanged.",
            ],
        )
        + chapter(
            "CHAPTER 5: SYSTEM DESIGN",
            [
                "The system is divided into five main layers: document upload, text extraction, analysis, vector storage, and recommendation. Companies upload requirement documents while candidates upload resumes. The text is extracted and converted into vectors.",
                BoxDiagram(["Company|Docs", "Candidate|Resumes", "Text|Extraction", "Pinecone|Vectors", "RAG Match|Result"]),
                "Fig. 5.1: System architecture of company resume analysis portal",
                "The dashboard contains tabs for resume checking, candidate upload, company document upload, automatic matching, stored data, and Apps Script setup. This gives both companies and administrators a clear workflow.",
                "The candidate upload module accepts PDF resumes or pasted resume text. The company document module accepts requirement PDFs or pasted requirement details. The automatic matching module combines both sources and produces a shortlist.",
                "The design also includes a local fallback. If Pinecone credentials are not configured, the application uses deterministic local vectors and JSON storage. This makes the project easy to demonstrate in offline or limited-access environments.",
            ],
        )
        + chapter(
            "CHAPTER 6: DATA STORAGE AND VECTOR DATABASE",
            [
                "The project stores candidate resumes and company documents as active records for approximately 183 days, which is treated as six months. Expired records are purged automatically when the app runs.",
                "Pinecone stores two kinds of vectors. Candidate resume vectors are tagged as candidate_resume. Company document vectors are tagged as company_knowledge. Metadata is stored with each vector to support filtering and retrieval.",
                pinecone_table,
                "The use of metadata allows the app to search only active candidate resumes when ranking candidates and search only company knowledge when retrieving company context.",
                "Each candidate record contains fields such as candidate ID, name, email, phone, role applied, resume text, upload date, expiry date, latest score, and status. Each company record contains company name, record type, title, date or period, details, tags, expiry date, and status.",
                "The six-month active period is important because companies may not want to keep old candidate profiles indefinitely. At the same time, six months is long enough for companies to reuse candidate data when new requirements arrive.",
            ],
        )
        + chapter(
            "CHAPTER 7: RAG WORKFLOW",
            [
                "The retrieval-augmented workflow is the core intelligence of the project. When a new requirement is entered, the system retrieves relevant company documents from Pinecone. These documents may include establishment history, growth records, projects, technology stack, culture, or current hiring requirements.",
                BoxDiagram(["New|Requirement", "Retrieve|Company Context", "Augment|Requirement", "Search|Resumes", "Explain|Recommendation"]),
                "Fig. 7.1: RAG workflow using Pinecone vector database",
                "After retrieval, the requirement is augmented with company context. Candidate resumes are then searched and scored. The final output includes a ranked list of candidates, a match score, potential label, and recommendation reason.",
                "The RAG flow in this project is retrieval-focused and explainable. Instead of generating long free-form text, the system generates a concise recommendation based on retrieved company context and candidate analysis. This makes the output easier for recruiters to trust and verify.",
                "The retrieved company context may include current hiring needs, technical stack, previous project descriptions, or company growth direction. This context improves the matching decision because a candidate may fit not only the immediate requirement but also the long-term direction of the company.",
            ],
        )
        + chapter(
            "CHAPTER 8: APPS SCRIPT AUTOMATION",
            [
                "Google Apps Script is used to automate candidate and company document intake. Candidate form submissions are sent to the FastAPI /ingest endpoint. Company form submissions are sent to the /company-ingest endpoint.",
                "A Google Sheets custom menu named Resume RAG can call the /rag-match endpoint. This allows the sheet to automatically calculate the best candidate, potential category, match score, and recommendation for a company requirement.",
                BoxDiagram(["Google|Form", "Apps|Script", "FastAPI|Endpoint", "Pinecone|Storage", "Sheet|Result"]),
                "Fig. 8.1: Google Apps Script automation flow",
                ["Candidate forms calculate ATS score automatically.", "Company forms store requirement documents automatically.", "Google Sheets can trigger RAG matching.", "Results are written back to the sheet for company review."],
                "The Apps Script menu gives non-technical users a simple way to trigger matching. A recruiter can paste a requirement in Google Sheets, click the custom menu, and receive the best candidate details directly in the sheet.",
                "This automation is useful because many internship and recruitment programs already use Google Forms. The project adds intelligence to that existing workflow without forcing the company to change its data collection method.",
            ],
        )
        + chapter(
            "CHAPTER 9: IMPLEMENTATION",
            [
                "The Streamlit application is implemented in app.py. The resume analysis logic is implemented in resume_analyzer.py. Candidate storage and company document storage are handled by candidate_store.py and company_store.py.",
                "The vector database and RAG matching functions are implemented in vector_store.py. The FastAPI backend is implemented in api.py. The Google Apps Script automation code is stored in apps_script/Code.gs.",
                "The app extracts text from PDF files using pypdf. It detects sections such as Education, Experience, Projects, Skills, Certifications, and Contact. It also detects technical skills such as Python, SQL, Streamlit, machine learning, Git, and communication.",
                "The matching score combines ATS-style analysis with vector similarity. Candidate potential is labeled as Ideal Match, Strong Potential, Moderate Potential, or Low Match.",
                "The implementation follows a clean modular structure. The resume analyzer is responsible for text analysis, the candidate store handles active resume records, the company store handles active company documents, and the vector store handles Pinecone operations and RAG matching.",
                "The FastAPI backend exposes three major endpoints: /ingest for candidate resumes, /company-ingest for company documents, and /rag-match for automatic ideal-match calculation.",
                "The Streamlit UI provides a direct manual workflow, while Apps Script provides the automated workflow. This means the same backend logic can serve both dashboard users and Google Sheets users.",
            ],
        )
        + chapter(
            "CHAPTER 10: RESULTS AND TESTING",
            [
                "The system was tested with sample company requirements and candidate resumes. The application successfully stored both company and candidate records, retrieved relevant context, and generated candidate recommendations.",
                potential_table,
                "Fig. 10.1: Candidate match and potential result table",
                "The application also passed Python syntax checks and local Streamlit execution checks. The project has been pushed to GitHub and configured for Streamlit Cloud and Render deployment.",
                "The output generated by the system is understandable for recruiters because it provides not only a score but also a reason for the recommendation.",
                "Testing was performed for PDF generation, Python syntax, report generation, candidate ranking, local RAG matching, and Streamlit server startup. The local matching test confirmed that a candidate can be classified into a potential category and that the recommendation text is generated correctly.",
                "A key result of the project is that it can work in two modes. In production mode, Pinecone is used as the vector database. In demonstration mode, local vector ranking is used so the project remains functional without external API keys.",
            ],
        )
        + chapter(
            "CHAPTER 11: USER INTERFACE DESCRIPTION",
            [
                "The user interface is built using Streamlit and is divided into multiple tabs so that different users can perform different tasks without confusion. The Resume Check tab is used for individual resume analysis. It accepts a PDF resume and a job description, then displays ATS score, semantic match, keyword match, detected sections, strengths, weaknesses, and suggestions.",
                "The Candidate Upload tab is designed for candidate intake. A candidate or HR user can enter candidate name, email, phone number, role applied, and upload a resume PDF. The system extracts the resume text and stores the candidate as an active record for six months.",
                "The Company Documents tab is used by a company to upload requirement documents or paste company details. These details can include technical needs, hiring requirements, growth plans, company establishment details, department needs, or project descriptions.",
                "The Auto Match tab is the main recommendation interface. It accepts a new company requirement and retrieves relevant company context. It then ranks active candidates and displays match score, potential label, recommendation, missing skills, and candidate contact details.",
                "The Stored Data tab shows active candidate records and active company documents. This helps recruiters verify what data is currently available for matching. The Apps Script Setup tab explains how to connect Google Forms and Google Sheets with the FastAPI backend.",
                ["The UI is simple enough for non-technical users.", "Each tab maps to a real recruitment workflow.", "The dashboard can run locally or on Streamlit Cloud.", "Shortlists can be exported as CSV for company use."],
            ],
        )
        + chapter(
            "CHAPTER 12: API AND AUTOMATION DESIGN",
            [
                "The FastAPI backend provides automation endpoints so that the project can work beyond the Streamlit dashboard. This is important because companies often collect resumes and requirements through forms. The API allows Google Apps Script to send form data directly to the project backend.",
                api_table,
                "The /ingest endpoint accepts candidate information, resume text, or resume PDF in base64 format. It extracts text, analyzes the resume, stores the candidate record, syncs the vector to Pinecone, and returns candidate ID, ATS score, expiry date, and sync status.",
                "The /company-ingest endpoint accepts company document information. It can receive company details as text or a company requirement PDF in base64 format. It stores the company record, syncs it to Pinecone, and returns record ID and active-until date.",
                "The /rag-match endpoint accepts a requirement and returns a RAG-style recommendation. It retrieves relevant company context, augments the requirement, ranks candidates, and returns the best candidate, potential label, match score, recommendation text, and retrieved evidence.",
                "This API design separates the user interface from automation. The same core logic can be used by Streamlit, Google Sheets, or future mobile/web clients.",
            ],
        )
        + chapter(
            "CHAPTER 13: DEPLOYMENT AND USER GUIDE",
            [
                "The project is deployment-ready using GitHub, Streamlit Community Cloud, Render, and Pinecone. The Streamlit dashboard can be deployed as the main user-facing application, while the FastAPI backend can be deployed separately for Apps Script automation.",
                deployment_table,
                BoxDiagram(["GitHub|Repository", "Streamlit|Dashboard", "Render|API", "Pinecone|Vectors", "Google Sheets|Automation"]),
                "Fig. 11.1: Deployment workflow",
                "To use the system, a company first uploads requirement documents or pastes requirement details. Candidates then upload resumes. The recruiter can open the Auto Match tab, enter a requirement, and view ranked candidates. If Apps Script is configured, the same process can be triggered directly from Google Sheets.",
                "The GitHub repository contains the application code, deployment files, documentation, Apps Script code, and the generated report. This makes the project easy to share, review, and redeploy.",
                "For Streamlit Cloud deployment, the repository, branch, and main file path are selected. In this project, the main file path is app.py. For Render deployment, the render.yaml file defines two services: one for the Streamlit dashboard and one for the FastAPI backend.",
                "The user should configure Pinecone environment variables in the deployment platform. These include PINECONE_API_KEY, PINECONE_INDEX_NAME, PINECONE_CLOUD, and PINECONE_REGION. The INTAKE_TOKEN variable is used by Apps Script to call protected API endpoints.",
            ],
        )
        + chapter(
            "CHAPTER 14: SECURITY AND DATA LIFECYCLE",
            [
                "Because the system handles resumes and company documents, data lifecycle and basic security controls are important. This project implements an active period of approximately six months for both candidate and company records.",
                security_table,
                BoxDiagram(["Upload|Record", "Store|Vector", "Active|183 Days", "Match|Only Active", "Purge|Expired"]),
                "Fig. 12.1: Six-month data lifecycle",
                "The API uses an intake token to protect automated endpoints. Pinecone metadata filters ensure that candidate resumes and company knowledge records are queried separately. This prevents company documents from appearing as candidates and keeps the retrieval process controlled.",
                "A production-ready version should add authentication, role-based access, encrypted storage, audit logs, and explicit consent from candidates before storing resumes.",
                "The six-month active period is implemented through expiry dates. When the app runs, expired candidate and company records are removed from local active storage. Pinecone metadata also includes active status and expiry date so that retrieval can focus on valid records.",
                "The project avoids storing secret keys in the repository. Streamlit secrets or deployment environment variables should be used for Pinecone keys and intake tokens. This is important because API keys in public repositories can be misused.",
            ],
        )
        + chapter(
            "CHAPTER 15: CONCLUSION AND FUTURE SCOPE",
            [
                "The project successfully implements a company resume analysis and ideal match finder system. It allows companies to upload requirements and candidates to upload resumes. Both data types are stored for six months and can be searched using Pinecone.",
                "The RAG workflow improves matching because the system considers company context before ranking candidates. Apps Script automation makes the system useful for form-based real-world workflows.",
                "Future improvements can include transformer-based embeddings, email notifications, PDF report export, interview scheduling, admin login, analytics dashboards, and integration with job portals.",
                "The current project demonstrates a strong foundation for an intelligent recruitment system. With improved embeddings and authentication, it can be expanded into a production-grade company hiring assistant.",
            ],
        )
        + chapter(
            "APPENDIX A: MODULE DESCRIPTION",
            [
                "app.py: This file contains the Streamlit dashboard. It provides tabs for resume checking, candidate upload, company document upload, automatic matching, stored data, and Apps Script setup.",
                "resume_analyzer.py: This file contains the logic for extracting resume text, detecting sections, identifying skills, calculating keyword overlap, and generating ATS-style feedback.",
                "candidate_store.py: This file manages candidate records, including candidate ID, contact details, resume text, upload date, expiry date, latest score, and active status.",
                "company_store.py: This file manages company records such as establishment details, growth history, department requirements, project descriptions, and uploaded requirement documents.",
                "vector_store.py: This file contains the vector embedding function, Pinecone upsert functions, local fallback ranking, company context retrieval, and RAG match report generation.",
                "api.py: This file contains FastAPI endpoints for candidate ingestion, company document ingestion, and RAG matching. These endpoints are used by Apps Script automation.",
                "apps_script/Code.gs: This file contains Google Apps Script code for sending Google Form submissions to the API and writing automatic calculations back to Google Sheets.",
            ],
        )
        + chapter(
            "APPENDIX B: SAMPLE WORKFLOW",
            [
                "Step 1: A company uploads a requirement document mentioning that it needs a Python, SQL, and Streamlit developer for a dashboard project.",
                "Step 2: Candidate resumes are uploaded through the dashboard or Google Form. Each candidate record is stored with an expiry date six months from the upload date.",
                "Step 3: The system converts both company documents and resumes into vector representations and stores them in Pinecone with metadata.",
                "Step 4: When the recruiter enters a requirement, the system retrieves relevant company records from Pinecone and augments the requirement with this context.",
                "Step 5: Active candidate resumes are retrieved and scored. The system generates a ranked table with match score, ATS score, semantic match, missing skills, potential label, and recommendation.",
                "Step 6: The recruiter downloads the shortlist CSV or uses the Google Sheets automation result to contact suitable candidates.",
            ],
        )
        + chapter(
            "APPENDIX C: API ENDPOINTS",
            [
                "GET /health: This endpoint returns a simple status response and is used to verify that the backend is running.",
                "POST /ingest: This endpoint receives candidate information. It supports resume text and base64 PDF input. It returns candidate ID, ATS score, expiry date, and Pinecone sync status.",
                "POST /company-ingest: This endpoint receives company requirement or knowledge records. It supports text details and base64 PDF input. It returns company record ID, expiry date, and Pinecone sync status.",
                "POST /rag-match: This endpoint performs the RAG matching workflow. It retrieves company context, ranks candidate resumes, and returns the best candidate with potential label and recommendation.",
                "These endpoints make the project extensible because future clients can call the same backend without rewriting the core matching logic.",
            ],
        )
    )


def references():
    return [
        p("REFERENCES", "ChapterTitle"),
        p("1. Streamlit Documentation, https://docs.streamlit.io/"),
        p("2. FastAPI Documentation, https://fastapi.tiangolo.com/"),
        p("3. Pinecone Documentation, https://docs.pinecone.io/"),
        p("4. Google Apps Script Documentation, https://developers.google.com/apps-script/"),
        p("5. Python pypdf Documentation, https://pypdf.readthedocs.io/"),
        p("6. Project Repository: https://github.com/akanksha29122002/company_Resume_analysis"),
    ]


def cell(text, bold=False):
    style = ParagraphStyle(
        name="TableCellBold" if bold else "TableCell",
        parent=styles["BodyText"],
        fontName="Times-Bold" if bold else "Times-Roman",
        fontSize=9.2,
        leading=11.2,
        wordWrap="CJK",
    )
    return Paragraph(text, style)


def default_table_style():
    return TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d9eaf7")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("FONT", (0, 0), (-1, 0), "Times-Bold", 10.5),
            ("FONT", (0, 1), (-1, -1), "Times-Roman", 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )


def cover_table_style(header_color):
    return TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), header_color),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONT", (0, 0), (-1, 0), "Times-Bold", 8),
            ("FONT", (0, 1), (-1, -1), "Times-Roman", 7.8),
            ("GRID", (0, 0), (-1, -1), 0.45, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("ALIGN", (2, 1), (2, -1), "CENTER"),
        ]
    )


def build():
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=0.85 * inch,
        leftMargin=0.85 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title=PROJECT_TITLE,
        author=STUDENT_NAME,
    )
    story = []
    story.extend(cover_page())
    story.extend(certificate_pages())
    story.extend(prelim_pages())
    story.extend(lists_and_toc())
    story.extend(project_chapters())
    story.extend(references())
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(OUTPUT.resolve())


if __name__ == "__main__":
    build()
