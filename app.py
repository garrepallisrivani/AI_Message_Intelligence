import streamlit as st
import pandas as pd

from src.classifier import classify_message
from src.sensitive_detector import (
    detect_sensitive_information,
    mask_sensitive_information,
    get_sensitivity_metadata
)
from src.task_event_extractor import extract_task_or_event


st.set_page_config(
    page_title="AI Message Intelligence",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Message Intelligence")
st.write(
    "A rule-based message intelligence system for classification, "
    "task/event extraction, and sensitive-information protection."
)

st.warning(
    "Do not upload real passwords, OTPs, banking information, "
    "or other private information to this demo."
)

uploaded_file = st.file_uploader(
    "Upload a CSV containing Message ID, Timestamp, Sender and Message",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)

        required_columns = [
            "message_id",
            "timestamp",
            "sender",
            "message"
        ]

        missing = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing:
            st.error(
                f"Missing required columns: {', '.join(missing)}"
            )
            st.stop()

        df = df.sort_values("timestamp").reset_index(drop=True)

        results = []

        for _, row in df.iterrows():

            message_id = row["message_id"]
            timestamp = row["timestamp"]
            sender = row["sender"]
            message = str(row["message"])

            sensitive_types = detect_sensitive_information(message)

            sensitivity_metadata = get_sensitivity_metadata(
                sensitive_types
            )

            masked_message = mask_sensitive_information(message)

            classification = classify_message(message)

            task_or_event = extract_task_or_event(
                message_id,
                message,
                classification["category"]
            )

            result = {
                "message_id": message_id,
                "timestamp": str(timestamp),
                "sender": sender,
                "category": classification["category"],
                "confidence": classification["confidence"],
                "reason": classification["reason"],
                "sensitive": bool(sensitive_types),
                "sensitivity_types": sensitive_types,
                "sensitivity_risk": sensitivity_metadata["risk"],
                "recommended_action":
                    sensitivity_metadata["recommended_action"],
                "masked_message": masked_message,
                "task_or_event": task_or_event
            }

            results.append(result)

        result_df = pd.DataFrame(results)

        st.success(
            f"Successfully processed {len(results)} messages."
        )

        st.subheader("Category Summary")

        category_counts = (
            result_df["category"]
            .value_counts()
            .rename_axis("Category")
            .reset_index(name="Count")
        )

        st.dataframe(
            category_counts,
            use_container_width=True,
            hide_index=True
        )

        col1, col2, col3, col4 = st.columns(4)

        task_event_count = sum(
            bool(x.get("task_or_event"))
            for x in results
        )

        sensitive_count = int(
            result_df["sensitive"].sum()
        )

        unresolved_dates = sum(
            1
            for x in results
            if x.get("task_or_event")
            and x["task_or_event"].get("date_or_deadline") is None
        )

        with col1:
            st.metric(
                "Messages Processed",
                len(results)
            )

        with col2:
            st.metric(
                "Task/Event Records",
                task_event_count
            )

        with col3:
            st.metric(
                "Sensitive Messages",
                sensitive_count
            )
        with col4:
            st.metric(
                "Unresolved Dates",
                unresolved_dates
            )
        st.subheader("Search Message")

        message_ids = result_df["message_id"].astype(str).tolist()

        selected_id = st.selectbox(
            "Select a message ID",
            message_ids
        )

        selected = next(
            x for x in results
            if str(x["message_id"]) == selected_id
        )

        st.write("### Classification")

        col1, col2 = st.columns(2)

        with col1:
            st.write(
                "**Category:**",
                selected["category"]
            )
            st.write(
                "**Confidence:**",
                selected["confidence"]
            )

        with col2:
            st.write(
                "**Sensitive:**",
                selected["sensitive"]
            )
            st.write(
                "**Risk:**",
                selected["sensitivity_risk"]
            )

        st.write("**Reason:**")
        st.info(selected["reason"])

        st.write("### Masked Message")
        st.code(selected["masked_message"])

        if selected["sensitive"]:

            st.write("### Sensitive Information")

            st.write(
                "**Types:**",
                ", ".join(selected["sensitivity_types"])
            )

            st.write(
                "**Recommended Action:**",
                selected["recommended_action"]
            )

        if selected["task_or_event"]:

            st.write("### Task / Event")

            item = selected["task_or_event"]

            st.json(item)

        st.write("### Processed Results")

        display_df = result_df[
            [
                "message_id",
                "timestamp",
                "sender",
                "category",
                "confidence",
                "sensitive",
                "sensitivity_risk",
                "masked_message"
            ]
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:

        st.error(
            "An error occurred while processing the uploaded CSV."
        )

        st.exception(e)

else:

    st.info(
        "Upload the assignment CSV to run the message intelligence pipeline."
    )

    st.subheader("System Capabilities")

    st.write(
        """
        - Six-category message classification
        - Confidence scoring
        - Explainable classification reasons
        - Sensitive information detection
        - Sensitive information masking
        - Risk assessment
        - Recommended security actions
        - Task extraction
        - Event extraction
        - Date and deadline extraction
        - Time extraction
        - Person extraction
        - Priority determination
        """
    )