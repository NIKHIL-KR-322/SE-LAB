
import pytest

from attendance_eligibility import (
    attendance_percent,
    exam_eligibility,
    attendance_warning
)


# =========================================
# ATTENDANCE PERCENTAGE - BRANCH TESTS
# =========================================

def test_total_classes_zero():
    with pytest.raises(ValueError):
        attendance_percent(10, 0, 0)


def test_total_classes_negative():
    with pytest.raises(ValueError):
        attendance_percent(10, -5, 0)


def test_valid_total_classes():
    assert attendance_percent(30, 40, 0) == 75


def test_attended_negative():
    with pytest.raises(ValueError):
        attendance_percent(-1, 40, 0)


def test_attended_greater_than_total():
    with pytest.raises(ValueError):
        attendance_percent(45, 40, 0)


def test_attended_valid():
    assert attendance_percent(20, 40, 0) == 50


def test_medical_leave_more_than_five():
    assert attendance_percent(20, 40, 10) == 62


def test_medical_leave_equal_to_five():
    assert attendance_percent(20, 40, 5) == 62


def test_credited_attendance_exceeds_total():
    assert attendance_percent(38, 40, 5) == 100


def test_credited_attendance_does_not_exceed_total():
    assert attendance_percent(20, 40, 2) == 55


# =========================================
# EXAM ELIGIBILITY - BRANCH TESTS
# =========================================

def test_fees_not_paid():
    assert exam_eligibility(90, False, False) == "fees pending"


def test_fees_paid():
    assert exam_eligibility(90, False, True) == "eligible"


def test_percentage_exactly_75():
    assert exam_eligibility(75, False, True) == "eligible"


def test_percentage_below_75():
    assert exam_eligibility(70, True, True) == "eligible"


def test_percentage_exactly_65_with_condonation():
    assert exam_eligibility(65, True, True) == "eligible"


def test_condonation_not_available():
    assert exam_eligibility(65, False, True) == "condonation required"


def test_percentage_below_65():
    assert exam_eligibility(64, False, True) == "detained"


# =========================================
# ATTENDANCE WARNING - BRANCH TESTS
# =========================================

def test_percentage_above_85():
    assert attendance_warning(90, 2) is None


def test_percentage_exactly_85():
    assert attendance_warning(85, 2) is None


def test_percentage_below_85():
    assert attendance_warning(80, 2) == "reminder"


def test_percentage_below_75():
    assert attendance_warning(70, 6) == "critical"


def test_weeks_left_more_than_four():
    assert attendance_warning(74, 5) == "critical"


def test_weeks_left_exactly_four():
    assert attendance_warning(74, 4) == "final notice"


def test_percentage_exactly_75():
    assert attendance_warning(75, 2) == "reminder"
