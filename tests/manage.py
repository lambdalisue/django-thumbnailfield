#!/usr/bin/env python
#
# This is compatible version of manage.py
# This manage.py support all django versions
#
import os, sys

# Add external PYTHON_PATH
root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if os.path.join(root, 'src') not in sys.path:
    sys.path.insert(0, os.path.join(root, 'src'))

# configure DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

try:
    # django >= 1.4
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
except ImportError:
    # django < 1.4
    from django.core.management import execute_manager
    try:
        import settings # Assumed to be in the same directory.
    except ImportError:
        import sys
        sys.stderr.write("Error: Can't find the file 'settings.py' in the "
                         "directory containing %r. It appears you've "
                         "customized things.\n"
                         "You'll have to run django-admin.py, passing it your "
                         "settings module.\n"
                         "(If the file settings.py does indeed exist, it's "
                         "causing an ImportError somehow.)\n" % __file__)
        sys.exit(1)
    execute_manager(settings)
