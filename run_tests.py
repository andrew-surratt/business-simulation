#!/usr/bin/env python
"""
Local Django script to run all tests.

Usage:
    python run_tests.py
    python run_tests.py --verbose
    python run_tests.py business
    python run_tests.py business.tests.IndexViewTest
    python run_tests.py business.tests.IndexViewTest.test_index_view_status_code
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'business_dashboard.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=True, keepdb=False)
    
    # Get test label from command line arguments, default to all tests
    test_labels = sys.argv[1:] if len(sys.argv) > 1 else ['business']
    
    failures = test_runner.run_tests(test_labels)
    
    sys.exit(bool(failures))
