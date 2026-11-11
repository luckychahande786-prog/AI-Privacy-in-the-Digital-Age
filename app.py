import streamlit as st
import re

st.set_page_config(
    page_title="AI Privacy Guardian",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 AI Privacy Guardian")
st.subheader("AI Privacy in the Digital Age")

st.write(
    "An educational tool to identify personal information "
    "before sharing text with AI tools."
)

st.info("Your text is checked locally in this app and is not saved.")

st.header("Privacy Risk Checker")

user_text = st.text_area(
    "Enter text to check:",
    placeholder="Type your text here..."
)

if st.button("Check Privacy Risk"):

    if user_text.strip() == "":
        st.warning("Please enter some text first.")

    else:
        risks = []

        patterns = {
            "Email Address": r'[\w\.-]+@[\w\.-]+\.\w+',
            "Phone Number": r'\b\d{10}\b',
            "Aadhaar-like Number": r'\b\d{4}\s?\d{4}\s?\d{4}\b',
            "Credit Card-like Number": r'\b(?:\d[ -]*?){13,16}\b'
        }

        for name, pattern in patterns.items():
            if re.search(pattern, user_text):
                risks.append(name)

        st.header("Privacy Report")

        if risks:
            st.error("Privacy risks detected!")

            for risk in risks:
                st.write("⚠️", risk)

            st.write("Recommendation: Remove sensitive information before sharing.")

        else:
            st.success("No common personal information patterns detected.")

        st.caption(
            "Note: This is a basic educational checker. "
            "It cannot detect every type of personal information."
        )

st.divider()

st.subheader("Privacy Tips")

st.write("1. Never share passwords with AI.")
st.write("2. Avoid sharing bank details.")
st.write("3. Protect your personal information.")
st.write("4. Review AI privacy settings.")

st.caption("Class 12 AI Capstone Project | 2026-27")
