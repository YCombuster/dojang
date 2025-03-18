"""
A stub implementation of psycopg2 module.
This allows the code to import without having the actual psycopg2 package installed.
For development purposes only.
"""

# This is just a minimal stub to prevent import errors
# It won't actually connect to a database

def connect(*args, **kwargs):
    """Stub for psycopg2.connect"""
    print("WARNING: Using psycopg2 stub - no actual database connection will be made")
    return None 