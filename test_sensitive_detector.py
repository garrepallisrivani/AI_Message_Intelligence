from src.sensitive_detector import (
    detect_sensitive_information,
    mask_sensitive_information,
    get_sensitivity_metadata,
)


def test_otp_detection_and_masking():

    message = "Your OTP is 482193."

    detected = detect_sensitive_information(message)
    masked = mask_sensitive_information(message)

    assert "one_time_password" in detected
    assert "482193" not in masked
    assert "******" in masked


def test_password_detection_and_masking():

    message = "My password is Hello123."

    detected = detect_sensitive_information(message)
    masked = mask_sensitive_information(message)

    assert "password" in detected
    assert "Hello123" not in masked


def test_phone_detection_and_masking():

    message = "Call me at 9876543210."

    detected = detect_sensitive_information(message)
    masked = mask_sensitive_information(message)

    assert "phone_number" in detected
    assert "9876543210" not in masked


def test_email_detection_and_masking():

    message = "My email is example@gmail.com."

    detected = detect_sensitive_information(message)
    masked = mask_sensitive_information(message)

    assert "email" in detected
    assert "example@gmail.com" not in masked


def test_sensitive_metadata():

    detected = ["one_time_password"]

    metadata = get_sensitivity_metadata(detected)

    assert metadata["risk"] == "high"
    assert metadata["recommended_action"] == "do_not_store"