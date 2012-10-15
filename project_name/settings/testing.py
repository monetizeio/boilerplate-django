#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === settings.testing ----------------------------------------------------===
# Copyright © 2011-2012, RokuSigma Inc. and contributors as an unpublished
# work. See AUTHORS for details.
#
# RokuSigma Inc. (the “Company”) Confidential
#
# NOTICE: All information contained herein is, and remains the property of the
# Company. The intellectual and technical concepts contained herein are
# proprietary to the Company and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained from the
# Company. Access to the source code contained herein is hereby forbidden to
# anyone except current Company employees, managers or contractors who have
# executed Confidentiality and Non-disclosure agreements explicitly covering
# such access.
#
# The copyright notice above does not evidence any actual or intended
# publication or disclosure of this source code, which includes information
# that is confidential and/or proprietary, and is a trade secret, of the
# Company. ANY REPRODUCTION, MODIFICATION, DISTRIBUTION, PUBLIC PERFORMANCE,
# OR PUBLIC DISPLAY OF OR THROUGH USE OF THIS SOURCE CODE WITHOUT THE EXPRESS
# WRITTEN CONSENT OF THE COMPANY IS STRICTLY PROHIBITED, AND IN VIOLATION OF
# APPLICABLE LAWS AND INTERNATIONAL TREATIES. THE RECEIPT OR POSSESSION OF
# THIS SOURCE CODE AND/OR RELATED INFORMATION DOES NOT CONVEY OR IMPLY ANY
# RIGHTS TO REPRODUCE, DISCLOSE OR DISTRIBUTE ITS CONTENTS, OR TO MANUFACTURE,
# USE, OR SELL ANYTHING THAT IT MAY DESCRIBE, IN WHOLE OR IN PART.
# ===----------------------------------------------------------------------===

"""
Settings file for use while running unit tests during development and on the
staging server. This settings file attempts to match as closely as possible
the production settings, while providing a few configuration tweaks that are
necessary to setup a sandboxed settings environment.
"""

# Import the production settings, which will be used as the base
# configuration:
from .common import *

# An in-memory SQLite database is sufficient for testing purposes in a local
# development environment. On a continuous integration server, the production
# database server should be used instead. The build scripts can adjust these
# settings by specifing their own settings file.
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
  }
}

# Run syncdb and migrate on first run if an in-memory database is used.
MIDDLEWARE_CLASSES = (
  'django_patterns.middleware.SyncDBOnStartupMiddleware',
  ) + MIDDLEWARE_CLASSES

# The django_nose test runner uses nose under the hood (obviously) and is
# better than the default Django test runner in that it can discover and run
# tests in source files spread throughout the project (this allows tests to be
# written near the code that being tested), generates better reports, and has
# a better framework for extending its functionality through plug-ins.
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Add the applications necessary for unit test discovery:
for app in (
  # Django-extensions is a dependency of Django-patterns, and provides the
  # ever-useful shell_plus command for launching an ipython interactive
  # development shell.
  'django_extensions',

  # Our Django application, which provides setup and utilities for assisting
  # test discovery.
  'django_patterns',

  # Replaces the default Django test runner with nose's, which is much more
  # capable at auto-discovery of tests and provides a better framework for
  # report generation and plug-in functionality.
  'django_nose',
  ):
  if app not in INSTALLED_APPS:
    INSTALLED_APPS += (app,)

# Use django_patterns to detect embedded Django test applications, and add
# them to our INSTALLED_APPS:
from django_patterns.test.discover import discover_test_apps
apps = discover_test_apps("{{ project_name }}")
if apps:
  for app in apps:
    INSTALLED_APPS += (app,)

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
