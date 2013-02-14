# -*- mode: ruby -*-
# vi: set ft=ruby :

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

PROJECT = File.join(File.dirname(__FILE__))

Vagrant::Config.run do |config|
    config.vm.box     = "Ubuntu 12.04 (x86_64)"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"

    config.vm.define "postgres" do |cfg|
        cfg.vm.forward_port 5432, 5432
        cfg.vm.provision :chef_solo do |chef|
            chef.cookbooks_path = [
                File.join(PROJECT, 'cookbooks'),
            ]
            chef.add_recipe("apt")
            chef.add_recipe("build-essential")
            chef.add_recipe("postgresql::apt_postgresql_ppa")
            chef.add_recipe("postgresql::server")
            chef.add_recipe("postgresql-pgmp")
            chef.json = {
                :postgresql => {
                    :version => "9.1",
                    :listen_addresses => "*",
                    :hba => [
                        { :method => "trust", :address => "0.0.0.0/0" },
                        { :method => "trust", :address => "::1/0" },
                    ],
                    :password => {
                        :postgres => "password"
                    }
                }
            }
        end
        cfg.vm.provision :shell, :path => 'etc/postgres/init.sh'
    end
end

#
# End of File
#
