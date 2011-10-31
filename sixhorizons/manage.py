#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === sixhorizons/manage.py -----------------------------------------------===
# Copyright © 2011, RokuSigma Inc. (Mark Friedenbach <mark@roku-sigma.com>)
# as an unpublished work.
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

""

# PROJECT_DIRECTORY is the directory on the file system which contains the
# Django project this manage.py file is a part of.
import os
PROJECT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

# We need our Django project package to be accessible from the Python path, as
# we do double-duty as both a Django project and application:
import sys
sys.path.insert(0, os.path.abspath(os.path.join(PROJECT_DIRECTORY, '..')))

from django.core.management import execute_manager
import imp
try:
  import settings.development as settings
except ImportError:
  import sys
  sys.stderr.write("Error: Can't find the file 'settings/development.py' relative to the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
  sys.exit(1)

if __name__ == "__main__":
  execute_manager(settings)

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
