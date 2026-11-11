# AI Privacy Guardian

**Class 12 AI Capstone Project — AI Privacy in the Digital Age**

*Contributor.*Vinit Chahande

*class.*XII-B

*School.*PM SHRI Jawahar Navodaya Vidyalaya,Selukate,Wardha

## What it does
- Detects common patterns such as email addresses, phone numbers, password-like phrases, IP addresses, payment-card-like digit strings and PAN-like identifiers.
- Masks detected values in the results.
- Uses a small Scikit-learn TF-IDF + Logistic Regression model trained on the included synthetic classroom dataset to classify text as `personal_data` or `general`.
- Calculates a simple educational risk score and suggests privacy practices.
- Lets the user download a text report.

## Important limitations
This is a classroom prototype, not a certified privacy/security product. It does not validate identity numbers or payment cards, cannot detect every form of personal information, and its small synthetic ML dataset is not representative of real-world language. A low score does not guarantee that text is safe. Do not enter real personal, financial, password, or government-ID data.

## Requirements
- Python 3.10 or newer recommended
- Internet connection for the first installation of packages

## Run on Windows
1. Install Python from https://www.python.org/downloads/ and enable **Add Python to PATH**.
2. Open this folder in VS Code.
3. Open Terminal > New Terminal.
4. Run:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

5. A browser tab should open with the application. If not, copy the local URL shown in the terminal (usually http://localhost:8501).

## Project files
- `app.py` — Streamlit user interface
- `privacy_model.py` — pattern scanner, masking, ML model and recommendations
- `data/training_data.csv` — synthetic training examples
- `requirements.txt` — Python dependencies
- `documentation/` — project report
- `presentation/` — project presentation

## Privacy design
The app does not include code to upload text to a remote service or save the scanned text to a database. Streamlit runs locally when launched using the instructions above. Downloading a report is an action initiated by the user.
