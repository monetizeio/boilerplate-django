#!/bin/bash

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

POSTGRES_VERSION=9.1

sudo cp -a /etc/postgresql/9.1/main/postgresql.conf .
sudo cp -a /etc/postgresql/9.1/main/pg_hba.conf .
sudo -u postgres pg_dropcluster --stop 9.1 main
sudo -u postgres pg_createcluster -E 'UTF-8' --lc-collate='en_US.UTF-8' --lc-ctype='en_US.UTF-8' --locale='en_US.UTF-8' 9.1 main
sudo cp -a ./postgresql.conf /etc/postgresql/9.1/main
sudo cp -a ./pg_hba.conf /etc/postgresql/9.1/main
sudo /etc/init.d/postgresql restart
sudo -u postgres psql postgres -c "CREATE EXTENSION IF NOT EXISTS pgmp;"
sudo -u postgres psql template1 -c "CREATE EXTENSION IF NOT EXISTS pgmp;"
sudo -u postgres psql -c "CREATE USER django WITH PASSWORD 'password';"
sudo -u postgres psql -c "ALTER ROLE django WITH CREATEDB"
sudo -u postgres psql -c "CREATE DATABASE django;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE django TO django;"

#
# End of File
#
