import math
import re

import pdfplumber
import streamlit as st


TFI_VALID_TYPES = [
    "Ordinary Hours",
    "Overtime At 1.50X",
    "Public Holiday",
    "Annual Leave",
    "Personal Leave",
]

APG_VALID_ITEMS = [
    "ORD HOURS",
    "T1.5",
    "T2.0",
    "PHT1.5 ORD",
    "PHT2.5 O/T"
]


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


def extract_hours_chandler(text):
    pattern = (
        r"(\d{1,2}/\d{1,2}/\d{4})\s+"
        r"(Ordinary|Time\s+and\s+1/2|Double\s+Time|Shift\s+-\s+Public\s+Holiday)\s+"
        r"(\d+(?:\.\d+)?)"
    )

    matches = re.findall(pattern, text, re.IGNORECASE)

    public_holiday_dates = set()

    for date, description, hours in matches:
        if description.lower().strip() == "shift - public holiday":
            public_holiday_dates.add(date.strip())

    results = []
    seen = set()

    for date, description, hours in matches:
        date = date.strip()
        description = description.strip()
        hours = float(hours)

        if description.lower() == "ordinary" and date in public_holiday_dates:
            continue

        key = (date, description.lower(), hours)

        if key in seen:
            continue

        seen.add(key)

        results.append({
            "format": "Chandler Agency",
            "description": description.title(),
            "date": date,
            "hours": hours,
        })

    return results


def extract_hours_tfi(text):
    valid_types_pattern = "|".join(re.escape(item) for item in TFI_VALID_TYPES)

    pattern = (
        rf"({valid_types_pattern})"
        r"(?! Unpaid).*?- TIM\s+"
        r"(\d+(?:\.\d+)?)\s+"
        r"\d+(?:\.\d+)?\s+"
        r"\d+(?:\.\d+)?\s+"
        r"\d+(?:\.\d+)?\s+"
        r"(\d{1,2}/\d{1,2}/\d{4})"
    )

    matches = re.findall(pattern, text, re.IGNORECASE)

    results = []
    seen = set()

    for description, hours, date in matches:
        description = description.strip()
        date = date.strip()
        hours = float(hours)

        key = (description.lower(), date, hours)

        if key in seen:
            continue

        seen.add(key)

        results.append({
            "format": "TFI",
            "description": description.title(),
            "date": date,
            "hours": hours,
        })

    return results


def extract_hours_apg(text):
    valid_items_pattern = "|".join(re.escape(item) for item in APG_VALID_ITEMS)

    pattern = (
        rf"({valid_items_pattern})\s+"
        r".*?\s+"
        r"(\d+(?:\.\d+)?)\s+"
        r"\$?\d+(?:\.\d+)?\s+"
        r"\$?\d+(?:,\d{3})*(?:\.\d+)?"
    )

    matches = re.findall(pattern, text, re.IGNORECASE)

    results = []
    seen = set()

    for description, hours in matches:
        description = description.strip().upper()
        hours = float(hours)

        key = (description, hours)

        if key in seen:
            continue

        seen.add(key)

        results.append({
            "format": "APG Workforce",
            "description": description,
            "date": "-",
            "hours": hours,
        })

    return results


def extract_hours(text):
    apg_results = extract_hours_apg(text)
    if apg_results:
        return apg_results

    tfi_results = extract_hours_tfi(text)
    if tfi_results:
        return tfi_results

    chandler_results = extract_hours_chandler(text)
    if chandler_results:
        return chandler_results

    return []


def extract_hours_by_format(text, format_mode):
    if format_mode == "Chandler Agency":
        return extract_hours_chandler(text)

    if format_mode == "TFI":
        return extract_hours_tfi(text)

    if format_mode == "APG Workforce":
        return extract_hours_apg(text)

    return extract_hours(text)


def main():
    st.set_page_config(
        page_title="Payslip Hours Calculator",
        page_icon="🧾",
        layout="centered",
    )

    st.title("🧾 Payslip Hours Calculator")
    st.caption("Calculate working hours from PDF payslips or manual input.")

    input_mode = st.selectbox(
        "Choose input method",
        ["Upload PDF", "Manual Input"],
    )

    grand_total_hours = 0
    grand_total_days = 0

    if input_mode == "Upload PDF":
        format_mode = st.selectbox(
            "Select payslip format",
            ["Auto Detect", "Chandler Agency", "TFI", "APG Workforce"],
        )

        st.caption("Use Auto Detect for convenience, or select a format manually if detection fails.")

        uploaded_files = st.file_uploader(
            "Upload PDF payslips",
            type=["pdf"],
            accept_multiple_files=True,
        )

        if uploaded_files:
            for index, uploaded_file in enumerate(uploaded_files, start=1):
                st.subheader(f"Payslip {index}: {uploaded_file.name}")

                text = extract_text_from_pdf(uploaded_file)
                extracted_items = extract_hours_by_format(text, format_mode)

                if not extracted_items:
                    st.warning("No supported working hours detected in this payslip.")
                    continue

                total_hours = sum(item["hours"] for item in extracted_items)
                total_days = calculate_day(total_hours)

                grand_total_hours += total_hours
                grand_total_days += total_days

                detected_format = extracted_items[0]["format"]
                st.write(f"Detected format: **{detected_format}**")

                st.write("Detected items:")

                for item in extracted_items:
                    st.write(
                        f"- {item['date']} | "
                        f"{item['description']}: "
                        f"{item['hours']:.2f} hours"
                    )

                st.success(f"Total hours this payslip: {total_hours:.2f}")
                st.info(f"Total days this payslip: {total_days}")

    else:
        total_payslips = st.number_input(
            "Enter total payslips",
            min_value=1,
            step=1,
        )

        for i in range(total_payslips):
            st.subheader(f"Payslip {i + 1}")

            ordinary_hours = st.number_input(
                "Ordinary hours",
                min_value=0.0,
                step=0.25,
                key=f"ordinary_{i}",
            )

            time_half_hours = st.number_input(
                "Time and 1/2 hours",
                min_value=0.0,
                step=0.25,
                key=f"time_half_{i}",
            )

            double_time_hours = st.number_input(
                "Double Time hours",
                min_value=0.0,
                step=0.25,
                key=f"double_time_{i}",
            )

            annual_leave_hours = st.number_input(
                "Annual Leave hours",
                min_value=0.0,
                step=0.25,
                key=f"annual_leave_{i}",
            )

            personal_leave_hours = st.number_input(
                "Personal Leave hours",
                min_value=0.0,
                step=0.25,
                key=f"personal_leave_{i}",
            )

            public_holiday_hours = st.number_input(
                "Public Holiday hours",
                min_value=0.0,
                step=0.25,
                key=f"public_holiday_{i}",
            )

            total_hours = (
                ordinary_hours
                + time_half_hours
                + double_time_hours
                + annual_leave_hours
                + personal_leave_hours
                + public_holiday_hours
            )

            total_days = calculate_day(total_hours)

            grand_total_hours += total_hours
            grand_total_days += total_days

            st.success(f"Total hours this payslip: {total_hours:.2f}")
            st.info(f"Total days this payslip: {total_days}")

    if grand_total_hours > 0:
        st.divider()
        st.header("Overall Total")
        st.metric("Grand Total Hours", f"{grand_total_hours:.2f}")
        st.metric("Grand Total Days", grand_total_days)


if __name__ == "__main__":
    main()