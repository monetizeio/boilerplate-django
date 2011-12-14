# === Makefile ------------------------------------------------------------===
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

ROOT=$(shell pwd)
CACHE_ROOT=${ROOT}/.cache
PKG_ROOT=${ROOT}/.pkg
RVM_ROOT=${HOME}/.rvm
RVM_RUBY_VERSION=ruby-1.9.2-p290
RVM_GEMSET_NAME=6horizons.com
APP_URL=6horizons.com
SQLITE=$(shell which sqlite3)

.PHONY: all
all: ${PKG_ROOT}/.stamp-h

.PHONY: db
db: all
	"${PKG_ROOT}"/bin/python sixhorizons/manage.py syncdb
	"${PKG_ROOT}"/bin/python sixhorizons/manage.py migrate
	mkdir -p db/sqlite.media

.PHONY: dbshell
dbshell: all db
	"${SQLITE}" db/sqlite.db

.PHONY: dbclean
dbclean: all
	rm -rf db/sqlite.media
	rm -f db/sqlite.db
	${MAKE} db

.PHONY: check
check: all
	mkdir -p build/report
	"${PKG_ROOT}"/bin/python -Wall sixhorizons/manage.py test \
	  --settings=settings.testing \
	  --exclude-dir=sixhorizons/settings \
	  --with-xunit \
	  --xunit-file="build/report/xunit.xml" \
	  --with-xcoverage \
	  --xcoverage-file="build/report/coverage.xml" \
	  --cover-package=sixhorizons \
	  --cover-erase \
	  --cover-tests \
	  --cover-inclusive \
	  sixhorizons

.PHONY: shell
shell: all db
	"${PKG_ROOT}"/bin/python sixhorizons/manage.py shell_plus \
	  --settings=settings.development \
	  --print-sql \
	  --ipython

.PHONY: run
run: all db
	"${PKG_ROOT}"/bin/python sixhorizons/manage.py runserver_plus \
	  --settings=settings.development

.PHONY: mostlyclean
mostlyclean:

.PHONY: clean
clean: mostlyclean
	-rm -rf "${PKG_ROOT}"
	-[ ! -e "${RVM_ROOT}"/scripts/rvm ] || \
	  bash -c "source '${RVM_ROOT}'/scripts/rvm; \
	    rvm ${RVM_RUBY_VERSION} --force gemset delete ${RVM_GEMSET_NAME} \
	  "

.PHONY: distclean
distclean: clean
	-rm -rf ${CACHE_ROOT}

.PHONY: maintainer-clean
maintainer-clean: distclean
	@echo 'This command is intended for maintainers to use; it'
	@echo 'deletes files that may need special tools to rebuild.'

.PHONY: dist
dist:

# ===----------------------------------------------------------------------===
# ===----------------------------------------------------------------------===

${CACHE_ROOT}/virtualenv/virtualenv-1.6.4.tar.gz:
	mkdir -p ${CACHE_ROOT}/virtualenv
	sh -c "cd ${CACHE_ROOT}/virtualenv && curl -O http://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.6.4.tar.gz"

${PKG_ROOT}/.stamp-h: conf/requirements.* ${CACHE_ROOT}/virtualenv/virtualenv-1.6.4.tar.gz
	# Because build and run-time dependencies are not thoroughly tracked,
	# it is entirely possible that rebuilding the development environment
	# on top of an existing one could result in a broken build. For the
	# sake of consistency and preventing unnecessary, difficult-to-debug
	# problems, the entire development environment is rebuilt from scratch
	# everytime this make target is selected.
	${MAKE} clean
	
	# The PKG_ROOT directory, if it exists, is removed by the `clean`
	# target. The PyPI cache is nonexistant if this is a freshly checked-
	# out repository, or if the `distclean` target has been run. Either
	# case might cause problems with build scripts executed later which
	# assume their existence, so they are created now if necessary.
	mkdir -p "${PKG_ROOT}"
	mkdir -p ${CACHE_ROOT}/pypi
	
	# virtualenv is used to create a separate Python installation for this
	# project in PKG_ROOT.
	tar \
	  -C ${CACHE_ROOT}/virtualenv --gzip \
	  -xf ${CACHE_ROOT}/virtualenv/virtualenv-1.6.4.tar.gz
	python ${CACHE_ROOT}/virtualenv/virtualenv-1.6.4/virtualenv.py \
	  --clear \
	  --no-site-packages \
	  --distribute \
	  --never-download \
	  --prompt="(${APP_URL}) " \
	  "${PKG_ROOT}"
	rm -rf ${CACHE_ROOT}/virtualenv/virtualenv-1.6.4
	
	# readline is installed here to get around a bug on Mac OS X which is
	# causing readline to not build properly if installed from pip.
	${PKG_ROOT}/bin/easy_install readline
	
	# pip is used to install Python dependencies for this project.
	for reqfile in conf/requirements*.pip; do \
	  ${PKG_ROOT}/bin/python ${PKG_ROOT}/bin/pip install \
	    --download-cache="${ROOT}"/${CACHE_ROOT}/pypi \
	    -r "$$reqfile"; \
	done
	
	# The RVM installation script handles all the details of installing
	# RVM, if it is not already installed.. It normally places RVM in the
	# user's HOME directory, and we will work off of that assumption.
	[ -e ${RVM_ROOT}/scripts/rvm ] || \
	  curl -s https://rvm.beginrescueend.com/install/rvm | bash
	
	# Make sure our required Ruby version is built and installed, if it is
	# not already.
	bash -c "source '${RVM_ROOT}'/scripts/rvm; \
	  if test "x" = "x`bash -c "source '${RVM_ROOT}'/scripts/rvm; rvm list | grep -e '${RVM_RUBY_VERSION}' | cut -d' ' -f 4"`"; then \
	    rvm install ${RVM_RUBY_VERSION}; \
	  fi \
	"
	
	# A gemset environment is created for this project.
	bash -c "source '${RVM_ROOT}'/scripts/rvm; \
	  rvm use ${RVM_RUBY_VERSION}@${RVM_GEMSET_NAME} --create \
	"
	
	# Local links are created in PKG_ROOT for the ruby interpreter,
	# rubygems package manager, and various other related tools. This is a
	# convenience so that if the virtualenv activate script is run, the
	# ruby environment will be activated as well, automatically.
	for i in `ls "${RVM_ROOT}"/bin/*${RVM_RUBY_VERSION}@${RVM_GEMSET_NAME}`; do \
	  echo '#!/bin/sh' \
	    >"${PKG_ROOT}"/bin/`basename $$i | cut -d'-' -f1`; \
	  echo '"${RVM_ROOT}"/bin/"'`basename $$i`'" $$@' \
	    >>"${PKG_ROOT}"/bin/`basename $$i | cut -d'-' -f1`; \
	  chmod +x "${PKG_ROOT}"/bin/`basename $$i | cut -d'-' -f1`; \
	done
	
	# gem_snapshot is a rubygem which provides a capability for ruby
	# similar to `pip install -r` (it will install specific versions of
	# gems specified in a configuration file).
	"${PKG_ROOT}"/bin/gem install gem_snapshot
	for reqfile in conf/requirements*.gem; do \
	  "${PKG_ROOT}"/bin/gem snapshot restore < "$$reqfile"; \
	done
	
	# Some gems install programs of their own to the gemset's bin
	# directory. We find and install symbolic links to these programs into
	# PKG_ROOT, so that they are accessible from the virtualenv
	# environment.
	for i in `ls "${RVM_ROOT}"/gems/${RVM_RUBY_VERSION}@${RVM_GEMSET_NAME}/bin`; do \
	  echo '#!/bin/sh' \
	    >"${PKG_ROOT}"/bin/`basename $$i | cut -d'-' -f1`; \
	  echo source '"${RVM_ROOT}"/scripts/rvm' \
	    >>"${PKG_ROOT}"/bin/`basename $$i | cut -d'-' -f1`; \
	  echo '"`dirname $$0`"/ruby "${RVM_ROOT}"/gems/${RVM_RUBY_VERSION}@${RVM_GEMSET_NAME}/bin/"'`basename $$i`'" $$@' \
	    >>"${PKG_ROOT}"/bin/`basename $$i | cut -d'-' -f1`; \
	  chmod +x "${PKG_ROOT}"/bin/`basename $$i | cut -d'-' -f1`; \
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
