import os
import pytest
import pandas as pd
from bot import check_keywords, save_lead_to_excel, EXCEL_FILE, KEYWORDS

def setup_module(module):
    # Ensure a clean slate for the test Excel file
    if os.path.exists(EXCEL_FILE):
        os.remove(EXCEL_FILE)

def teardown_module(module):
    # Clean up after tests
    if os.path.exists(EXCEL_FILE):
        os.remove(EXCEL_FILE)

def test_check_keywords_match(monkeypatch):
    # Mock the KEYWORDS list directly in the module
    monkeypatch.setattr('bot.KEYWORDS', ['lead', 'b2b', 'marketing'])

    assert check_keywords("We need a new b2b solution") == "b2b"
    assert check_keywords("Looking for good LEAD gen tools") == "lead"
    assert check_keywords("Marketing is important") == "marketing"

def test_check_keywords_no_match(monkeypatch):
    monkeypatch.setattr('bot.KEYWORDS', ['lead', 'b2b', 'marketing'])

    assert check_keywords("Hello world") is None
    assert check_keywords("Just another message") is None

def test_check_keywords_empty(monkeypatch):
    monkeypatch.setattr('bot.KEYWORDS', ['lead', 'b2b', 'marketing'])

    assert check_keywords("") is None
    assert check_keywords(None) is None

def test_save_lead_to_excel():
    # Call the function to create/append
    save_lead_to_excel(
        username="testuser",
        name="Test User",
        matched_keyword="b2b",
        message_snippet="Need a b2b tool...",
        chat_title="Test Group",
        message_link="https://t.me/testgroup/123"
    )

    # Verify file exists
    assert os.path.exists(EXCEL_FILE)

    # Read back and verify data
    df = pd.read_excel(EXCEL_FILE)
    assert len(df) == 1
    assert df.iloc[0]['Username'] == "@testuser"
    assert df.iloc[0]['Matched Keyword'] == "b2b"
    assert df.iloc[0]['Message Snippet'] == "Need a b2b tool..."

    # Append another lead
    save_lead_to_excel(
        username="anotheruser",
        name="Another User",
        matched_keyword="lead",
        message_snippet="Looking for lead gen...",
        chat_title="Test Group 2",
        message_link="https://t.me/testgroup2/456"
    )

    # Verify append worked
    df = pd.read_excel(EXCEL_FILE)
    assert len(df) == 2
    assert df.iloc[1]['Username'] == "@anotheruser"
    assert df.iloc[1]['Matched Keyword'] == "lead"
