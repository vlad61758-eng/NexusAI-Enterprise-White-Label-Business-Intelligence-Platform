import pytest
import os
import shutil
from pathlib import Path
import sys

# Add parent directory to path so we can import the scripts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from organizer import organize_directory, FILE_CATEGORIES
from b2b_scraper import save_to_csv

# Test for Smart Data Organizer
def test_organizer(tmp_path):
    # Create dummy files
    (tmp_path / "test1.jpg").touch()
    (tmp_path / "test2.png").touch()
    (tmp_path / "test_doc.pdf").touch()
    (tmp_path / "test_script.py").touch()
    (tmp_path / "unknown.xyz").touch()

    # Run the organizer
    organize_directory(str(tmp_path))

    # Assert folders were created and files moved
    assert (tmp_path / "Images").exists()
    assert (tmp_path / "Images" / "test1.jpg").exists()
    assert (tmp_path / "Images" / "test2.png").exists()

    assert (tmp_path / "Documents").exists()
    assert (tmp_path / "Documents" / "test_doc.pdf").exists()

    assert (tmp_path / "Scripts").exists()
    assert (tmp_path / "Scripts" / "test_script.py").exists()

    assert (tmp_path / "Others").exists()
    assert (tmp_path / "Others" / "unknown.xyz").exists()

def test_b2b_scraper_save_to_csv(tmp_path):
    # Mock data
    emails = ["test@example.com", "info@company.com"]
    output_file = tmp_path / "test_leads.csv"

    # Change working directory so file is saved correctly if absolute path is not passed (though we pass absolute here)
    save_to_csv(emails, str(output_file))

    assert output_file.exists()
    content = output_file.read_text()
    assert "Email" in content
    assert "test@example.com" in content
    assert "info@company.com" in content

# We won't test the scraper network requests directly in unit tests to avoid flakiness,
# nor the bot which requires an event loop and active tokens, but we verified their compilation.
