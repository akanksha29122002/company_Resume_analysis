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
        ["Chapter 11: Conclusion and Future Scope", "28"],
        ["References", "30"],
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
        PageBreak(),
        p("LIST OF TABLES", "ChapterTitle"),
        p("Table 4.1: Technology stack used in the project"),
        p("Table 6.1: Pinecone metadata design"),
        p("Table 10.1: Candidate potential categories"),
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

    return (
        chapter(
            "CHAPTER 1: INTRODUCTION",
            [
                "Recruitment has become increasingly data-driven as companies receive a large number of resumes for every open role. Manual shortlisting is slow and may miss good candidates because recruiters must compare resumes with changing requirements, company growth direction, department needs, and technical expectations.",
                "The proposed project provides a platform where companies can upload their requirement documents and candidates can upload their resumes. The system stores both types of documents for approximately six months and automatically compares active resumes with active company requirements.",
                "The application is designed as a practical hiring support tool. It does not only calculate an ATS-style score; it also identifies candidate potential and provides a recommendation that helps the company decide whether a candidate should be shortlisted.",
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
            ],
        )
        + chapter(
            "CHAPTER 3: PROBLEM STATEMENT",
            [
                "Companies often collect resumes through forms, email, and job portals. However, these resumes are not always organized in a way that can be searched when a new requirement arrives.",
                "Another problem is that company requirements change over time. A company may establish new teams, expand into new technologies, or start new projects. Candidate matching should consider these company documents instead of looking only at a single job description.",
                "The main problem addressed in this project is to build a system that stores company documents and candidate resumes, keeps them active for six months, and automatically recommends ideal candidates whenever a company requirement is available.",
            ],
        )
        + chapter(
            "CHAPTER 4: TECHNOLOGY OVERVIEW",
            [
                "The project uses a combination of frontend, backend, document processing, vector search, and automation technologies. Streamlit provides the web interface, FastAPI exposes endpoints for automation, Pinecone stores vectors, and Google Apps Script connects Google Forms and Sheets.",
                tech_table,
                "This combination makes the project suitable for a final-year submission because it demonstrates practical software engineering, cloud deployment, automation, and applied NLP concepts.",
            ],
        )
        + chapter(
            "CHAPTER 5: SYSTEM DESIGN",
            [
                "The system is divided into five main layers: document upload, text extraction, analysis, vector storage, and recommendation. Companies upload requirement documents while candidates upload resumes. The text is extracted and converted into vectors.",
                BoxDiagram(["Company|Docs", "Candidate|Resumes", "Text|Extraction", "Pinecone|Vectors", "RAG Match|Result"]),
                "Fig. 5.1: System architecture of company resume analysis portal",
                "The dashboard contains tabs for resume checking, candidate upload, company document upload, automatic matching, stored data, and Apps Script setup. This gives both companies and administrators a clear workflow.",
            ],
        )
        + chapter(
            "CHAPTER 6: DATA STORAGE AND VECTOR DATABASE",
            [
                "The project stores candidate resumes and company documents as active records for approximately 183 days, which is treated as six months. Expired records are purged automatically when the app runs.",
                "Pinecone stores two kinds of vectors. Candidate resume vectors are tagged as candidate_resume. Company document vectors are tagged as company_knowledge. Metadata is stored with each vector to support filtering and retrieval.",
                pinecone_table,
                "The use of metadata allows the app to search only active candidate resumes when ranking candidates and search only company knowledge when retrieving company context.",
            ],
        )
        + chapter(
            "CHAPTER 7: RAG WORKFLOW",
            [
                "The retrieval-augmented workflow is the core intelligence of the project. When a new requirement is entered, the system retrieves relevant company documents from Pinecone. These documents may include establishment history, growth records, projects, technology stack, culture, or current hiring requirements.",
                BoxDiagram(["New|Requirement", "Retrieve|Company Context", "Augment|Requirement", "Search|Resumes", "Explain|Recommendation"]),
                "Fig. 7.1: RAG workflow using Pinecone vector database",
                "After retrieval, the requirement is augmented with company context. Candidate resumes are then searched and scored. The final output includes a ranked list of candidates, a match score, potential label, and recommendation reason.",
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
            ],
        )
        + chapter(
            "CHAPTER 9: IMPLEMENTATION",
            [
                "The Streamlit application is implemented in app.py. The resume analysis logic is implemented in resume_analyzer.py. Candidate storage and company document storage are handled by candidate_store.py and company_store.py.",
                "The vector database and RAG matching functions are implemented in vector_store.py. The FastAPI backend is implemented in api.py. The Google Apps Script automation code is stored in apps_script/Code.gs.",
                "The app extracts text from PDF files using pypdf. It detects sections such as Education, Experience, Projects, Skills, Certifications, and Contact. It also detects technical skills such as Python, SQL, Streamlit, machine learning, Git, and communication.",
                "The matching score combines ATS-style analysis with vector similarity. Candidate potential is labeled as Ideal Match, Strong Potential, Moderate Potential, or Low Match.",
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
            ],
        )
        + chapter(
            "CHAPTER 11: CONCLUSION AND FUTURE SCOPE",
            [
                "The project successfully implements a company resume analysis and ideal match finder system. It allows companies to upload requirements and candidates to upload resumes. Both data types are stored for six months and can be searched using Pinecone.",
                "The RAG workflow improves matching because the system considers company context before ranking candidates. Apps Script automation makes the system useful for form-based real-world workflows.",
                "Future improvements can include transformer-based embeddings, email notifications, PDF report export, interview scheduling, admin login, analytics dashboards, and integration with job portals.",
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
