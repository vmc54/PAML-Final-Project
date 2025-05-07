**Project Overview**
SafeScan is a machine learning-powered Streamlit app that helps users evaluate the safety of cosmetic products by analyzing ingredient labels from images. Many consumers are unsure about chemical names like parabens or sulfates, and existing tools are often static or incomplete. SafeScan uses OCR to extract ingredients and predicts a 0–10 safety score, offering a transparent and personalized experience for health-conscious users.

**Repo Structure**
streamlit_app.py                     # Main Streamlit application
Real_Ingredient_Safety_List.csv      # Ingredient database with harm scores and descriptions
code.ipynb
README.md                            # Project documentation

**How to Run**
Install Tesseract OCR
Make sure Tesseract is installed and accessible:

Windows: Download using this link: https://github.com/tesseract-ocr/tesseract 
Mac: brew install tesseract
Linux: sudo apt-get install tesseract-ocr

Install Python dependencies
pip install streamlit pandas pillow pytesseract

Run the app
streamlit run streamlit_app.py

Upload an image of a product’s ingredient list and view the analysis!
Note: You may need to update the path to the Tesseract executable in streamlit_app.py depending on your OS.

**ML Models**
We trained three regression models from scratch to predict the safety score based on ingredient content:

Linear Regression (R² = 0.66)
Decision Tree (R² = 0.76)
Random Forest (R² = 0.87, MSE = 1.31, MAE = 0.76)

The Random Forest model was selected for deployment due to its strong generalization performance.


**Demo Output**
Sample Input (OCR Extracted): `Water, Glycerin, Parfum` 
=> Result: Overall Safety Score: 3.8 / 10

Ingredient Breakdown:
Water — 0.0: Likely safe.
Glycerin — 0.0: Likely safe.
Parfum — 1.0: Likely safe.

**Video Link**
https://drive.google.com/file/d/1uwJCd7NwHV8dVMMOh3D__-q5G_egMVrB/view?usp=sharing 

**Team Members**
Jaspreet Lal (jl4536)
Yi Lu (yl3838)
Vivien Chang (vmc54)
Zifan Yang (zy489)
