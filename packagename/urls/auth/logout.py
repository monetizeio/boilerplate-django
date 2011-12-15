#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === packagename.urls.auth.logout ----------------------------------------===
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

from django.conf.urls.defaults import patterns, url
from django.contrib.auth.views import logout

urlpatterns = patterns('',
  # Logs the user out.
  #
  # FIXME: ‘redirect_field_name’ should be localized in “logout/”.
  url(r'^$',
    logout, {
      # The GET field which may contain a URL to redirect to after logout. If
      # this field is not set, the hard-coded ‘next_page’ parameter used
      # instead. If ‘next_page’ is None, the template specified by the
      # ‘template_name’ parameter is rendered and returned.
      'redirect_field_name': 'next',
      # The hard-coded URL to redirect to after a successful logout, assuming
      # the ‘redirect_field_name’ is empty or not specified (see above).
      'next_page':           None,
      # The full name of the template used after logging the user out if
      # neither a run-time nor a hard-coded redirect is requested (see above).
      # The template receives a RequestContext with three additional
      # variables: ‘site’, ‘site_name’, and ‘title’ (see the documentation in
      # the template file for details).
      'template_name':       'auth/logout.html',
    }, name='auth_logout'),
)

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
