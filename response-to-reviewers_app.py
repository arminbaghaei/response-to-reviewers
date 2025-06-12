import streamlit as st
from docx import Document
from docx.shared import Pt
from io import BytesIO

st.set_page_config(page_title="📝 Response to Reviewers Tool", layout="wide")
st.title("📝 Response to Reviewers Generator")

st.markdown("Fill in the details and generate a response document for your reviewers.")

# Manuscript info
journal_name = st.text_input("Journal's Name")
manuscript_id = st.text_input("Manuscript ID")
manuscript_title = st.text_input("Manuscript Title")

st.markdown("---")

# Initialize session state for reviewers
if "reviewers" not in st.session_state:
    st.session_state.reviewers = [{"id": 1, "comments": [{"comment": "", "response": ""}]}]

def add_reviewer():
    st.session_state.reviewers.append({
        "id": len(st.session_state.reviewers) + 1,
        "comments": [{"comment": "", "response": ""}]
    })

def add_comment(reviewer_index):
    st.session_state.reviewers[reviewer_index]["comments"].append({"comment": "", "response": ""})

# Input sections for reviewers
for i, reviewer in enumerate(st.session_state.reviewers):
    st.subheader(f"Reviewer {reviewer['id']}")
    for j, comment_pair in enumerate(reviewer["comments"]):
        comment = st.text_area(f"Comment {j + 1}", key=f"comment_{i}_{j}")
        response = st.text_area(f"Response {j + 1}", key=f"response_{i}_{j}")
        reviewer["comments"][j]["comment"] = comment
        reviewer["comments"][j]["response"] = response
    st.button("➕ Add another comment", on_click=add_comment, args=(i,), key=f"add_comment_{i}")
    st.markdown("---")

st.button("➕ Add Reviewer", on_click=add_reviewer)

# Generate Word file
def generate_docx():
    doc = Document()
    doc.add_heading(journal_name or "Journal Name", level=1)
    doc.add_paragraph(f"Manuscript ID: {manuscript_id}")
    doc.add_paragraph(f"Manuscript Title: {manuscript_title}")
    doc.add_paragraph(
        "We would like to thank you for your valuable time and insightful comments to improve the quality of this manuscript. "
        "We have now addressed these comments and revised the manuscript thoroughly. Please see our detailed responses and revisions below.\n\nThanks,\nAuthors"
    )

    for reviewer in st.session_state.reviewers:
        doc.add_heading(f"Reviewer {reviewer['id']}", level=2)
        for idx, comment_data in enumerate(reviewer["comments"], 1):
            doc.add_paragraph(f"Comment {idx}:", style='List Number')
            comment_para = doc.add_paragraph(comment_data['comment'])
            comment_para.paragraph_format.left_indent = Pt(20)
            doc.add_paragraph("Response:", style='List Number')
            response_para = doc.add_paragraph(comment_data['response'])
            response_para.paragraph_format.left_indent = Pt(20)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

if st.button("📄 Generate Word File"):
    buffer = generate_docx()
    st.download_button(
        label="📥 Download Response_to_Reviewers.docx",
        data=buffer,
        file_name="Response_to_Reviewers.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
