import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import time
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.set_page_config(page_title="SafeScan", layout="centered")

@st.cache_data
def load_safety_data():
    df = pd.read_csv("Real_Ingredient_Safety_List.csv")
    return df

safety_data = load_safety_data()

def clean_ingredient_name(name):
    return re.sub(r'[^a-zA-Z0-9 ]', '', name).lower().strip()

def real_ocr(uploaded_file):
    image = Image.open(uploaded_file).convert('RGB')
    text = pytesseract.image_to_string(image)
    ingredients_raw = re.split(r'[,\n]', text)
    ingredients = [clean_ingredient_name(i) for i in ingredients_raw if i.strip()]
    return ingredients

def get_safety_info(ingredient, safety_data):
    cleaned_db = safety_data.copy()
    cleaned_db["clean_name"] = safety_data["Ingredient"].apply(clean_ingredient_name)
    match = cleaned_db[cleaned_db["clean_name"] == ingredient]
    if not match.empty:
        row = match.iloc[0]
        return row["Info"], row["Risk"]
    else:
        return "No data available", "⚪ Unknown"

def calculate_safety_score(ingredients, safety_data):
    risk_mapping = {"🟢 Low": 2, "🟠 Moderate": 1, "🔴 High": 0, "⚪ Unknown": 1}
    score = 0
    for ing in ingredients:
        _, risk = get_safety_info(ing, safety_data)
        score += risk_mapping.get(risk, 1)
    return round((score / (2 * len(ingredients))) * 10, 1)

st.title("SAFESCAN : PRODUCT SAFETY SCANNER")

if "step" not in st.session_state:
    st.session_state.step = "home"

if st.session_state.step == "home":
    st.subheader("Welcome to SafeScan!")
    st.markdown("""
    SafeScan helps you assess the safety of cosmetic and personal care products by scanning ingredient lists for harmful chemicals and giving a safety score from 0–10.

    ### How SafeScan Works:
    1. **Upload a photo** of the product’s ingredient label.
    2. **OCR extracts** the text.
    3. **Ingredients are checked** against a safety database.
    4. **A score is calculated**, and flagged ingredients are explained.
    """)
    if st.button("Upload an Image"):
        st.session_state.step = "upload"

elif st.session_state.step == "upload":
    uploaded_file = st.file_uploader("Choose an image of ingredients", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, width=250)
        st.session_state.uploaded_file = uploaded_file
        if st.button("Continue"):
            st.session_state.step = "loading"

elif st.session_state.step == "loading":
    st.subheader("Analyzing Image...")
    with st.spinner("Running OCR and processing data..."):
        time.sleep(2)
        try:
            ingredients = real_ocr(st.session_state.uploaded_file)
            if not ingredients:
                st.error("No ingredients detected. Please upload a clearer image.")
                st.session_state.step = "home"
            else:
                st.session_state.ingredients = ingredients
                st.session_state.step = "done"
        except Exception as e:
            st.error(f"An error occurred while processing the image: {e}")
            st.session_state.step = "home"

elif st.session_state.step == "done":
    st.subheader("Done Processing!")
    if st.button("View Results"):
        st.session_state.step = "results"

elif st.session_state.step == "results":
    st.subheader("SAFESCAN : PRODUCT SAFETY SCANNER")
    
    ingredients = st.session_state.ingredients
    score = calculate_safety_score(ingredients, safety_data)
    st.markdown(f"### OVERALL SAFETY SCORE: **{score}/10**")

    st.markdown("#### Ingredient Breakdown")
    results = []
    for ingredient in ingredients:
        info, risk = get_safety_info(ingredient, safety_data)
        results.append((ingredient, info, risk))

    st.table({
        "Ingredients": [r[0] for r in results],
        "Information": [r[1] for r in results],
        "Risk Level": [r[2] for r in results],
    })

    st.button("Return to Home", on_click=lambda: st.session_state.update(step="home"))
