import re


# Patterns used to identify sensitive information

SENSITIVE_PATTERNS = {

    "one_time_password": [
        r"\b(?:otp|one[- ]time password)\b.{0,30}\b\d{4,8}\b"
    ],

    "password": [
        r"\b(?:password|passwd|pwd)\b\s*(?:is|:|=)?\s*\S+"
    ],

    "pin": [
        r"\b(?:pin|pin number)\b\s*(?:is|:|=)\s*\d{4,6}\b"
    ],

    "phone_number": [
        r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b"
    ],

    "email": [
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ],

    "card_number": [
        r"\b(?:\d[ -]?){13,19}\b"
    ],

    "account_number": [
        r"\b(?:account|a/c|bank account)\b.{0,30}\b\d{8,18}\b"
    ],

    "access_token": [
        r"\b(?:access token|token|api key|auth token)\b.{0,50}\S+"
    ],

    "recovery_code": [
        r"\b(?:recovery code|backup code)\b.{0,30}\b[A-Za-z0-9-]{4,20}\b"
    ],

    "identification_number": [
        r"\b(?:aadhaar|passport|pan|id number|identification number)\b"
        r".{0,30}\b[A-Za-z0-9-]{4,20}\b"
    ],

    "address": [
        r"\b(?:my home address|my address|home address)\b.{0,100}"
    ],

    "health_information": [
        r"\b(?:test result|medical diagnosis|diagnosis|medication|"
        r"medicine|prescription|symptom|blood pressure|blood sugar|"
        r"vitamin [a-z0-9]+|health condition|medical condition)\b"
    ],
}

# Risk level and recommended action for each sensitivity type

SENSITIVITY_METADATA = {
    "one_time_password": {
        "risk": "high",
        "recommended_action": "do_not_store",
    },
    "password": {
        "risk": "high",
        "recommended_action": "do_not_store",
    },
    "pin": {
        "risk": "high",
        "recommended_action": "do_not_store",
    },
    "access_token": {
        "risk": "high",
        "recommended_action": "do_not_store",
    },
    "recovery_code": {
        "risk": "high",
        "recommended_action": "do_not_store",
    },
    "card_number": {
        "risk": "high",
        "recommended_action": "do_not_store",
    },
    "account_number": {
        "risk": "high",
        "recommended_action": "ask_for_confirmation",
    },
    "identification_number": {
        "risk": "high",
        "recommended_action": "do_not_store",
    },
    "phone_number": {
        "risk": "medium",
        "recommended_action": "safe_to_process_locally",
    },
    "email": {
        "risk": "medium",
        "recommended_action": "safe_to_process_locally",
    },
    "address": {
        "risk": "medium",
        "recommended_action": "ask_for_confirmation",
    },
    "health_information": {
        "risk": "high",
        "recommended_action": "do_not_store",
    },
}
def detect_sensitive_information(message):
    """
    Detect sensitive information in a message.

    Returns a list of detected sensitive information types.
    """

    detected_types = []

    for sensitivity_type, patterns in SENSITIVE_PATTERNS.items():

        for pattern in patterns:

            if re.search(
                pattern,
                message,
                flags=re.IGNORECASE
            ):
                detected_types.append(sensitivity_type)
                break

    return detected_types

def get_sensitivity_metadata(detected_types):
    """
    Return risk level and recommended action for detected
    sensitive information types.
    """

    if not detected_types:
        return {
            "risk": None,
            "recommended_action": None,
        }

    risks = []
    actions = []

    for sensitivity_type in detected_types:

        metadata = SENSITIVITY_METADATA.get(
            sensitivity_type
        )

        if metadata:
            risks.append(metadata["risk"])
            actions.append(
                metadata["recommended_action"]
            )

    # Highest risk wins
    if "high" in risks:
        risk = "high"
    elif "medium" in risks:
        risk = "medium"
    else:
        risk = "low"

    # Most restrictive action wins
    if "do_not_store" in actions:
        action = "do_not_store"
    elif "ask_for_confirmation" in actions:
        action = "ask_for_confirmation"
    else:
        action = "safe_to_process_locally"

    return {
        "risk": risk,
        "recommended_action": action,
    }

def mask_sensitive_information(message):
    """
    Replace sensitive values with safe masked text.
    """

    masked_message = message

    # ---------------------------------------------------------
    # OTP
    # ---------------------------------------------------------

    masked_message = re.sub(
        r"(\b(?:otp|one[- ]time password)\b.{0,30}?)\b\d{4,8}\b",
        r"\1******",
        masked_message,
        flags=re.IGNORECASE
    )

    # ---------------------------------------------------------
    # Password
    # ---------------------------------------------------------

    masked_message = re.sub(
        r"(\b(?:password|passwd|pwd)\b\s*(?:is|:|=)?\s*)\S+",
        r"\1******",
        masked_message,
        flags=re.IGNORECASE
    )

    # ---------------------------------------------------------
    # PIN
    # ---------------------------------------------------------

    masked_message = re.sub(
        r"(\b(?:pin|pin number)\b\s*(?:is|:|=)\s*)\d{4,6}\b",
        r"\1******",
        masked_message,
        flags=re.IGNORECASE
    )

    # ---------------------------------------------------------
    # Phone numbers
    # ---------------------------------------------------------

    masked_message = re.sub(
        r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",
        "[PHONE_REDACTED]",
        masked_message
    )

    # ---------------------------------------------------------
    # Email addresses
    # ---------------------------------------------------------

    masked_message = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "[EMAIL_REDACTED]",
        masked_message
    )

    # ---------------------------------------------------------
    # Card numbers
    # ---------------------------------------------------------

    masked_message = re.sub(
        r"\b(?:\d[ -]?){13,19}\b",
        "[CARD_REDACTED]",
        masked_message
    )

    # ---------------------------------------------------------
    # Account numbers
    # ---------------------------------------------------------

    masked_message = re.sub(
        r"(\b(?:account|a/c|bank account)\b.{0,30}?)"
        r"\b\d{8,18}\b",
        r"\1[ACCOUNT_REDACTED]",
        masked_message,
        flags=re.IGNORECASE
    )

    # ---------------------------------------------------------
    # Identification numbers
    # ---------------------------------------------------------

    masked_message = re.sub(
        r"(\b(?:aadhaar|passport|pan|id number|identification number)\b"
        r".{0,30}?)\b[A-Za-z0-9-]{4,20}\b",
        r"\1[ID_REDACTED]",
        masked_message,
        flags=re.IGNORECASE
    )

    # ---------------------------------------------------------
    # Access tokens / API keys
    # ---------------------------------------------------------

    masked_message = re.sub(
        r"(\b(?:access token|token|api key|auth token)\b"
        r"\s*(?:is|:|=)?\s*)\S+",
        r"\1[TOKEN_REDACTED]",
        masked_message,
        flags=re.IGNORECASE
    )

    # ---------------------------------------------------------
    # Recovery codes
    # ---------------------------------------------------------

    masked_message = re.sub(
        r"(\b(?:recovery code|backup code)\b.{0,30}?)"
        r"\b[A-Za-z0-9-]{4,20}\b",
        r"\1[CODE_REDACTED]",
        masked_message,
        flags=re.IGNORECASE
    )

    # ---------------------------------------------------------
    # Health information
    # ---------------------------------------------------------

    masked_message = re.sub(
        r"\b(?:my\s+)?(?:recent\s+)?"
        r"(?:test result|medical diagnosis|diagnosis|"
        r"medication|medicine|prescription|symptom|"
        r"blood pressure|blood sugar|"
        r"vitamin [a-z0-9]+|health condition|medical condition)"
        r"(?:\s+(?:says|is|shows))?"
        r"(?:.{0,100})",
        "[HEALTH_INFORMATION_REDACTED]",
        masked_message,
        flags=re.IGNORECASE
    )

    # ---------------------------------------------------------
    # Home address
    # ---------------------------------------------------------

    masked_message = re.sub(
        r"\b(?:my home address|my address|home address)\b.{0,100}",
        "[ADDRESS_REDACTED]",
        masked_message,
        flags=re.IGNORECASE
    )

    return masked_message