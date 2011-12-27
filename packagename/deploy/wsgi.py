#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === packagename.deploy.wsgi ---------------------------------------------===
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

"A deployment script that sets up a proper environment for hosting this project as a WSGI application. Simply point your WSGI-enabled web server at this module (with the root package accessible from ``sys.path``), and it will handle the rest."

# The settings environment variable needs to be set so that Django knows where
# to find our production settings. This would be necessary anyway, but it is
# especially required in our case because the settings module is not in its
# default location.
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'packagename.settings.production'

# Django provides a handler class that works as our WSGI application without
# modification.
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
