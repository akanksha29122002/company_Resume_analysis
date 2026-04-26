from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import html


SLIDES = [
    ("AI Resume Analyzer", ["Company Knowledge Bank using Streamlit, Apps Script, and Pinecone", "Final Year Project Presentation"]),
    ("Introduction", ["Resume screening is an important recruitment step.", "Companies need a searchable active resume pool.", "Company history and growth should influence hiring decisions."]),
    ("Problem Statement", ["Manual company resume review is slow.", "Recruiters need the best resume whenever a new role arrives.", "Matching should consider establishment, growth, projects, and current direction."]),
    ("Objectives", ["Upload and analyze resume PDFs.", "Receive resumes automatically from Google Forms.", "Maintain candidates as active for 6 months.", "Store company growth details in Pinecone.", "Rank candidates for each company role."]),
    ("System Architecture", ["Google Form sends resume data through Apps Script.", "FastAPI intake stores candidate records.", "Pinecone stores resume vectors.", "Pinecone also stores company knowledge vectors.", "Streamlit dashboard ranks active candidates."]),
    ("Main Modules", ["PDF text extraction", "Skill and section detection", "Candidate database", "Company growth knowledge base", "Apps Script intake", "Pinecone vector search"]),
    ("Pinecone Design", ["candidate_resume records store resume vectors and metadata.", "company_knowledge records store establishment and growth data.", "Role matching uses candidate data and retrieved company documents."]),
    ("RAG Flow", ["Store company documents and resumes as vectors in Pinecone.", "Retrieve relevant company context for a new requirement.", "Augment the requirement with retrieved context.", "Retrieve and rank active candidate resumes.", "Generate an explainable recommendation."]),
    ("Apps Script Automation", ["Candidate form sends resumes to the API.", "Company form sends requirements to the API.", "Google Sheets menu calls /rag-match.", "Sheet receives candidate, potential, score, and recommendation."]),
    ("Scoring Logic", ["Skill match: 30 percent", "Semantic similarity: 25 percent", "Section completeness: 20 percent", "Keyword overlap: 15 percent", "Contact and length quality: 10 percent"]),
    ("User Interface", ["Single resume analyzer", "Company candidate intake", "Company growth timeline", "Active candidate database", "Role matching dashboard", "CSV shortlist export"]),
    ("Results", ["ATS score out of 100", "Strengths and weaknesses", "Missing job skills", "Candidate expiry date", "Company requirement context", "Best-fit role shortlist"]),
    ("Deployment", ["Dashboard deploys on Streamlit Cloud.", "Webhook API deploys on Render.", "Apps Script connects Google Form to API.", "Pinecone is optional with local fallback."]),
    ("Conclusion", ["The project helps students and companies.", "It automates intake, scoring, and retrieval.", "It uses company growth history for better hiring decisions.", "It is deployable and presentation-ready."]),
]


def write_file(zf, name, content):
    zf.writestr(name, content)


def slide_xml(title, bullets):
    bullet_xml = ""
    y = 1800000
    for bullet in bullets:
        bullet_xml += f"""
        <p:sp>
          <p:nvSpPr><p:cNvPr id="{y}" name="Bullet"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
          <p:spPr><a:xfrm><a:off x="850000" y="{y}"/><a:ext cx="7600000" cy="420000"/></a:xfrm></p:spPr>
          <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr lang="en-US" sz="2600"/><a:t>{html.escape(bullet)}</a:t></a:r></a:p></p:txBody>
        </p:sp>"""
        y += 560000
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg><p:bgPr><a:solidFill><a:srgbClr val="F8FAFC"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="Title"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="650000" y="520000"/><a:ext cx="8200000" cy="850000"/></a:xfrm></p:spPr>
        <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr lang="en-US" sz="4200" b="1"><a:solidFill><a:srgbClr val="0F172A"/></a:solidFill></a:rPr><a:t>{html.escape(title)}</a:t></a:r></a:p></p:txBody>
      </p:sp>
      {bullet_xml}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""


def build_pptx(path):
    slide_count = len(SLIDES)
    with ZipFile(path, "w", ZIP_DEFLATED) as zf:
        write_file(zf, "[Content_Types].xml", content_types(slide_count))
        write_file(zf, "_rels/.rels", root_rels())
        write_file(zf, "ppt/presentation.xml", presentation_xml(slide_count))
        write_file(zf, "ppt/_rels/presentation.xml.rels", presentation_rels(slide_count))
        for i, (title, bullets) in enumerate(SLIDES, 1):
            write_file(zf, f"ppt/slides/slide{i}.xml", slide_xml(title, bullets))
            write_file(zf, f"ppt/slides/_rels/slide{i}.xml.rels", "")


def content_types(slide_count):
    overrides = "".join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, slide_count + 1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  {overrides}
</Types>"""


def root_rels():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>"""


def presentation_rels(slide_count):
    rels = "".join(
        f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
        for i in range(1, slide_count + 1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{rels}</Relationships>"""


def presentation_xml(slide_count):
    slide_ids = "".join(f'<p:sldId id="{255+i}" r:id="rId{i}"/>' for i in range(1, slide_count + 1))
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldIdLst>{slide_ids}</p:sldIdLst>
  <p:sldSz cx="10000000" cy="5625000" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>"""


if __name__ == "__main__":
    output = Path("AI_Resume_Analyzer_Presentation.pptx")
    build_pptx(output)
    print(output.resolve())
