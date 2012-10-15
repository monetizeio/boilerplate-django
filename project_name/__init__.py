#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ===----------------------------------------------------------------------===
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
Brief description of your package goes here.

To get started, try exploring the following modules:

  `project_name.admin`     Django-admin interface
  `project_name.db`        Django model definitions
  `project_name.deploy`    WSGI deploy scripts
  `project_name.settings`  Development, testing, and production settings
  `project_name.urls`      Django URL specifications
  `project_name.tests`     Unit tests of package-wide features

And the following scripts/directories:

  `manage.py`             Command-line management script
  `static`                CSS, JavaScript, and other media files
  `templates`             HTML and email template files
"""

__all__ = [
  'VERSION',
  'get_version',
]

VERSION = (0,0,0, 'alpha', 0)

def get_version():
  version = '%s.%s' % (VERSION[0], VERSION[1])
  if VERSION[2]:
    version = '%s.%s' % (version, VERSION[2])
  if VERSION[3:] == ('alpha', 0):
    version = '%s pre-alpha' % version
  else:
    if VERSION[3] != 'final':
      version = "%s %s" % (version, VERSION[3])
      if VERSION[4] != 0:
        version = '%s %s' % (version, VERSION[4])
  return version

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
