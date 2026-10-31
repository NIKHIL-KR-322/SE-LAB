@'
# L6_L7_62 — Attendance Eligibility

Lab 6: Code and Branch Coverage

## About

A small Python module that calculates a student's attendance percentage with medical leave, decides exam eligibility and chooses which attendance warning to send.

## Files

| File | Description |
|------|-------------|
| `attendance_eligibility.py` | The module under test |
| `test_attendance_eligibility.py` | Starter test file |
| `CodeCoverageTest_PES2UG25CS815_application.py` | Test cases for code coverage |
| `BranchCoverageTest_PES2UG25CS815_application.py` | Test cases for branch coverage |

## Coverage Results

- Code Coverage: 100%
- Branch Coverage: 100%
- Branch tests passed: 22

## Tools Used

- Python
- pytest
- coverage.py

## Running the Tests

Run code coverage:

```bash
coverage erase
coverage run -m pytest LAB6/CodeCoverageTest_PES2UG25CS815_application.py
coverage report -m LAB6/attendance_eligibility.py## Branch Coverage Analysis

Branch coverage measures whether every possible decision outcome (True and False) in the program has been executed by the test cases.

### Branch Coverage Test File

`BranchCoverageTest_PES2UG25CS815_application.py`

### Test Execution

```bash
coverage erase
coverage run --branch -m pytest LAB6/BranchCoverageTest_PES2UG25CS815_application.py -v
coverage report -m LAB6/attendance_eligibility.py
