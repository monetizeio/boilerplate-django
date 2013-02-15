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

ROOT=$(shell pwd)
CACHE_ROOT=${ROOT}/.cache
PKG_ROOT=${ROOT}/.pkg
APP_NAME=boilerplate-django-startproject
PACKAGE=project_name

-include Makefile.local

.PHONY: all
all: ${PKG_ROOT}/.stamp-h ${ROOT}/${PACKAGE}/settings/secret_keys.py vmup

.PHONY: check
check: all
	mkdir -p "${ROOT}"/build/report
	"${PKG_ROOT}"/bin/python -Wall "${ROOT}"/manage.py test \
	    --settings=${PACKAGE}.settings.testing \
	    --with-xunit \
	    --xunit-file="${ROOT}"/build/report/xunit.xml \
	    --with-xcoverage \
	    --xcoverage-file="${ROOT}"/build/report/coverage.xml \
	    --cover-package=${PACKAGE} \
	    --cover-package=apps \
	    --cover-package=xunit \
	    --cover-erase \
	    --cover-tests \
	    --cover-inclusive \
	    --all-modules \
	    ${PACKAGE} apps xunit

.PHONY: shell
shell: all db
	"${PKG_ROOT}"/bin/python "${ROOT}"/manage.py shell_plusplus \
	  --settings=${PACKAGE}.settings.development \
	  --print-sql \
	  --ipython

.PHONY: run
run: all db
	sh -c "source '${PKG_ROOT}'/bin/activate && \
	    RBENV_ROOT='${PKG_ROOT}' '${PKG_ROOT}'/bin/rbenv exec bundle exec \
	        foreman start --procfile Procfile.development --port=8000"

.PHONY: mostlyclean
mostlyclean:
	- rm -rf dist
	- rm -rf build
	- rm -rf .coverage

.PHONY: clean
clean: mostlyclean vmdestroy
	-rm -f .rbenv-version
	-rm -rf "${PKG_ROOT}"

.PHONY: distclean
distclean: clean
	-rm -rf cookbooks tmp
	-rm -rf "${CACHE_ROOT}"
	-rm -rf Makefile.local

.PHONY: maintainer-clean
maintainer-clean: distclean
	@echo 'This command is intended for maintainers to use; it'
	@echo 'deletes files that may need special tools to rebuild.'

# ===----------------------------------------------------------------------===

${ROOT}/${PACKAGE}/settings/secret_keys.py:
	@echo  >"${ROOT}/${PACKAGE}"/settings/secret_keys.py '#!/usr/bin/env python'
	@echo >>"${ROOT}/${PACKAGE}"/settings/secret_keys.py '# -*- coding: utf-8 -*-'
	@echo >>"${ROOT}/${PACKAGE}"/settings/secret_keys.py \
	    "SECRET_KEY='`LC_CTYPE=C < /dev/urandom tr -dc A-Za-z0-9_ | head -c24`'"

# ===--------------------------------------------------------------------===

.PHONY: db
db: all
	"${PKG_ROOT}"/bin/python "${ROOT}"/manage.py syncdb \
	  --settings=${PACKAGE}.settings.development

.PHONY: dbshell
dbshell: db
	"${PKG_ROOT}"/bin/python "${ROOT}"/manage.py dbshell \
	  --settings=${PACKAGE}.settings.development

.PHONY: dbssh
dbssh: db
	- RBENV_ROOT="${PKG_ROOT}" "${PKG_ROOT}"/bin/rbenv exec bundle exec \
	    vagrant ssh postgres

# ===--------------------------------------------------------------------===

.PHONY: vmup
vmup: ${PKG_ROOT}/.stamp-h
	RBENV_ROOT="${PKG_ROOT}" "${PKG_ROOT}"/bin/rbenv exec bundle exec \
	    vagrant up
	PGPASSWORD=password psql -h localhost -U django -c "SELECT TRUE;" || \
	RBENV_ROOT="${PKG_ROOT}" "${PKG_ROOT}"/bin/rbenv exec bundle exec \
	    vagrant reload

.PHONY: vmsuspend
vmsuspend: ${PKG_ROOT}/.stamp-h
	- RBENV_ROOT="${PKG_ROOT}" "${PKG_ROOT}"/bin/rbenv exec bundle exec \
	    vagrant suspend

.PHONY: vmresume
vmresume: ${PKG_ROOT}/.stamp-h
	- RBENV_ROOT="${PKG_ROOT}" "${PKG_ROOT}"/bin/rbenv exec bundle exec \
	    vagrant resume

.PHONY: vmreload
vmreload: ${PKG_ROOT}/.stamp-h
	- RBENV_ROOT="${PKG_ROOT}" "${PKG_ROOT}"/bin/rbenv exec bundle exec \
	    vagrant reload

.PHONY: vmdestroy
vmdestroy:
	- RBENV_ROOT="${PKG_ROOT}" "${PKG_ROOT}"/bin/rbenv exec bundle exec \
	    vagrant destroy --force

# ===--------------------------------------------------------------------===

${CACHE_ROOT}/virtualenv/virtualenv-1.8.4.tar.gz:
	mkdir -p "${CACHE_ROOT}"/virtualenv
	sh -c "cd '${CACHE_ROOT}'/virtualenv && curl -O 'http://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.8.4.tar.gz'"

${CACHE_ROOT}/gmpy2/gmpy2-2.0.0b3.zip:
	mkdir -p "${CACHE_ROOT}"/gmpy2
	sh -c "cd "${CACHE_ROOT}"/gmpy2 && curl -O 'http://gmpy.googlecode.com/files/gmpy2-2.0.0b3.zip'"

${CACHE_ROOT}/rbenv/rbenv-0.4.0.tar.gz:
	mkdir -p ${CACHE_ROOT}/rbenv
	curl -L 'https://nodeload.github.com/sstephenson/rbenv/tar.gz/v0.4.0' >'$@'

${CACHE_ROOT}/rbenv/ruby-build-20130129.tar.gz:
	mkdir -p ${CACHE_ROOT}/rbenv
	curl -L 'https://nodeload.github.com/sstephenson/ruby-build/tar.gz/v20130129' >'$@'

${PKG_ROOT}/.stamp-h: ${ROOT}/requirements*.pip ${CACHE_ROOT}/virtualenv/virtualenv-1.8.4.tar.gz ${CACHE_ROOT}/gmpy2/gmpy2-2.0.0b3.zip ${CACHE_ROOT}/rbenv/rbenv-0.4.0.tar.gz ${CACHE_ROOT}/rbenv/ruby-build-20130129.tar.gz
	# Because build and run-time dependencies are not thoroughly tracked,
	# it is entirely possible that rebuilding the development environment
	# on top of an existing one could result in a broken build. For the
	# sake of consistency and preventing unnecessary, difficult-to-debug
	# problems, the entire development environment is rebuilt from scratch
	# everytime this make target is selected.
	${MAKE} clean
	
	# The ``${PKG_ROOT}`` directory, if it exists, is removed by the
	# ``clean`` target. The PyPI cache is nonexistant if this is a freshly
	# checked-out repository, or if the ``distclean`` target has been run.
	# This might cause problems with build scripts executed later which
	# assume their existence, so they are created now if they don't
	# already exist.
	mkdir -p "${PKG_ROOT}"
	mkdir -p "${CACHE_ROOT}"/pypi
	
	# ``virtualenv`` is used to create a separate Python installation for
	# this project in ``${PKG_ROOT}``.
	tar \
	    -C "${CACHE_ROOT}"/virtualenv --gzip \
	    -xf "${CACHE_ROOT}"/virtualenv/virtualenv-1.8.4.tar.gz
	python "${CACHE_ROOT}"/virtualenv/virtualenv-1.8.4/virtualenv.py \
	    --clear \
	    --distribute \
	    --never-download \
	    --prompt="(${APP_NAME}) " \
	    "${PKG_ROOT}"
	rm -rf "${CACHE_ROOT}"/virtualenv/virtualenv-1.8.4
	
	# pip has broken the Python Imaging Library install (perhaps because
	# the tarball does not follow standard naming practice). So we
	# manually install it here, specifying the download URL directly:
	"${PKG_ROOT}"/bin/easy_install \
	    http://effbot.org/downloads/Imaging-1.1.7.tar.gz
	
	# readline is installed here to get around a bug on Mac OS X which is
	# causing readline to not build properly if installed from pip.
	"${PKG_ROOT}"/bin/easy_install readline
	
	# gmpy2 is installed here since the 2.x series is not yet included in the
	# python packaging index.
	CFLAGS=-I/opt/local/include LDFLAGS=-L/opt/local/lib \
	"${PKG_ROOT}"/bin/easy_install \
	    "${CACHE_ROOT}"/gmpy2/gmpy2-2.0.0b3.zip
	
	# pip is used to install Python dependencies for this project.
	for reqfile in "${ROOT}"/requirements*.pip; do \
	    CFLAGS=-I/opt/local/include LDFLAGS=-L/opt/local/lib \
	    "${PKG_ROOT}"/bin/python "${PKG_ROOT}"/bin/pip install \
	        --download-cache="${CACHE_ROOT}"/pypi \
	        -r "$$reqfile"; \
	done
	
	# rbenv (and its plugins, ruby-build and rbenv-gemset) is used to build,
	# install, and manage ruby environments:
	tar \
	    -C "${PKG_ROOT}" --strip-components 1 --gzip \
	    -xf "${CACHE_ROOT}"/rbenv/rbenv-0.4.0.tar.gz
	mkdir -p "${PKG_ROOT}"/plugins/ruby-build
	tar \
	    -C "${PKG_ROOT}"/plugins/ruby-build --strip-components 1 --gzip \
	    -xf "${CACHE_ROOT}"/rbenv/ruby-build-20130129.tar.gz
	
	# Trigger a build and install of our required ruby version:
	- CONFIGURE_OPTS=--with-openssl-dir=$(shell which openssl | sed -e s:/bin/openssl::) \
	  RBENV_ROOT="${PKG_ROOT}" "${PKG_ROOT}"/bin/rbenv install 1.9.3-p194
	- RBENV_ROOT="${PKG_ROOT}" "${PKG_ROOT}"/bin/rbenv rehash
	echo 1.9.3-p194 >.rbenv-version
	
	# Install bundler & gemset dependencies:
	RBENV_ROOT="${PKG_ROOT}" "${PKG_ROOT}"/bin/rbenv exec gem install bundler
	- RBENV_ROOT="${PKG_ROOT}" "${PKG_ROOT}"/bin/rbenv rehash
	RBENV_ROOT="${PKG_ROOT}" "${PKG_ROOT}"/bin/rbenv exec bundle install
	- RBENV_ROOT="${PKG_ROOT}" "${PKG_ROOT}"/bin/rbenv rehash
	
	# Fetch Chef cookbooks
	RBENV_ROOT="${PKG_ROOT}" "${PKG_ROOT}"/bin/rbenv exec bundle exec librarian-chef install
	
	# The static directory is where Django accumulates staticfiles. It
	# needs to be present (even if empty), or else errors will be thrown
	# by the `run` target.
	mkdir -p "${PKG_ROOT}"/var/www/${PACKAGE}/public/static
	
	# All done!
	touch "${PKG_ROOT}"/.stamp-h

#
# End of File
#
