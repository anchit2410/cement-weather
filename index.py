# import streamlit as st
# import requests
# import streamlit.components.v1 as components

# API_BASE_URL = "http://localhost:8000"  # Change this if your FastAPI server is hosted elsewhere

# # Page config
# st.set_page_config(page_title="🌦️ Weather Update Processor", layout="centered")

# # Title
# st.markdown("<h1 style='padding-top: 10px;'>Weather Update Processor</h1>", unsafe_allow_html=True)

# # Health Check (run only once when the app starts)
# if "health_checked" not in st.session_state:
#     with st.spinner("🔄 Checking API health..."):
#         try:
#             health = requests.get(f"{API_BASE_URL}/health")
#             if health.status_code == 200:
#                 st.success("✅ API is healthy and ready!")
#             else:
#                 st.error("❌ API health check failed.")
#         except Exception as e:
#             st.error(f"❌ API not reachable: {e}")
#     st.session_state.health_checked = True

# # Caching sample file download
# @st.cache_data
# def fetch_sample_file():
#     try:
#         response = requests.get(f"{API_BASE_URL}/data/sample-file")
#         if response.status_code == 200:
#             return response.content
#     except Exception:
#         return None

# col1, col2 = st.columns([3.7, 1.4])

# with col1:
#     st.markdown("<h3 style='font-size:17px;'>📥 Download Sample Excel File</h3>", unsafe_allow_html=True)

# with col2:
#     with st.spinner("Fetching sample file..."):
#         sample_file = fetch_sample_file()

#     if sample_file:
#         st.download_button(
#             label="⬇️ Download Sample",
#             data=sample_file,
#             file_name="sample_input.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )
#     else:
#         st.error("⚠️ Could not load sample file.")
 

# # Run Weather Update
# st.markdown("### ⚙️ Process Weather Update")

# # Upload Excel File
# with st.expander("📤 Upload Excel File (Optional)", expanded=False):
#     uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

# # Initialize session state
# for key in ["processing", "processed", "downloaded"]:
#     if key not in st.session_state:
#         st.session_state[key] = False

# # Run update
# if st.button("▶️ Run Weather Update", disabled=st.session_state.processing):
#     st.session_state.processing = True
#     with st.spinner("⏳ Processing... Please wait."):
#         try:
#             if uploaded_file:
#                 files = {
#                     "file": (uploaded_file.name, uploaded_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
#                 }
#                 response = requests.post(f"{API_BASE_URL}/upload/weather-update", files=files)
#             else:
#                 response = requests.post(f"{API_BASE_URL}/upload/weather-update")

#             if response.status_code == 200:
#                 st.success("✅ Weather update processed successfully!")
#                 st.session_state.processed = True
#                 st.session_state.downloaded = False
#             else:
#                 st.error(f"❌ Error: {response.status_code} - {response.text}")
#         except Exception as e:
#             st.error(f"❌ An error occurred: {e}")
#         finally:
#             st.session_state.processing = False

# # Caching output file download
# @st.cache_data
# def fetch_output_file():
#     try:
#         response = requests.get(f"{API_BASE_URL}/data/download")
#         if response.status_code == 200:
#             return response.content
#     except Exception:
#         return None

# # Show download only after processing
# if st.session_state.processed and not st.session_state.downloaded:
#     st.markdown("### 📥 Download Processed Output File")
#     output_file = fetch_output_file()
#     if output_file:
#         st.download_button(
#             label="⬇️ Click to Download Output",
#             data=output_file,
#             file_name="weather-forecast.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )
#         st.session_state.downloaded = True
#     else:
#         st.error("⚠️ Failed to download output file.")

# # Embedded Power BI Report
# st.markdown("## 📊 Embedded Power BI Report")
# powerbi_url = "https://app.powerbi.com/reportEmbed?reportId=c007eeb1-aad4-43fb-b509-30725768d463&autoAuth=true&ctid=04c72f56-1848-46a2-8167-8e5d36510cbc"
# components.html(
#     f"""
#     <iframe title="Power BI Report" width="100%" height="600" 
#     src="{powerbi_url}" frameborder="0" allowFullScreen="true"></iframe>
#     """,
#     height=620,
# )



import streamlit as st
import requests
import streamlit.components.v1 as components

API_BASE_URL = "http://localhost:8000"  # Change this if your FastAPI server is hosted elsewhere




# Page config
st.set_page_config(page_title="🌦️ Weather Update Processor", layout="centered")

#logo
logo_url = "sirius-icon 1.png"  # Replace with your logo URL or local file path
st.logo(logo_url, size="medium", link=None, icon_image=None)


st.markdown("<h1 style='padding-top: 10px;'>Weather Update Processor</h1>", unsafe_allow_html=True)

# Health Check (run only once when the app starts)
if "health_checked" not in st.session_state:
    with st.spinner("🔄 Checking API health..."):
        try:
            health = requests.get(f"{API_BASE_URL}/health")
            if health.status_code == 200:
                st.success("✅ System is healthy and ready!")
            else:
                st.error("❌ System health check failed.")
        except Exception as e:
            st.error(f"❌ Server not reachable: {e}")
    st.session_state.health_checked = True
else :
    st.success("✅ System is healthy and ready!")

@st.cache_data(show_spinner=False)
def fetch_sample_file():
    try:
        response = requests.get(f"{API_BASE_URL}/data/sample-file")
        if response.status_code == 200:
            return response.content
    except Exception:
        return None

col1, col2 = st.columns([3.7, 1.4])
sample_file = fetch_sample_file()
with col1:
    st.markdown("<h3 style='font-size:17px;'>📥 Download Sample Excel File</h3>", unsafe_allow_html=True)

with col2:
    if sample_file:
        st.download_button(
            label="⬇️ Download Sample",
            data=sample_file,
            file_name="sample_input.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("⚠️ Could not load sample file.")
 


# Run Weather Update
st.markdown("<h3 style='font-size:25px;'>⚙️ Process Weather Update</h3>", unsafe_allow_html=True)

# Upload Excel File
with st.expander("📤 Upload Excel File (Optional)", expanded=False):
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])



# Initialize session state
if "processing" not in st.session_state:
    st.session_state.processing = False
if "processed" not in st.session_state:
    st.session_state.processed = False
if "downloaded" not in st.session_state:
    st.session_state.downloaded = False
if "output_file" not in st.session_state:
    st.session_state.output_file = None

# Run Weather Update Button
if st.button("▶️ Run Weather Update", disabled=st.session_state.processing):
    st.session_state.processing = True
    
    with st.spinner("⏳ Processing... Please wait."):
        try:
            if uploaded_file:
                files = {
                    "file": (uploaded_file.name, uploaded_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                }
                response = requests.post(f"{API_BASE_URL}/upload/weather-update", files=files)
            else:
                response = requests.post(f"{API_BASE_URL}/upload/weather-update")

            if response.status_code == 200:
                st.success("✅ Weather update processed successfully!")
                st.session_state.processed = True
                st.session_state.downloaded = False

                # Fetch the file immediately after processing
                file_response = requests.get(f"{API_BASE_URL}/data/download")
                if file_response.status_code == 200:
                    st.session_state.output_file = file_response.content
                else:
                    st.error("⚠️ Failed to fetch output file.")
            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
        finally:
            st.session_state.processing = False

# Show download section only after processing
if st.session_state.processed and st.session_state.output_file:
    st.markdown("### 📥 Download Processed Output File")
    c_1, c_2 = st.columns([4, 2])

    with c_1:
        st.download_button(
            label="📄 Download Output File",
            data=st.session_state.output_file,
            file_name="weather-forecast.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            # disabled=st.session_state.processing  # Disable while processing
        )

    with c_2:
        powerbi_url = "https://app.powerbi.com/reportEmbed?reportId=c007eeb1-aad4-43fb-b509-30725768d463&autoAuth=true&ctid=04c72f56-1848-46a2-8167-8e5d36510cbc"
        # disabled_attr = "disabled" if st.session_state.processing else ""
        st.markdown(
            f"""
            <a href="{powerbi_url}" target="_blank">
            <button style="display: inline-flex;-webkit-box-align: center;align-items: center;-webkit-box-pack: center;justify-content: center;font-weight: 400;padding: 0.25rem 0.75rem;border-radius: 0.5rem;
                min-height: 2.5rem;margin: 0px;line-height: 1.6;text-transform: none;font-size: inherit;font-family: inherit;color: rgb(26 27 29);width: auto;
                cursor: pointer; user-select: none;background-color: rgb(255, 255, 255);border: 1px solid rgba(49, 51, 63, 0.2);">📊 Open Power BI Report
            </button>
            </a>
            """, unsafe_allow_html=True
        )
        
    




