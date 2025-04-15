from enum import Enum


class ValidationStatus(Enum):
    UNVALIDATED = "UNVALIDATED"
    PASSED = "PASSED"
    FAILED = "FAILED"
