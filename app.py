import math
import re
import pdfplumber
import streamlit as st


def calculate_day(hour):
    if hour >= 40:
        return 7
    return math.ceil(hour / 8)


def extract_text_from_pdf(uploaded_file):
    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


def extract_hours_from_text(text):
    pattern = r"(Ordinary|Time\s+and\s+1/2|Double\s+Time)\s+(\d+(?:\.\d+)?)"
    matches = re.findall(pattern, text, re.IGNORECASE)

    results = []

    for item, qty in matches:
        results.append({
            "description": item.title(),
            "hours": float(qty)
        })

    return results


def main():
    st.set_page_config(
        page_title="Payslip Hours Calculator",
        page_icon="🧾",
        layout="centered"
    )

    st.title("🧾 Payslip Hours Calculator")
    st.write("Calculate working hours from PDF payslips or manual input.")

    input_mode = st.radio(
        "Choose input method",
        ["Upload PDF", "Manual Input"]
    )

    grand_total_hours = 0
    grand_total_days = 0

    if input_mode == "Upload PDF":
        uploaded_files = st.file_uploader(
            "Upload PDF payslips",
            type=["pdf"],
            accept_multiple_files=True
        )

        if uploaded_files:
            for index, uploaded_file in enumerate(uploaded_files, start=1):
                st.subheader(f"Payslip {index}: {uploaded_file.name}")

                text = extract_text_from_pdf(uploaded_file)
                extracted_items = extract_hours_from_text(text)

                if not extracted_items:
                    st.warning("No working hours detected in this payslip.")
                    continue

                total_hours = sum(item["hours"] for item in extracted_items)
                total_days = calculate_day(total_hours)

                grand_total_hours += total_hours
                grand_total_days += total_days

                # for item in extracted_items:
                #     st.write(f"- {item['description']}: {item['hours']:.2f} hours")

                st.success(f"Hours: {total_hours:.2f}")
                st.info(f"Days: {total_days}")

    else:
        total_payslips = st.number_input(
            "Enter total payslips",
            min_value=1,
            step=1
        )

        for i in range(total_payslips):
            st.subheader(f"Payslip {i + 1}")

            ordinary_hours = st.number_input(
                "Ordinary hours",
                min_value=0.0,
                step=0.25,
                key=f"ordinary_{i}"
            )

            time_half_hours = st.number_input(
                "Time and 1/2",
                min_value=0.0,
                step=0.25,
                key=f"time_half_{i}"
            )

            double_time_hours = st.number_input(
                "Double Time",
                min_value=0.0,
                step=0.25,
                key=f"double_time_{i}"
            )

            total_hours = ordinary_hours + time_half_hours + double_time_hours
            total_days = calculate_day(total_hours)

            grand_total_hours += total_hours
            grand_total_days += total_days

            st.success(f"Total hours this payslip: {total_hours:.2f}")
            st.info(f"Total days this payslip: {total_days}")

    if grand_total_hours > 0:
        st.divider()
        st.header("---Overall---")
        st.metric("Total Hours", f"{grand_total_hours:.2f}")
        st.metric("Total Days", grand_total_days)


if __name__ == "__main__":
    main()