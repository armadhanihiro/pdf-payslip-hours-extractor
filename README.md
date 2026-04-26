# 🧾 PDF Payslip Hours Extractor

A Streamlit web application that automatically extracts and calculates working hours from PDF payslips or manual input.

---

## 🌐 Live Demo

*https://pdf-payslip-hours-extractor.streamlit.app/*

---

## 🚀 Features

* 📄 Upload PDF payslips
* 🔍 Automatic extraction of working hours:

  * Ordinary
  * Time and 1/2
  * Double Time
* ✍️ Manual input for flexible usage
* ⏱️ Calculate total working hours
* 📅 Estimate total working days
* 📊 Handle multiple payslips

---

## 🎯 Scope & Flexibility

This application is designed to extract working hours from structured PDF payslips.

* ✅ **Chandler Agency payslip** → fully automated extraction
* 🔧 **Other payslip formats** → supported via manual input

This approach ensures flexibility, allowing users to still calculate working hours even when the PDF structure differs.

---

## ⚙️ How It Works

### 1. PDF Upload Mode

* Extracts text from uploaded payslip
* Detects working hours using pattern matching (regex)
* Calculates total hours and days automatically

### 2. Manual Input Mode

* Input hours manually per payslip:

  * Ordinary
  * Time and 1/2
  * Double Time
* Useful for unsupported or different payslip formats

---

## 📂 Project Structure

```text
pdf-payslip-hours-extractor/
│
├── app.py
├── requirements.txt
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

## ⚠️ Notes

The automated extraction currently supports:

* Ordinary
* Time and 1/2
* Double Time

Other values such as:

* Shift allowances
* Bonuses
* Tax or salary components

are intentionally ignored to ensure accurate working hour calculations.

---

## 🔮 Future Improvements

* Support for multiple payslip formats
* Smart payslip structure detection
* Data visualization dashboard

---

## 👨‍💻 Author

**Armadhani Hiro Juni Permana**


---

## ⭐ Support

If you find this project useful, feel free to ⭐ the repository!
