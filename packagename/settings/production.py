#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === packagename.settings.production -------------------------------------===
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

"Base (production) Django settings for this project."

###############
# Environment #
###############

# PROJECT_DIRECTORY is the directory on the file system which contains the
# Django project this settings file is a part of. It is used so many times
# that it deserves its own variable for efficiency and clarity.
import os
PROJECT_DIRECTORY = os.path.abspath(
  os.path.join(os.path.dirname(__file__), '..'))

##################
# Debug Settings #
##################

DEBUG = True
TEMPLATE_DEBUG = DEBUG

##########################
# Administrative Contact #
##########################

ADMINS = (
  # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

#########################
# Session Configuration #
#########################

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'please replace this with your own very long sekret'

##########################
# Database Configuration #
##########################

DATABASES = {
  'default': {
    # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    'ENGINE': 'django.db.backends.sqlite3',
    # Or path to database file if using sqlite3.
    'NAME': os.path.abspath(os.path.join(PROJECT_DIRECTORY, '..', 'db', 'sqlite.db')),
    # Not used with sqlite3.
    'USER': '',
    # Not used with sqlite3.
    'PASSWORD': '',
    # Set to empty string for localhost. Not used with sqlite3.
    'HOST': '',
    # Set to empty string for default. Not used with sqlite3.
    'PORT': '',
  }
}

#############
# Timezones #
#############

# Local time zone for this installation. Choices can be found here:
# <http://en.wikipedia.org/wiki/List_of_tz_zones_by_name>, although not all
# choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same timezone
# as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

#########################################
# Internationalization and Localization #
#########################################

# Language code for this installation. All choices can be found here:
# <http://www.i18nguy.com/unicode/language-identifiers.html>.
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not to
# load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

##########################
# Template Configuration #
##########################

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
#  'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
  # Put strings here, like "/home/html/django_templates" or
  #   "C:/www/django/templates".
  # Always use forward slashes, even on Windows.
  # Don't forget to use absolute paths, not relative paths.
  os.path.abspath(os.path.join(PROJECT_DIRECTORY, '..', 'templates')),
)

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.contrib.auth.context_processors.auth",
  "django.core.context_processors.csrf",
  "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
  "django.core.context_processors.static",
  "django.contrib.messages.context_processors.messages",
  "context_extras.context_processors.current_site",
  "context_extras.context_processors.project_settings",
  "context_extras.context_processors.protocol_host",
)

############################
# Middleware Configuration #
############################

MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

#####################
# URL Configuration #
#####################

ROOT_URLCONF = 'packagename.urls'

######################
# WSGI Configuration #
######################

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'packagename.deploy.wsgi.application'

#######################
# Email Configuration #
#######################

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_HOST_USER = "no-reply@roku-sigma.com"
EMAIL_HOST_PASSWORD = "X8wCeeX6rS93"
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = "no-reply@roku-sigma.com"

#########################
# Logging Configuration #
#########################

# A sample logging configuration. The only tangible logging performed by this
# configuration is to send an email to the site admins on every HTTP 500 error
# when DEBUG=False. See <http://docs.djangoproject.com/en/dev/topics/logging>
# for more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#############################
# Application Configuration #
#############################

INSTALLED_APPS = (
  # The project itself is also an application. Strictly speaking, this is in
  # bad form as a good Django project contains only the settings, url and view
  # definitions which are required to glue together each of the components of
  # the site, which are implemented in individual applications. However the
  # project does serve as a reasonable incubation center for components and
  # ideas that are currently in flux and have not reached a level of maturity
  # where they can be broken off into a separate application with a stable
  # API. For this reason, any application-like functionality provided at the
  # project level is to be treated as unstable and a work-in-progress.
  'packagename',

  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.markup',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  # Uncomment the next line to enable the admin:
  'django.contrib.admin',
  # Uncomment the next line to enable admin documentation:
  'django.contrib.admindocs',

  # Django-extensions provides a number of useful management scripts for
  # Django development, and some reusable code that solves common problems.
  'django_extensions',

  # Django-patterns is RokuSigma Inc.'s collection of idiomatic solutions to
  # common Django problems.
  'django_patterns',

  # South is the most excellent database migration/schema versioning tool
  # written by Andrew Godwin.
  'south',

  # django-context-extras is a simple Django app that provides some extra
  # context processors for your Django based projects, such as adding the
  # current site object or project settings to the context.
  'context_extras',

  # Django-form-utils is an application which provides utilities for enhancing
  # Django's form handling. It provides:
  #   1. BetterForm and BetterModelForm classes, which are subclasses of
  #      django.forms.Form and django.forms.ModelForm, respectively.
  #      BetterForm and BetterModelForm allow subdivision of forms into
  #      fieldsets which are iterable from a template, and also allow
  #      definition of row_attrs which can be accessed from the template to
  #      apply attributes to the surrounding container (<li>, <tr>, or
  #      whatever) of a specific form field.
  #   2. A ClearableFileField to enhance FileField and ImageField with a
  #      checkbox for clearing the contents of the field.
  #   3. An ImageWidget which display a thumbnail of the image rather than
  #      just the filename.
  #   4. An AutoResizeTextarea widget which auto-resizes to accomodate its
  #      contents.
  'form_utils',

  # Django-registration is a fairly simple user-registration application for
  # Django written by James Bennett, designed to make allowing user signups as
  # painless as possible.
  'registration',
)

#=-------------------=#
# django.contrib.auth #
#=-------------------=#

PASSWORD_HASHERS = (
  'django.contrib.auth.hashers.PBKDF2PasswordHasher',
  'django.contrib.auth.hashers.BCryptPasswordHasher',
)

# Used by django.contrib.auth utility decorators, the LOGIN_URL / LOGOUT_URL
# settings must be kept up-to-date with the site's urlpatterns.
LOGIN_URL  = "/login/"
LOGOUT_URL = "/logout/"

# Used by django.contrib.auth, this setting specifies the redirect URL after a
# successful login for which there is no ‘next’ GET field.
LOGIN_REDIRECT_URL = "/"

#=--------------------=#
# django.contrib.sites #
#=--------------------=#

SITE_ID = 1

#=--------------------------=#
# django.contrib.staticfiles #
#=--------------------------=#

# Absolute filesystem path to the directory that will hold user-uploaded
# files. Example:
#
# MEDIA_ROOT = "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.abspath(
  os.path.join(PROJECT_DIRECTORY, '..', 'db', 'sqlite.media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash. Examples:
#
# MEDIA_URL = "http://media.lawrence.com/media/"
# MEDIA_URL = "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to. Don't
# put anything in this directory yourself; store your static files in apps'
# "static/" subdirectories and in STATICFILES_DIRS. Example:
#
# STATIC_ROOT = "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.abspath(
  os.path.join(PROJECT_DIRECTORY, '..', 'pkg',
               'var', 'www', 'www.appname.com', 'public', 'static'))

# URL prefix for static files. Example:
#
# STATIC_URL = "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files.
STATICFILES_DIRS = (
  # Put strings here, like "/home/html/static" or "C:/www/django/static".
  # Always use forward slashes, even on Windows.
  # Don't forget to use absolute paths, not relative paths.
  os.path.abspath(os.path.join(PROJECT_DIRECTORY, '..', 'static')),
)

# List of finder classes that know how to find static files in various
# locations.
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#  'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

#=------------=#
# registration #
#=------------=#

# This setting is used by Django-registration to determine if the site is
# accepting new users or not. It is actually not required as the setting
# defaults to True, but exists here as a reminder of its existence.
REGISTRATION_OPEN = True

# This setting is used by Django-registration to determine how long email
# activation requests may remain outstanding. Note that if this time limit is
# exceeded, the account is marked as inactive and may be cleaned up by
# automated maintenance scripts provided by Django-registration.
ACCOUNT_ACTIVATION_DAYS = 15

#=-----------=#
# packagename #
#=-----------=#

SITE_WIDE_SEARCH = False

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
