import pytest
import pandas as pd
import os
import re

def load_csv(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    df = pd.read_csv(filepath)
    if df.empty:
        raise ValueError("CSV file is empty")
    return df


def clean_phone(phone):
    if not isinstance(phone, str):
        return None
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == "1":
        return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    return None


def validate_email(email):
    if not isinstance(email, str):
        return False
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))


# tests for load_csv 

def test_load_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_csv("nonexistent_file.csv")


def test_load_csv_empty_file(tmp_path):
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")
    with pytest.raises((ValueError, pd.errors.EmptyDataError)):
        load_csv(str(empty_file))


def test_load_csv_successful(tmp_path):
    valid_file = tmp_path / "valid.csv"
    valid_file.write_text("customer_id,age,email\n1,25,test@example.com\n")
    df = load_csv(str(valid_file))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert "customer_id" in df.columns

# tests for clean phone
def test_clean_phone_dashes():
    assert clean_phone("416-555-1234") == "(416) 555-1234"


def test_clean_phone_dots():
    assert clean_phone("416.555.1234") == "(416) 555-1234"


def test_clean_phone_with_country_code():
    assert clean_phone("1-416-555-1234") == "(416) 555-1234"


def test_clean_phone_plain_digits():
    assert clean_phone("4165551234") == "(416) 555-1234"


def test_clean_phone_invalid_too_short():
    assert clean_phone("12345") is None


def test_clean_phone_invalid_non_string():
    assert clean_phone(1234567890) is None


# tests for validate_email

def test_validate_email_valid():
    assert validate_email("user@example.com") is True


def test_validate_email_valid_with_subdomain():
    assert validate_email("user@mail.example.co.uk") is True


def test_validate_email_missing_at():
    assert validate_email("userexample.com") is False


def test_validate_email_missing_domain():
    assert validate_email("user@") is False


def test_validate_email_empty_string():
    assert validate_email("") is False


def test_validate_email_non_string():
    assert validate_email(None) is False


def test_validate_email_spaces():
    assert validate_email("user @example.com") is False