import streamlit as st
import pandas as pd
import joblib
import os

# Path to models directory
model_dir = 'models'

# Load the model, scaler, label encoder, and columns used during training
model = joblib.load(os.path.join(model_dir, 'crime_model.pkl'))
scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
label_encoder = joblib.load(os.path.join(model_dir, 'label_encoder.pkl'))
training_columns = joblib.load(os.path.join(model_dir, 'columns.pkl'))

# Load dataset for reference (assuming the dataset is small enough to load into memory)
df = pd.read_csv('data_set.csv')
df['AREA NAME'] = df['AREA NAME'].astype(str)  # Ensure AREA NAME is string type

# Streamlit app
st.markdown(
    """
    <style>
    .e1f1d6gn0{
        background:#000;
        padding:20px;
        box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
    }
   .st-emotion-cache-1jzia57 h1, .st-emotion-cache-1jzia57 h2, .st-emotion-cache-1jzia57 h3, .st-emotion-cache-1jzia57 h4, .st-emotion-cache-1jzia57 h5, .st-emotion-cache-1jzia57 h6, .st-emotion-cache-1jzia57 span {
    scroll-margin-top: 3.75rem;
    color: #fff;
    margin-left:20px;
    color:#bd0000;
}
        .stApp {
            background-image: url('https://i.ibb.co/1sddw5G/freepicdownloader-com-bloody-handprint-background-large.jpg');
            background-size: cover;
            background-attachment: fixed;
        }
        .main-container {
            background: rgba(255, 255, 255, 0.9);  /* Semi-transparent white */
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin: 20px;
        }
        .stButton>button {
            background-color: #bd0000;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.3s;
            width:100%;
            border:2px solid #bd0000;
            
        }
        .stButton>button:hover {
            background-color: #000;
            color: #fff;
            transform: scale(1.02);
            border:2px solid #fff;
        }
        h1 {
            color: #333;
        }
        label {
            font-size: 1.1em;
            color: #333;
        }
        .css-1f1d6gn {
            padding: 0px;
        }
        .st-emotion-cache-ul70r3 p {
    word-break: break-word;
    font-size: 21px;
}
    </style>
    """,
    unsafe_allow_html=True
)

# st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.title("🚨 Crime Hotspot Prediction 🚨 ")

# Create two columns
col1, col2 = st.columns(2)

with col1:
    date_rptd = st.date_input("Date Reported")
    time_occ = st.text_input("Time Occurred (HHMM)", placeholder="e.g., 1300 for 1:00 PM")
    area_name = st.selectbox("Area Name", df['AREA NAME'].unique(), index=0)
    lat = st.text_input("Latitude", placeholder="e.g., 34.0522")

with col2:
    date_occ = st.date_input("Date Occurred")
    rpt_dist_no = st.selectbox("Report District Number", df['Rpt Dist No'].unique(), index=0)
    crm_cd = st.selectbox("Crime Code", df['Crm Cd'].unique(), index=0)
    lon = st.text_input("Longitude", placeholder="e.g., -118.2437")

# Predict button
if st.button('Predict'):
    try:
        # Get the crime description based on the selected crime code
        selected_crime_desc = df[df['Crm Cd'] == crm_cd]['Crm Cd Desc'].values[0]
        st.write(f"**Selected Crime Description:** {selected_crime_desc}")
        
        # Calculate number of crimes in the reported district
        district_crime_count = df[df['Rpt Dist No'] == int(rpt_dist_no)].shape[0]
        st.info(f"**Number of Crimes in Reported District {rpt_dist_no}:** {district_crime_count}")

    except Exception as e:
        st.error(f"Error: {e}")

st.markdown('</div>', unsafe_allow_html=True)
