#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === packagename.urls.account.activate -----------------------------------===
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
from django.views.generic.simple import direct_to_template

from registration.views import activate

urlpatterns = patterns('',
  # The activation process is quite simple: the user clicks on a
  # registration_activate link from within their email client, and the mere
  # act of requesting the page results in the account being activated. The
  # user is then redirected to the registration_activation_complete and is
  # informed of the activation of their account.
  #
  # NOTE: A full description of the registration and activation workflow, as
  #       well as the registration URL's can be found in the
  #       urls.account.register module.

  # NOTE: I've tried to layout the URL's in a logical ordering, but in this
  #       case registration_activation_complete must come before
  #       registration_activate (which follows) as the regular expression for
  #       the latter matches the former.
  #
  # The page shown after the user has successfully activated their account.
  url(r'^complete/$',
    direct_to_template, {
      # The template to be used to inform the user that their account has been
      # successfully activated. The template is passed a RequestContext
      # without any special context variables.
      'template': 'account/activation_complete.html'
    }, name='registration_activation_complete'),

  # The URL handler for the activation link sent via email to the new user as
  # part of the new account registration process. See urls.account.register
  # for more information.
  #
  # NOTE: Activation keys get matched by \w+ instead of the more specific
  #       [a-fA-F0-9]{40} because a bad activation key should still get to the
  #       view; that way it can return a sensible “invalid key” message
  #       instead of a confusing 404.
  url(r'^(?P<activation_key>\w+)/$',
    activate, {
      # The dotted Python import path to the backend class to use. The backend
      # provides the workflow and logic for new user account registration. The
      # default backend, which we are using, handles the logic of new account
      # activation. See the Django-registration documentation and source code
      # (it's quite simple) for more information.
      'backend':       'registration.backends.default.DefaultBackend',
      # The template used to display an error if activation is not successful.
      # The template is given a RequestContext without any special context
      # variables.
      'template_name': 'account/activation_failed.html',
      # The URL to redirect the user to upon successful activation of the new
      # account. If None, the redirect URL is provided by the registration
      # backend.
      'success_url':   None,
    }, name='registration_activate'),
)

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
