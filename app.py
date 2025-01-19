import streamlit as st
import PyPDF2
import google.generativeai as genai
from io import StringIO
import plotly.graph_objects as go

# Set up Gemini API
genai.configure(api_key="AIzaSyD0dsA5fgIIiISSLSGkFDNz_0caCpwcFnM")  # Replace with your Gemini API key
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("AI-Powered Agreement Risk Analyzer")
st.write("Upload a PDF agreement to analyze risks.")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF agreement", type="pdf")

# Extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Analyze agreement using Gemini API
def analyze_agreement(text):
    prompt = f"""
    Analyze the following legal agreement and identify all risk clauses. 
    Focus on clauses related to financial risks, compliance risks, liability risks, and termination risks.
    Provide a summary of each risk clause in bullet points.

    Agreement Text:
    {text}
    """
    response = model.generate_content(prompt)
    return response.text

# Calculate risk score
def calculate_risk_score(risk_analysis):
    risk_clauses = risk_analysis.split("\n")
    risk_score = 0
    for clause in risk_clauses:
        if "withhold" in clause.lower():
            risk_score += 2  # High severity
        elif "fraud" in clause.lower():
            risk_score += 3  # Very high severity
        else:
            risk_score += 1  # Low severity
    return risk_score

# Create Risk Meter
def create_risk_meter(risk_score):
    if risk_score <= 3:
        risk_level = "Low"
        color = "green"
    elif 4 <= risk_score <= 6:
        risk_level = "Medium"
        color = "orange"
    else:
        risk_level = "High"
        color = "red"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        title={'text': f"Risk Level: {risk_level}"},
        gauge={
            'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 3], 'color': "green"},
                {'range': [4, 6], 'color': "orange"},
                {'range': [7, 10], 'color': "red"}
            ],
        }
    ))
    return fig

# Main logic
if uploaded_file is not None:
    agreement_text = extract_text_from_pdf(uploaded_file)
    # st.write("### Extracted Text")
    # st.write(agreement_text[:1000] + "...")  # Display first 1000 characters for preview

    st.write("### Risk Analysis")
    with st.spinner("Analyzing agreement for risk clauses..."):
        risk_analysis = analyze_agreement(agreement_text)
        st.write(risk_analysis)

        # Calculate risk score
        risk_score = calculate_risk_score(risk_analysis)
        st.write(f"### Overall Risk Score: {risk_score}")

        # Display Risk Meter
        st.write("### Risk Meter")
        risk_meter = create_risk_meter(risk_score)
        st.plotly_chart(risk_meter)