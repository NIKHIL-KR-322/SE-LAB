
import pytest

from attendance_eligibility import (
    attendance_percent,
    exam_eligibility,
    attendance_warning
)


# -----------------------------------------
# ATTENDANCE PERCENTAGE TEST CASES
# -----------------------------------------

def test_invalid_total_classes():
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(10, 0, 0)


def test_negative_total_classes():
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(10, -5, 0)


def test_negative_attendance():
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(-1, 40, 0)


def test_attendance_greater_than_total():
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(45, 40, 0)


def test_medical_leave_capped_at_five():
    assert attendance_percent(20, 40, 10) == 62


def test_credited_attendance_capped_at_total():
    assert attendance_percent(38, 40, 6) == 100


# -----------------------------------------
# EXAM ELIGIBILITY TEST CASES
# -----------------------------------------

def test_fees_pending():
    assert exam_eligibility(90, False, False) == "fees pending"


def test_direct_exam_eligibility():
    assert exam_eligibility(80, False, True) == "eligible"


def test_condonation_approved():
    assert exam_eligibility(70, True, True) == "eligible"


def test_condonation_required():
    assert exam_eligibility(70, False, True) == "condonation required"


def test_student_detained():
    assert exam_eligibility(60, False, True) == "detained"


# -----------------------------------------
# ATTENDANCE WARNING TEST CASES
# -----------------------------------------

def test_no_warning():
    assert attendance_warning(90, 2) is None


def test_critical_warning():
    assert attendance_warning(70, 6) == "critical"


def test_final_notice():
    assert attendance_warning(70, 2) == "final notice"


def test_reminder_warning():
    assert attendance_warning(80, 3) == "reminder"
