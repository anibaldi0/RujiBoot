# path: utils/breadcrumb_util.py
# Breadcrumb navigation state for CLI menus

_breadcrumb_path = []

def reset_breadcrumb():
    """
    Clears the breadcrumb path to start fresh (usually at main menu).
    """
    global _breadcrumb_path
    _breadcrumb_path = []

def add_breadcrumb(entry: str):
    """
    Adds a new entry to the breadcrumb path.

    Args:
        entry (str): Name of the current submenu or step
    """
    global _breadcrumb_path
    _breadcrumb_path.append(entry)

def pop_breadcrumb():
    """
    Removes the last breadcrumb entry (used when returning).
    """
    global _breadcrumb_path
    if _breadcrumb_path:
        _breadcrumb_path.pop()

def get_breadcrumb_str() -> str:
    """
    Returns the current breadcrumb path as a formatted string.

    Returns:
        str: Formatted breadcrumb (e.g. 'Main > Write ISO > Persistence')
    """
    return " > ".join(_breadcrumb_path)
