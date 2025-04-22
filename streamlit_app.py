import streamlit as st
import time

def mock_ocr(image):
    return ["Water", "Parfum", "Parabens", "Sodium Laureth Sulfate", "Glycerin", "Phthalates"]

def get_ingredient_safety(ingredient):
    data = {
        "Water": ("Safe, commonly used as a base in products.", "🟢 Low Risk"),
        "Parfum": ("Can contain undisclosed chemicals; may cause irritation or allergies.", "🟠 Moderate Risk"),
        "Parabens": ("Preservatives linked to hormone disruption.", "🔴 High Risk"),
        "Sodium Laureth Sulfate": ("Cleansing agent, may cause skin irritation.", "🟡 Medium Risk"),
        "Glycerin": ("Moisturizer, generally safe.", "🟢 Low Risk"),
        "Phthalates": ("Often hidden in 'fragrance'; linked to reproductive harm.", "🔴 High Risk")
    }
    return data.get(ingredient, ("No data available", "⚪ Unknown"))

st.set_page_config(page_title="SafeScan", layout="centered")

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
        if st.button("Continue"):
            st.session_state.step = "loading"

elif st.session_state.step == "loading":
    st.subheader("Analyzing Image...")
    with st.spinner("Running OCR and processing data..."):
        time.sleep(2)
        st.session_state.ingredients = mock_ocr(None)
        st.session_state.step = "done"

elif st.session_state.step == "done":
    st.subheader("Done Processing!")
    if st.button("View Results"):
        st.session_state.step = "results"

elif st.session_state.step == "results":
    st.subheader("SAFESCAN : PRODUCT SAFETY SCANNER")
    st.markdown("### OVERALL SAFETY SCORE: **4/10**")

    st.markdown("#### Ingredient Breakdown")
    results = []
    for ingredient in st.session_state.ingredients:
        info, risk = get_ingredient_safety(ingredient)
        results.append((ingredient, info, risk))

    st.table({
        "Ingredients": [r[0] for r in results],
        "Information": [r[1] for r in results],
        "Risk Level": [r[2] for r in results],
    })

    st.button("Return to Home", on_click=lambda: st.session_state.update(step="home"))