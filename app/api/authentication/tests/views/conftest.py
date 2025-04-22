import os
import sys
import django

# Add project root to PYTHONPATH
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
)

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

# Initialize Django
django.setup()
