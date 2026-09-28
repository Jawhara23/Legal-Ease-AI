import os
import sys
import requests
import streamlit as st

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from dotenv import load_dotenv
from utils.formatters import format_docx, format_pdf

load_dotenv()

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)

st.title("LegalEase")
st.subheader("AI-Powered Legal Document Generator")

st.markdown("---")

document_type = st.text_input(
    "Document Type",
    placeholder="Example: NDA, Lease Agreement, Employment Contract"
)

parties = st.text_area(
    "Parties Involved",
    placeholder="Example: John Doe (Employee), ABC Company (Employer)"
)

terms = st.text_area(
    "Terms & Conditions",
    placeholder="Use semicolons between terms"
)

dates = st.text_input(
    "Effective Date",
    placeholder="Example: 26 September 2026"
)

if st.button("Generate Document", type="primary"):

    if not document_type or not parties or not terms or not dates:
        st.warning("Please fill in all the fields.")

    else:

        with st.spinner("Generating your legal document..."):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json={
                        "document_type": document_type,
                        "parties": parties,
                        "terms": terms,
                        "dates": dates
                    },
                    timeout=120
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success(
                        "Document generated successfully!"
                    )

                    generated_text = data["generated_text"]

                    st.session_state["document"] = generated_text
                    st.session_state["document_type"] = document_type
                    st.session_state["terms"] = terms

                else:

                    st.error(
                        f"Backend Error: {response.text}"
                    )

            except requests.exceptions.RequestException as error:

                st.error(
                    f"Could not connect to backend: {error}"
                )


if "document" in st.session_state:

    st.markdown("---")

    st.subheader("Edit Your Document")

    edited_document = st.text_area(
        "Document Preview",
        value=st.session_state["document"],
        height=600
    )

    st.session_state["document"] = edited_document

    st.subheader("Download Document")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.download_button(
            "Download TXT",
            data=edited_document,
            file_name="legal_document.txt",
            mime="text/plain"
        )

    with col2:

        try:

            docx_file = format_docx(
                edited_document,
                st.session_state["document_type"],
                st.session_state["terms"]
            )

            st.download_button(
                "Download DOCX",
                data=docx_file,
                file_name="legal_document.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        except Exception as error:

            st.error(f"DOCX Error: {error}")

    with col3:

        try:

            pdf_file = format_pdf(
                edited_document,
                st.session_state["document_type"],
                st.session_state["terms"]
            )

            st.download_button(
                "Download PDF",
                data=pdf_file,
                file_name="legal_document.pdf",
                mime="application/pdf"
            )

        except Exception as error:

            st.error(f"PDF Error: {error}")          