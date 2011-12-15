#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === packagename.urls.auth.password.change -------------------------------===
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
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import password_change, password_change_done

urlpatterns = patterns('',
  # Allows a user to change their password.
  #
  # The workflow for a password change request is as follows:
  #
  #   1. The user visits the auth_password_change URL. If the user has not
  #      authenticated, they are redirected to auth_login for authentication
  #      first.
  #   2. The user completes and successfully submits (POST to the
  #      auth_password_change URL) the password change form, which by default
  #      contains the old password (once) and the new password (twice).
  #   3. The user is redirected to ‘post_change_redirect’ (if specified) or to
  #      auth_password_change_done (the default).
  url(r'^$',
    password_change, {
      # The full name of the template used to display the password change form
      # to the user. The template is given a RequestContext with just one
      # variable, ‘form’, which contains an instance of
      # ‘password_change_form’.
      'template_name':        'auth/password_change.html',
      # A hard-coded redirect to be used after the password change form has
      # been successfully submitted. If None, the reverse URL lookup of
      # password_change_done is used instead.
      'post_change_redirect': None,
      # The form which is presented to the user for a password change request.
      # See the django.contrib.auth documentation for details on what specific
      # behavior is expected of this form object.
      'password_change_form': PasswordChangeForm,
    }, name='auth_password_change'),

  # The page shown after a user has changed their password.
  url(r'^done/$',
    password_change_done, {
      # The full name of the template shown after the user has successfully
      # changed their password. The template is given a RequestContext without
      # any special context variables.
      'template_name': 'auth/password_change_complete.html',
    }, name='auth_password_change_done'),
)

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
