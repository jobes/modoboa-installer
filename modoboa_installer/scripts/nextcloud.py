"""Modoboa related tasks."""

import json
import os
import pwd
import grp
import shutil
import stat
import sys
import subprocess

from .. import compatibility_matrix
from .. import package
from .. import python
from .. import utils
from .. import python

from . import base


class Nextcloud(base.Installer):
    """Modoboa installation."""

    appname = "nextcloud"
    packages = {
        "deb": [
            "php-fpm", "php-curl", "php-cli", "php-mysql", "php-gd",
            "php-iconv", "php-xsl", "php-json", "php-intl", "php-pear",
            "php-imagick", "php-dev", "php-common", "php-mbstring",
            "php-zip", "php-soap", "php-pgsql", "php-imap"],
        "rpm": [
            "php", "php-mysql", "php-pecl-zip", "php-xml", "php-mbstring",
            "php-gd", "php-fpm", "php-intl", "php-pgsql", "php-imap"]
    }
    config_files = [
        "nextcloud.conf=/etc/nginx/sites-available/nextcloud.conf",
        "config.php=/var/www/nextcloud/config/config.php"
    ]
    with_db = True
    with_user = False
    daemon_name = "nginx"

    def __init__(self, config):
        """Get configuration."""
        super(Nextcloud, self).__init__(config)
        python.install_packages(["future"])
        from future.standard_library import install_aliases
        install_aliases()
        from urllib.request import urlretrieve
        import zipfile
        urlretrieve(self.config.get("nextcloud", "nextcloudzip"), '/tmp/latest.zip')
        zip_ref = zipfile.ZipFile('/tmp/latest.zip', 'r')
        zip_ref.extractall(self.config.get("nextcloud", "installpath"))
        zip_ref.close()
        os.remove('/tmp/latest.zip')

        

    def post_run(self):
        uid = pwd.getpwnam("www-data").pw_uid
        gid = grp.getgrnam("www-data").gr_gid

        utils.exec_cmd("chown -R www-data:www-data "+self.config.get("nextcloud", "installpath")+"/nextcloud/")
        utils.exec_cmd('php '+self.config.get("nextcloud", "installpath")+'/nextcloud/occ  maintenance:install --database '+\
            self.config.get("database", "engine")+' --database-name '+self.config.get("nextcloud", "dbname")+' --database-user '+\
            self.config.get("nextcloud", "dbuser")+' --database-pass "'+self.config.get("nextcloud", "dbpassword")+\
            '--admin-user "admin" --admin-pass "password"', "www-data", login=False)

        utils.exec_cmd('php '+self.config.get("nextcloud", "installpath")+'/nextcloud/occ app:install user_external', "www-data", login=False
        utils.exec_cmd('php '+self.config.get("nextcloud", "installpath")+'/nextcloud/occ app:enable user_external', "www-data", login=False)
        utils.exec_cmd('php '+self.config.get("nextcloud", "installpath")+'/nextcloud/occ user:disable admin', "www-data", login=False)
        
        link = "/etc/nginx/sites-enabled/nextcloud.conf"
        dst = "/etc/nginx/sites-available/nextcloud.conf"
        if os.path.exists(link):
            return
        os.symlink(dst, link)
        #generovat mail s heslom pre nextcloud@cezmatrix.sk

