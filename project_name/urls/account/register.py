#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === urls.account.register -----------------------------------------------===
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

""

from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template

from registration.views import register

urlpatterns = patterns('',
  # URL patterns for new account registration, using Django-registration's
  # default backend. This registration backend has the following workflow for
  # new user account registration:
  #
  #   1. User visits the registration_register URL and fills out the new
  #      account registration form, which includes such information as the
  #      desired username, password, and email address to associate with the
  #      account.
  #
  #   2. If registration is open (settings.REGISTRATION_OPEN is True), upon
  #      successful submission of the new account registration form the user
  #      is redirected to the registration_done URL which informs them that an
  #      activation link has been sent to the email address they specified.
  #
  #      If registration is closed (settings.REGISTRATION_OPEN is False), upon
  #      successful submission of the new account registration form the user
  #      is redirected to the registration_disallowed URL which thanks them
  #      for their interest, informs that the site is currently closed for new
  #      users, that their email has been added to a wait-list, etc.
  #
  #   3. From their email client, the user clicks on the activation link which
  #      takes them to a unique registration_activate URL. Their account is
  #      then activated, and they are redirected to
  #      registration_activation_complete.
  #
  #   4. Registration is finished and the user may now login.
  #
  # NOTE: Activation urls and their documentation can be found in the
  #       {{ project_name }}.urls.account.activate module.
  url(r'^$',
    register, {
      # The dotted Python import path to the backend class to use. The backend
      # provides the workflow and logic for new user account registration. The
      # default backend, which we are using, requires that the user verify
      # ownership of the email address they provide through an activation
      # email before the user account can be used. See the Django-registration
      # documentation and source code (it's quite simple) for more
      # information.
      'backend':        'registration.backends.default.DefaultBackend',
      # The URL to redirect the user to upon successful completion of the new
      # account registration form. If None, the redirect URL is provided by
      # the registration backend.
      'success_url':    None,
      # The form class to use for registration. If not supplied, this will be
      # retrieved from the registration backend.
      'form_class':     None,
      # URL to redirect to if registration is not permitted for the current
      # HttpRequest. Must be a value which can legally be passed to
      # django.shortcuts.redirect. If not supplied, this will be whatever URL
      # corresponds to the named URL pattern registration_disallowed.
      'disallowed_url': 'registration_disallowed',
      # The template used to show the new account registration form to the
      # user. It receives a ‘form’ variable provided by the backend as
      # context.
      'template_name':  'account/registration.html',
    }, name='registration_register'),

  # If the setting REGISTRATION_OPEN is False, new user registrations are not
  # allowed and an attempt to register is redirected to a page which explains
  # the situation, the registration_disallowed URL.
  url(r'^closed/$',
    direct_to_template, {
      # The full name of the template shown after the user has successfully
      # submitted a new account registration form while registration is
      # closed. The template is given a RequestContext without any special
      # context variables.
      'template': 'account/registration_closed.html'
    }, name='registration_disallowed'),

  # The page shown after the user has completed the new account registration
  # form (if the setting REGISTRATION_OPEN is not False). In the case of the
  # default registration backend, its purpose is to tell the user that an
  # activation email has been sent to the email account they specified.
  #
  # FIXME: If we ever do our own backend, we should change the name of this
  #        URL to registration_done in order to match with the naming scheme
  #        of django.contrib.auth. Unfortunately it is too messy to do so now
  #        as the default registration backend explicitly references this name
  #        in the post_registration_redirect() method.
  url(r'^complete/$',
    direct_to_template, {
      # The full name of the template shown after the user has successfully
      # submitted a new account registration form and an activation email has
      # been sent. The template is given a RequestContext without any special
      # context variables.
      'template': 'account/registration_complete.html'
    }, name='registration_complete'),
)

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
