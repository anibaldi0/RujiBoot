# path: utils/generic_validator_util.py
# Description: Centralized, robust and parameterized input validator for RujiBoot

class GenericValidator:
    def __init__(self):
        pass

    def validate_input(
        self,
        user_input: str,
        expected_type: str = "str",               # "int", "str", "confirm", or "custom"
        expected_value: str = None,               # e.g., "YES"
        allowed_values: list = None,              # e.g., ["1", "2", "3"]
        allowed_chars: str = None,                # e.g., "abc123_"
        max_length: int = None,
        min_value: int = None,
        max_value: int = None,
        allow_empty: bool = False
    ):
        """
        Validates input generically based on expected type and constraints.

        Args:
            user_input (str): Input string to validate
            expected_type (str): "int", "str", "confirm", or "custom"
            expected_value (str): Exact string expected (case-insensitive)
            allowed_values (list): List of accepted values (for string type)
            allowed_chars (str): Allowed characters (only for str)
            max_length (int): Max allowed length (for str)
            min_value (int): Minimum value (for int)
            max_value (int): Maximum value (for int)
            allow_empty (bool): Whether empty input is allowed

        Returns:
            Union[str, int, bool]: Validated and cleaned input

        Raises:
            ValueError: If the input is invalid or empty when not allowed
        """
        cleaned = user_input.strip()

        # Empty check
        if not cleaned and not allow_empty:
            raise ValueError("[!] Input cannot be empty. Please enter a value.")

        # Type: confirm (y/n)
        if expected_type == "confirm":
            if cleaned.lower() not in ["y", "n"]:
                raise ValueError("[!] Invalid input. Expected 'y' or 'n'.")
            return cleaned.lower() == "y"

        # Type: custom (e.g., must type 'YES' or 'ERASE')
        if expected_type == "custom":
            if not expected_value:
                raise ValueError("[!] Validator misconfiguration: expected_value is required for type 'custom'.")
            if cleaned.upper() != expected_value.upper():
                raise ValueError(f"[!] You must type '{expected_value.upper()}' to proceed.")
            return True

        # Type: int
        if expected_type == "int":
            try:
                value = int(cleaned)
            except ValueError:
                raise ValueError("[!] Invalid input. Expected an integer number.")
            if min_value is not None and value < min_value:
                raise ValueError(f"[!] Value must be >= {min_value}")
            if max_value is not None and value > max_value:
                raise ValueError(f"[!] Value must be <= {max_value}")
            return value

        # Type: str (default)
        if expected_type == "str":
            if allowed_chars and any(c not in allowed_chars for c in cleaned):
                raise ValueError(f"[!] Invalid characters. Allowed: {allowed_chars}")
            if max_length and len(cleaned) > max_length:
                raise ValueError(f"[!] Input too long. Maximum: {max_length} characters.")
            if allowed_values and cleaned not in allowed_values:
                raise ValueError(f"[!] Invalid input. Expected one of: {allowed_values}")
            return cleaned

        raise ValueError("[!] Unknown expected_type passed to validator.")
