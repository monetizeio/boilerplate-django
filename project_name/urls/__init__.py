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

"Root URL configuration."

# Django.core
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template, redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # FIXME: The URL's below are grouped for readability. At some point it may
    #        make sense for performance reasons to reorder them based on
    #        frequency. However we should wait until we at least have the
    #        capability to measure the supposed performance increase; premature
    #        optimization that affects maintainability is never a good idea!

    ###################
    # Admin Interface #
    ###################

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    ###########################
    # User Account Management #
    ###########################

    # URL patterns for the views provided by django.contrib.auth and
    # Django-registration. These default views accomplish the following user
    # account management actions:
    #
    #     * User login at “login/”.
    #     * User logout at “logout/”.
    #     * The two-step password change at “account/password/change/”.
    #     * The four-step password reset at “account/password/reset/”.
    #     * The four-step, two-outcome new user account registration and
    #       activation at “register/” and “account/activate/”.

    url(r'^login/',                   include('project_name.urls.auth.login')),
    url(r'^logout/',                  include('project_name.urls.auth.logout')),
    url(r'^register/',                include('project_name.urls.account.register')),
    url(r'^account/password/change/', include('project_name.urls.auth.password.change')),
    url(r'^account/password/reset/',  include('project_name.urls.auth.password.reset')),
    url(r'^account/activate/',        include('project_name.urls.account.activate')),

    ####################
    ## Template Pages ##
    ####################

    # The landing page for the website.
    url(r'^$',
        direct_to_template, {
            'template': 'base.html.j2'
        }, name='homepage'),

    ################
    ## Info Files ##
    ################
    (r'^favicon.ico$',          redirect_to, {'permanent': False, 'url': '/static/images/favicon.ico'}),
    (r'^apple-touch-icon.png$', redirect_to, {'permanent': False, 'url': '/static/images/apple-touch-icon.png'}),
    (r'^crossdomain.xml$',      redirect_to, {'permanent': False, 'url': '/static/info/crossdomain.xml'}),
    (r'^humans.txt$',           redirect_to, {'permanent': False, 'url': '/static/info/humans.txt'}),
    (r'^robots.txt$',           redirect_to, {'permanent': False, 'url': '/static/info/robots.txt'}),

    ######################
    # Media File Hosting #
    ######################

    # In a production environment media files are hosted by the static web
    # server/gateway directly. For development purposes, and in case a request
    # slips through, media files are hosted by the Django static server as well.
    (r'^media\/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
        'show_indexes':  False,
    }),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

# 403 (permission denied), 404 (page not found), and 500 (server error) handlers
# are customized to load our Jinja2 templates instead:
from django.views.defaults import permission_denied
def handler403(request, template_name='403.html.j2'):
    permission_denied(request, template_name)
from django.views.defaults import page_not_found
def handler404(request, template_name='404.html.j2'):
    page_not_found(request, template_name)
from django.views.defaults import server_error
def handler500(request, template_name='500.html.j2'):
    server_error(request, template_name)

#
# End of File
#
