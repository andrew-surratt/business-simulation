#!/usr/bin/env python
"""
Local Django script to run all tests with coverage reporting.

Prerequisites:
    pip install coverage

Usage:
    python run_tests_coverage.py
    
This will:
    1. Run all tests with coverage tracking
    2. Generate a terminal report
    3. Generate an HTML report in htmlcov/index.html
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner
import coverage

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'business-dashboard.settings'

    # Start coverage
    cov = coverage.Coverage(
        source=['business'],
        omit=['business/tests.py'],
    )
    cov.start()

    django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=True, keepdb=False)
    
    # Run all business app tests
    failures = test_runner.run_tests(['business'])
    
    # Stop coverage and generate reports
    cov.stop()
    cov.save()
    
    print("\n" + "=" * 70)
    print("COVERAGE REPORT")
    print("=" * 70)
    
    # Terminal report
    cov.report()
    
    # HTML report
    html_dir = 'htmlcov'
    cov.html_report(directory=html_dir)
    print(f"\nHTML coverage report generated in: {html_dir}/index.html")
    print("=" * 70)
    
    sys.exit(bool(failures))
