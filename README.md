# 🧾 PDF Payslip Hours Extractor

A Streamlit web application that intelligently extracts and calculates working hours from multiple PDF payslip formats or manual input.

---

## 🌐 Live Demo

*https://pdf-payslip-hours-extractor.streamlit.app/*

---

## 🚀 Features

- 📄 Upload PDF payslips
- 🔍 Automatic extraction of working hours:
  - Chandler Agency
  - TFI (Thomas Foods International)
  - APG Workforce
- ✍️ Manual input for flexible usage
- ⏱️ Calculate total working hours
- 📅 Estimate total working days
- 📊 Handle multiple payslips

---

## 🎯 Scope & Flexibility

This application is designed to extract working hours from structured PDF payslips.

* ✅ **Chandler Agency payslip** → fully automated extraction
* 🔧 **Other payslip formats** → supported via manual input

This approach ensures flexibility, allowing users to still calculate working hours even when the PDF structure differs.

---

## ⚙️ How It Works

### 1. PDF Upload Mode

* Upload one or multiple payslips
* System extracts text and detects format
* Parses valid working hours
* Displays breakdown + totals

### 2. Manual Input Mode

* Input:
  * Ordinary
  * Overtime
  * Leave
  * Public Holiday
Useful for unsupported formats

---

## 📂 Project Structure

```text
pdf-payslip-hours-extractor/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
```

---

## 🛠️ Tech Stack

* Python
* Streamlit
* pdfplumber
* Regular Expressions (Regex)

---

## ⚙️ Installation & Setup

Clone the repository:

```bash
git clone https://github.com/armadhanihiro/pdf-payslip-hours-extractor.git
cd pdf-payslip-hours-extractor
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

Then open in browser:

```
http://localhost:8501
```

---

## 📸 Demo

<img width="861" height="939" alt="image" src="https://github.com/user-attachments/assets/6fe8c1b5-4cce-49ed-b75d-0dae574d8baa" />
<br/><br/>

<img width="1028" height="940" alt="image" src="https://github.com/user-attachments/assets/a97936d9-d65c-4d04-8bbd-d83f7d93c540" />




---

## 🎯 Use Case

This tool was built to automate the process of calculating working hours from payslips, eliminating manual calculations and reducing errors.

It is especially useful for:
  * Casual workers
  * Shift-based employees
  * Workers with multiple pay formats

---

## 🔮 Future Improvements

* Support for more payslip formats
* Smart payslip structure detection
* Data visualization dashboard

---

## 👨‍💻 Author

**Armadhani Hiro Juni Permana**


---

## ⭐ Support

If you find this project useful, feel free to ⭐ the repository!
