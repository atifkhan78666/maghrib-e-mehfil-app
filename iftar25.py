import streamlit as st
import qrcode
import os
import time
from PIL import Image
import gspread
from google.oauth2.service_account import Credentials

# Define the folder to store uploaded files and data
upload_folder = "uploaded_screenshots"
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# Google Sheets setup
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
client = gspread.authorize(creds)

# Open the Google Sheet by URL
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1ItSIfHlDumFX4Bu3Hqrt-b6OP51nXPcMCM8ldF5TZhg/edit?usp=sharing')
sheet_instance = sheet.get_worksheet(0)  # Select the first sheet

# Custom CSS for background color and styling
st.markdown("""
    <style>
        body {
            background-color: #f7f3e9;
        }
        .title {
            color: #3A6351;
            font-family: 'Verdana', sans-serif;
            text-align: center;
            font-size: 40px;
            font-weight: bold;
        }
        .dua {
            color: #3A6351;
            font-family: 'Georgia', sans-serif;
            text-align: center;
            font-size: 22px;
            margin-bottom: 20px;
        }
        .form-title {
            color: #000;
            text-align: center;
            margin-top: 30px;
            font-size: 28px;
        }
        .form-text {
            font-family: 'Verdana', sans-serif;
            color: #3A6351;
            font-size: 18px;
        }
        .coordinators {
            color: #000;
            font-weight: bold;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# Ramadan Dua at the top
st.markdown('<p class="dua">اللّهُمَّ إِنِّي لَكَ صُمْتُ وَبِكَ آمَنْتُ وَعَلَيْكَ تَوَكَّلْتُ وَعَلَى رِزْقِكَ أَفْطَرْتُ</p>', unsafe_allow_html=True)

# Title for the event
st.markdown('<p class="title">MAGHRIB-E-MEHFIL 2.0</p>', unsafe_allow_html=True)

# Event description
st.write("""
Let's come together for a spectacular Ramadan iftar party on **11th of March 2025 at 6pm**! 
Join us in CL Building, where we'll break our fast, enjoy scrumptious food, and create beautiful memories. Don't be late! 🌙🎉
""")

# Teacher coordinators
st.write("### TEACHER COORDINATORS:")
st.write("""
- Mr. Tabish Mufti
- Mr. Md. Omair Ahmad
- Ms. Nusrat Jahan
- Ms. Ayesha Kamal
""")

# Student coordinators
st.write("### STUDENT COORDINATORS:")
st.write("""
- Mohd Atif Khan - +919643748904
- Mohd Shadab Khan - +919718301702
- Mohmmad Sufian - +91 6200126662
- Mohsina - +9197989 41815
- Sana Abedin - +9170043 9433
""")

# Student details form
st.markdown('<p class="form-title">Registration Form</p>', unsafe_allow_html=True)
name = st.text_input("Name")
phone_number = st.text_input("Phone Number")
course = st.text_input("Course")
year = st.selectbox("Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
section = st.text_input("Section")

# QR Code for Payment (250 INR)
st.write("### Pay Rs. 250 via the QR code below and upload the payment screenshot.")
qr_image = qrcode.make("upi://pay?pa=your-upi-id@bank&pn=Maghrib-E-Mehfil&am=250")  # Replace with your UPI ID
qr_image.save("payment_qr.png")
st.image("payment_qr.png", caption="Scan to Pay Rs. 250")

# File uploader for payment screenshot
st.write("### Upload Payment Screenshot")
screenshot = st.file_uploader("Choose a file (image)", type=["jpg", "png", "jpeg"])

# Function to save student data to Google Sheet with timestamp and proper file extension
def save_student_data_to_sheet(name, phone_number, course, year, section, screenshot_file):
    # Get the file extension of the uploaded screenshot
    file_extension = os.path.splitext(screenshot_file.name)[1]
    timestamp = int(time.time())  # Add timestamp to avoid file overwrite
    
    # Create the file path where the screenshot will be saved
    screenshot_path = os.path.join(upload_folder, f"{name}_payment_screenshot_{timestamp}{file_extension}")
    
    # Save the uploaded screenshot file
    with open(screenshot_path, "wb") as f:
        f.write(screenshot_file.getbuffer())
    
    # Add the student's data along with the screenshot path to Google Sheet
    sheet_instance.append_row([name, phone_number, course, year, section, screenshot_path])
    
    st.success(f"Data saved successfully for {name}!")

# Submit button with error handling
if st.button("Submit"):
    # Check for missing information in form fields
    if not name or not phone_number or not course or not year or not section:
        st.error("Please fill all the fields.")
    elif screenshot is None:
        st.error("Please upload the payment screenshot.")
    else:
        # Save the student's data to Google Sheet and show success message
        try:
            save_student_data_to_sheet(name, phone_number, course, year, section, screenshot)
            st.success(f"Thank you, {name}! Your registration is complete.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")



