import requests
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px

# Streamlit App Title with Sidebar Menu
st.set_page_config(page_title="Job Scraping Tool", layout="wide")
st.markdown("""
    <style>
    .main {background-color: #f0f2f6;}
    .stButton > button {background-color: #4CAF50; color: white; padding: 10px 24px; border-radius: 10px;}
    .stSidebar {background-color: #dfe6e9; padding: 20px; border-radius: 10px;}
    .header {text-align: center; font-size: 36px; color: #4CAF50; font-weight: bold; margin-bottom: 20px;}
    .vector-img {display: flex; justify-content: center; margin-bottom: 30px;}
    </style>
""", unsafe_allow_html=True)

# Sidebar Menu with Option Menu
with st.sidebar:
    option = option_menu(
        menu_title="Menu",
        options=["Job Search", "About", "Visualize Trends"],
        icons=["search", "info-circle", "bar-chart"],
        menu_icon="cast",
        default_index=0
    )

# Function to Fetch Jobs from API
def fetch_jobs(job_title, location):
    api_url = "https://serpapi.com/search"
    api_key = "454f98f75cbd9171970dd5c51370485c61c301c4ca2c86ef27cf0134cccc92a0"  # Replace with your actual API key
    params = {
        "engine": "google_jobs",
        "q": f"{job_title} in {location}",
        "api_key": api_key
    }

    response = requests.get(api_url, params=params)

    if response.status_code != 200:
        st.error(f"Failed to retrieve data. Status Code: {response.status_code}. Please try again!")
        return []

    data = response.json()
    jobs = []

    if "jobs_results" in data:
        for job in data["jobs_results"]:
            jobs.append({
                "Job Title": job.get("title", "N/A"),
                "Company": job.get("company_name", "N/A"),
                "Location": job.get("location", "N/A"),
                "Posted": job.get("detected_extensions", {}).get("posted_at", "N/A")
            })
    else:
        st.warning("No jobs found. Try different keywords or location.")

    return jobs

# Main Page Content
if option == "Job Search":
    st.markdown("<div class='header'>Job Scraping Tool with API</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='vector-img'>
        <img src="https://cdn-icons-png.flaticon.com/512/2991/2991145.png" width="150">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("Search for jobs using Google Jobs API")

    job_options = ["Data Analyst", "Python Developer", "Software Developer", "SQL Developer", "Data Scientist"]
    location_options = ["Pune", "Mumbai", "Hyderabad", "India", "Noida", "Delhi", "Gurugram", "Bangalore", "Kolkata"]

    selected_jobs = st.multiselect("Select Job Titles", job_options, default=job_options[:2])
    selected_locations = st.multiselect("Select Locations", location_options, default=location_options[:2])

    if st.button("Start Scraping"):
        st.info("Fetching jobs... Please wait")
        all_jobs = []

        for job in selected_jobs:
            for loc in selected_locations:
                jobs = fetch_jobs(job, loc)
                all_jobs.extend(jobs)

        if all_jobs:
            df = pd.DataFrame(all_jobs)
            st.success(f"Fetching Completed! Found {len(df)} jobs.")
            st.dataframe(df)

            # Download CSV Button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="job_results.csv",
                mime='text/csv'
            )
        else:
            st.warning("No jobs found. Try different keywords or locations.")

elif option == "Visualize Trends":
    st.title("Job Trends Visualization")
    st.markdown("Explore job trends from the fetched data.")
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        
        # Bar Chart for Job Counts by Company
        if "Company" in df.columns:
            fig = px.bar(df, x="Company", title="Number of Jobs per Company")
            st.plotly_chart(fig)
        
        # Pie Chart for Location Distribution
        if "Location" in df.columns:
            fig_pie = px.pie(df, names="Location", title="Jobs by Location")
            st.plotly_chart(fig_pie)

elif option == "About":
    st.title("About the Project")
    st.markdown("""
    This tool uses **Google Jobs API** via **SerpApi** to fetch job listings based on user input.
    - Developed using **Streamlit**
    - CSV Download Option
    - Modern UI/UX Design
    - Vector Images for Better UI Experience
    - Interactive Data Visualizations using Plotly
    - Multi-location and multi-job title search
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/2991/2991145.png", width=200)