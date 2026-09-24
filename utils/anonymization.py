import hashlib


def anonymize_employee_id(employee_id: str) -> str:
    """
    Convert an employee ID into a consistent anonymous identifier.
    """

    hashed_id = hashlib.sha256(
        employee_id.encode("utf-8")
    ).hexdigest()

    return f"EMP-{hashed_id[:8].upper()}"