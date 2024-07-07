import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import base64

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(resume_text, jd_text):
    input_prompt = f"""
    Hey Act Like a skilled or very experienced ATS(Application Tracking System)
    with a deep understanding of tech field, software engineering, data science, data analyst,
    and big data engineer. Your task is to evaluate the resume based on the given job description.
    You must consider the job market is very competitive and you should provide
    best assistance for improving the resumes. Assign the percentage Matching based
    on Jd and
    the missing keywords with high accuracy
    resume:{resume_text}
    description:{jd_text}

    I want the response in one single string having the structure
    {{"JD Match":"%","Profile Summary":"","Scoring Breakdown":{{"Projects":"%","Skills":"%","Education":"%"}},"Skills Matched":"%","MissingSkills":[], "MissingKeywords": []}}  """

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input_prompt)
        return response.text
    except Exception as e:
        st.error(f"Error fetching response from API: {str(e)}")
        return None


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


def display_resume_pdf(file_bytes):
    base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="900" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)


def display_scoring_breakdown(breakdown):
    st.markdown("<h2 style='color: yellow;'>Scoring Breakdown</h2>",
                unsafe_allow_html=True)
    if "Projects" in breakdown:
        st.write(
            f"<p>Projects: {breakdown['Projects']} - Score based on relevance and depth of project experiences.</p>")
    else:
        st.write("<p>Projects: N/A</p>")

    if "Skills" in breakdown:
        st.write(
            f"<p>Skills: {breakdown['Skills']} - Score based on matching technical skills with job requirements.</p>")
    else:
        st.write("<p>Skills: N/A</p>")

    if "Education" in breakdown:
        st.write(
            f"<p>Education: {breakdown['Education']} - Score based on relevant education background.</p>")
    else:
        st.write("<p>Education: N/A</p>")


def display_formatting_tips():
    st.markdown("<h2 style='color: yellow;'>Resume Formatting Tips</h2>",
                unsafe_allow_html=True)
    tips = [
        "Use a clean, professional layout with clearly defined sections.",
        "Choose an ATS-friendly font such as Arial, Times New Roman, or Calibri.",
        "Use standard headings like 'Projects', 'Education', 'Skills'.",
        "Avoid using images, graphics, or tables.",
        "Save and upload your resume as a PDF to maintain formatting."
    ]
    for tip in tips:
        st.write(f"- {tip}")

# Function to calculate skills matched percentage and identify missing skills


def calculate_skills_matched(resume_text, jd_text):
    resume_skills = set(resume_text.lower().split())
    jd_skills = set(jd_text.lower().split())
    matched_skills = resume_skills.intersection(jd_skills)
    skills_matched_percentage = (len(matched_skills) / len(jd_skills)) * 100
    return skills_matched_percentage

# Function to generate feedback based on evaluation results


def generate_feedback(resume_text, jd_text, response_data):
    feedback = ""

    # Job Description Match
    feedback += f"<h2 style='color: yellow;'>Job Description Match</h2>"
    feedback += f"<p>**Job Description Match:** {response_data['JD Match']}</p>\n\n"

    # Profile Summary
    feedback += f"**Profile Summary:** {response_data['Profile Summary']}\n\n"

    # Missing Keywords
    if "MissingKeywords" in response_data:
        missing_keywords = response_data["MissingKeywords"]
        feedback += "<h2 style='color: yellow;'>Missing Keywords</h2>\n"
        for keyword in missing_keywords:
            feedback += f"<p>- {keyword}</p>\n"
        feedback += "\n"

    # Scoring Breakdown
    feedback += "<h2 style='color: yellow;'>Scoring Breakdown</h2>\n"
    if "Projects" in response_data["Scoring Breakdown"]:
        feedback += f"<p>- Projects: {response_data['Scoring Breakdown']['Projects']} - Score based on relevance and depth of project experiences.</p>\n"
    if "Skills" in response_data["Scoring Breakdown"]:
        feedback += f"<p>- Skills: {response_data['Scoring Breakdown']['Skills']} - Score based on matching technical skills with job requirements.</p>\n"
    if "Education" in response_data["Scoring Breakdown"]:
        feedback += f"<p>- Education: {response_data['Scoring Breakdown']['Education']} - Score based on relevant education background.</p>\n"
    feedback += "\n"

    # Skills Matched Percentage
    skills_matched_percentage = calculate_skills_matched(
        resume_text, jd_text)
    feedback += f"<h2 style='color: yellow;'>Skills Matched Percentage</h2>\n"
    feedback += f"<p>**Skills Matched Percentage:** {skills_matched_percentage:.2f}% of job description skills matched in the resume.</p>\n\n"

    return feedback


# Streamlit app
st.title("CVInsightForge")
st.markdown("<h1 style='color: yellow;'>Enhance Your Resume with Precision and Insight</h1>",
            unsafe_allow_html=True)
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader(
    "Upload Your Resume", type="pdf", help="Please upload the PDF file")

submit = st.button("Submit")

if submit:
    if uploaded_file and jd:
        # Read the uploaded file as bytes
        file_bytes = uploaded_file.read()

        # Use the bytes for text extraction and display
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(text, jd)

        if response:
            try:
                response_data = json.loads(response)
            except json.JSONDecodeError as e:
                st.error(f"Error decoding JSON response: {str(e)}")
                st.write("Response from API:")
                st.write(response)
            else:
                # Display the resume
                st.subheader(f"Uploaded Resume: {uploaded_file.name}")
                display_resume_pdf(file_bytes)

                # Display evaluation results
                st.subheader("Evaluation Result")
                st.markdown(generate_feedback(
                    text, jd, response_data), unsafe_allow_html=True)

                # Display formatting tips
                display_formatting_tips()
        else:
            st.error(
                "Failed to fetch response from API. Please check your API configuration.")
    else:
        st.error("Please upload a resume and enter a job description.")
