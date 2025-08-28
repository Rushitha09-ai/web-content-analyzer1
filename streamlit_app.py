import streamlit as st
import requests
import json
import io
from PIL import Image

st.set_page_config(
    page_title="Web Content Analyzer",
    page_icon="🌐",
    layout="wide"
)

def main():
    st.title("🌐 Web Content Analyzer")
    st.write("Analyze web content with AI-powered insights")

    # Input section
    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            url = st.text_input("Enter URL to analyze:", placeholder="https://example.com")
        with col2:
            analyze_button = st.button("Analyze URL", type="primary")

    # Batch analysis section
    with st.expander("Batch Analysis"):
        urls = st.text_area(
            "Enter multiple URLs (one per line):",
            placeholder="https://example1.com\nhttps://example2.com"
        )
        batch_analyze = st.button("Analyze All URLs")

    # Process single URL
    if analyze_button and url:
        with st.spinner("Analyzing URL..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8001/analyze",
                    json={"url": url}
                )
                if response.status_code == 200:
                    result = response.json()
                    display_analysis(result)
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Process batch URLs
    if batch_analyze and urls:
        url_list = [u.strip() for u in urls.split("\n") if u.strip()]
        if url_list:
            with st.spinner(f"Analyzing {len(url_list)} URLs..."):
                for url in url_list:
                    try:
                        response = requests.post(
                            "http://127.0.0.1:8001/analyze",
                            json={"url": url}
                        )
                        if response.status_code == 200:
                            result = response.json()
                            with st.expander(f"Analysis for {url}"):
                                display_analysis(result)
                        else:
                            st.error(f"Error analyzing {url}: {response.text}")
                    except Exception as e:
                        st.error(f"Error analyzing {url}: {str(e)}")

def display_analysis(result):
    """Display the analysis results in a structured format"""
    if result.get("status") == "success":
        # Content section
        st.subheader("📄 Content Analysis")
        content = result.get("content", {})
        st.write(f"**Title:** {content.get('title', 'N/A')}")
        
        # Analysis section
        st.subheader("🔍 AI Analysis")
        analysis = result.get("analysis", {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Summary:**")
            st.write(analysis.get("summary", "N/A"))
            
            st.write("**Sentiment:**")
            sentiment = analysis.get("sentiment", "neutral")
            sentiment_color = {
                "positive": "green",
                "negative": "red",
                "neutral": "gray"
            }.get(sentiment.lower(), "gray")
            st.markdown(f"<span style='color: {sentiment_color}'>{sentiment}</span>", unsafe_allow_html=True)
            
        with col2:
            st.write("**Confidence Score:**")
            confidence = analysis.get("confidence_score", 0)
            st.progress(confidence)
            
            st.write("**Key Points:**")
            for point in analysis.get("key_points", []):
                st.markdown(f"• {point}")
        
        # Export options
        st.subheader("📥 Export Options")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Export as PDF"):
                try:
                    pdf_response = requests.post(
                        "http://127.0.0.1:8001/export-pdf",
                        json=result
                    )
                    if pdf_response.status_code == 200:
                        # Create download button for PDF
                        st.download_button(
                            label="Download PDF",
                            data=pdf_response.content,
                            file_name="analysis_report.pdf",
                            mime="application/pdf"
                        )
                except Exception as e:
                    st.error(f"Error exporting PDF: {str(e)}")
        
        with col2:
            # Export as JSON
            st.download_button(
                label="Export as JSON",
                data=json.dumps(result, indent=2),
                file_name="analysis_report.json",
                mime="application/json"
            )
    else:
        st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
