# === Makefile ------------------------------------------------------------===
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

ROOT=$(shell pwd)
CACHE_ROOT=${ROOT}/.cache
PKG_ROOT=${ROOT}/.pkg
PACKAGE_NAME=packagename
APP_URL=appname.com
SQLITE=$(shell which sqlite3)

-include Makefile.local

.PHONY: all
all: ${PKG_ROOT}/.stamp-h

.PHONY: check
check: all
	mkdir -p build/report
	"${PKG_ROOT}"/bin/python -Wall "${ROOT}"/manage.py test \
	  --settings=${PACKAGE_NAME}.settings.testing \
	  --exclude-dir="${ROOT}"/${PACKAGE_NAME}/settings \
	  --with-xunit \
	  --xunit-file="${ROOT}"/build/report/xunit.xml \
	  --with-xcoverage \
	  --xcoverage-file="${ROOT}"/build/report/coverage.xml \
	  --cover-package=${PACKAGE_NAME} \
	  --cover-erase \
	  --cover-tests \
	  --cover-inclusive \
	  ${PACKAGE_NAME}

.PHONY: shell
shell: all db
	"${PKG_ROOT}"/bin/python "${ROOT}"/manage.py shell_plusplus \
	  --settings=${PACKAGE_NAME}.settings.development \
	  --print-sql \
	  --ipython

.PHONY: run
run: all db
	"${PKG_ROOT}"/bin/python "${ROOT}"/manage.py runserver_plus \
	  --settings=${PACKAGE_NAME}.settings.development

.PHONY: db
db: all
	"${PKG_ROOT}"/bin/python "${ROOT}"/manage.py syncdb
	"${PKG_ROOT}"/bin/python "${ROOT}"/manage.py migrate
	mkdir -p "${ROOT}"/db/sqlite.media

.PHONY: dbshell
dbshell: all db
	${SQLITE} "${ROOT}"/db/sqlite.db

.PHONY: dbclean
dbclean:
	rm -rf "${ROOT}"/db/sqlite.media
	rm -f "${ROOT}"/db/sqlite.db

.PHONY: mostlyclean
mostlyclean:
	-rm -rf dist
	-rm -rf build
	-rm -rf .coverage

.PHONY: clean
clean: mostlyclean
	-rm -rf "${PKG_ROOT}"

.PHONY: distclean
distclean: clean
	-rm -rf "${CACHE_ROOT}"
	-rm -rf Makefile.local

.PHONY: maintainer-clean
maintainer-clean: distclean
	@echo 'This command is intended for maintainers to use; it'
	@echo 'deletes files that may need special tools to rebuild.'

.PHONY: dist
dist:
	"${PKG_ROOT}"/bin/python setup.py sdist

# ===----------------------------------------------------------------------===

${CACHE_ROOT}/virtualenv/virtualenv-1.7.1.2.tar.gz:
	mkdir -p ${CACHE_ROOT}/virtualenv
	sh -c "cd ${CACHE_ROOT}/virtualenv && curl -O http://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.7.1.2.tar.gz"

${PKG_ROOT}/.stamp-h: ${ROOT}/conf/requirements.* ${CACHE_ROOT}/virtualenv/virtualenv-1.7.1.2.tar.gz
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
	  -xf "${CACHE_ROOT}"/virtualenv/virtualenv-1.7.1.2.tar.gz
	python "${CACHE_ROOT}"/virtualenv/virtualenv-1.7.1.2/virtualenv.py \
	  --clear \
	  --no-site-packages \
	  --distribute \
	  --never-download \
	  --prompt="(${APP_URL}) " \
	  "${PKG_ROOT}"
	rm -rf "${CACHE_ROOT}"/virtualenv/virtualenv-1.7.1.2
	
	# pip has broken the Python Imaging Library install (perhaps because
	# the tarball does not follow standard naming practice). So we
	# manually install it here, specifying the download URL directly:
	"${PKG_ROOT}"/bin/easy_install \
	  http://effbot.org/downloads/Imaging-1.1.7.tar.gz
	
	# readline is installed here to get around a bug on Mac OS X which is
	# causing readline to not build properly if installed from pip.
	"${PKG_ROOT}"/bin/easy_install readline
	
	# pip is used to install Python dependencies for this project.
	for reqfile in "${ROOT}"/conf/requirements*.pip; do \
	  "${PKG_ROOT}"/bin/python "${PKG_ROOT}"/bin/pip install \
	    --download-cache="${CACHE_ROOT}"/pypi \
	    -r "$$reqfile"; \
	done
	
	# The static directory is where Django accumulates staticfiles. It
	# needs to be present (even if empty), or else errors will be thrown
	# by the `run` target.
	mkdir -p "${PKG_ROOT}"/var/www/${APP_URL}/public/static
	
	# All done!
	touch "${PKG_ROOT}"/.stamp-h

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
