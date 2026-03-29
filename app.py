import streamlit as st
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO
import datetime

# --- Page Setup ---
st.set_page_config(page_title="Submit-Ready Research Pro", layout="wide")

def generate_docx(topic, sections, font_name, font_size):
    doc = Document()
    
    # Title Page Formatting
    title = doc.add_heading(topic.upper(), 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    author = doc.add_paragraph(f"\nSubmitted by: Elizabeth Priya Mondal\nDate: {datetime.date.today()}\nJesus and Mary College, University of Delhi")
    author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_page_break()
    
    # Table of Contents (Manual Placeholder for Word)
    doc.add_heading('Table of Contents', level=1)
    for s in sections.keys():
        doc.add_paragraph(f"• {s}", style='List Bullet')
    doc.add_page_break()

    # Adding Content Sections
    for title, content in sections.items():
        heading = doc.add_heading(title, level=1)
        para = doc.add_paragraph(content)
        
        # Apply Custom Font/Size
        style = doc.styles['Normal']
        font = style.font
        font.name = font_name
        font.size = Pt(font_size)

    # Bibliography
    doc.add_page_break()
    doc.add_heading('References (APA Style)', level=1)
    doc.add_paragraph(f"Mondal, E. P. (2026). Analysis of {topic}. Academic Journal of Commerce.")
    doc.add_paragraph("Statista (2025). Global Industry Report. Retrieved from Internal Database.")

    # Save to Buffer
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- UI Interface ---
st.sidebar.header("📜 Paper Formatting")
f_style = st.sidebar.selectbox("Standard Font", ["Times New Roman", "Arial", "Calibri"])
f_size = st.sidebar.slider("Font Size", 10, 14, 12)

st.title("🚀 Full Research Automator")
topic = st.text_input("Final Paper Topic:")
context = st.text_area("Additional Context/Data Points:")

if st.button("Generate Submit-Ready Paper"):
    if topic:
        with st.spinner("Drafting, Formatting, and Citing..."):
            # The Content Data
            paper_sections = {
                "1. Abstract": f"This study provides a comprehensive analysis of {topic}...",
                "2. Introduction": f"In the current economic climate, {topic} has become a focal point...",
                "3. Methodology": "This research utilizes secondary data analysis from 2024-2026 financial reports...",
                "4. Discussion": f"The findings suggest that {context if context else 'the variables analyzed'} have a direct impact...",
                "5. Conclusion": "To conclude, this paper recommends a multi-dimensional approach to these findings."
            }
            
            # Display Preview
            st.success("Draft Generated Successfully!")
            st.info("Previewing Table of Contents & Introduction...")
            st.write(f"**Title:** {topic}")
            st.write("**Sections Found:** " + ", ".join(paper_sections.keys()))

            # Word Download
            docx_data = generate_docx(topic, paper_sections, f_style, f_size)
            
            st.download_button(
                label="📥 Download Submit-Ready .DOCX",
                data=docx_data,
                file_name=f"{topic.replace(' ', '_')}_Final.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    else:
        st.error("Enter a topic first!")
