#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright © 2011-2013, RokuSigma Inc. and contributors as an unpublished
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
#

from django.conf.urls import patterns, url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login

urlpatterns = patterns('',
    # Authenticates and logs a user in.
    #
    # FIXME: ‘redirect_field_name’ should be localized in “login/”
    url(r'^$',
        login, {
            # The full name of the template file used to display the login form to
            # the user. The template is given a RequestContext with four extra
            # variables: ‘form’, ‘next’, ‘site’, and ‘site_name’ (see the
            # documentation in the template file for details).
            'template_name':       'auth/login.html.j2',
            # The GET field which may contain a URL to redirect to after logout. If
            # this field is not set, the LOGIN_REDIRECT_URL setting is used instead.
            'redirect_field_name': 'next',
            # The form which is presented to the user for authentication. It may be
            # overriden in the context of alternative authentication methods. See
            # the django.contrib.auth documentation for details on what specific
            # behavior is expected of this form object.
            'authentication_form': AuthenticationForm,
        }, name='auth_login'),
)

#
# End of File
#
