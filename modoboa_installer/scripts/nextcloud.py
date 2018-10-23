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
    no_daemon = True
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
        subprocess.Popen(("wget https://download.nextcloud.com/server/releases/latest.zip -P /tmp").split())
        subprocess.Popen(("unzip /tmp/latest.zip  -d "+self.config.get("nextcloud", "installpath")).split())
        subprocess.Popen(("chown -R www-data:www-data "+self.config.get("nextcloud", "installpath")).split())

        uid = pwd.getpwnam("www-data").pw_uid
        gid = grp.getgrnam("www-data").gr_gid
        for root, dirs, files in os.walk(self.config.get("nextcloud", "installpath")+'/nextcloud'):
            for momo in dirs:  
                os.chown(os.path.join(root, momo), uid, gid)
            for momo in files:
                os.chown(os.path.join(root, momo), uid, gid)


        subprocess.Popen(('sudo -u www-data php '+self.config.get("nextcloud", "installpath")+'/nextcloud/occ  maintenance:install --database '+\
            self.config.get("database", "engine")+' --database-name '+self.config.get("nextcloud", "dbname")+' --database-user '+\
            self.config.get("nextcloud", "dbuser")+' --database-pass "'+self.config.get("nextcloud", "dbpassword")+\
            '--admin-user "admin" --admin-pass "password"').split(), stdout=subprocess.PIPE)

        subprocess.Popen(('sudo -u www-data php '+self.config.get("nextcloud", "installpath")+'/nextcloud/occ app:install user_external').split(), stdout=subprocess.PIPE)
        subprocess.Popen(('sudo -u www-data php '+self.config.get("nextcloud", "installpath")+'/nextcloud/occ app:enable user_external').split(), stdout=subprocess.PIPE)
        subprocess.Popen(('sudo -u www-data php '+self.config.get("nextcloud", "installpath")+'/nextcloud/occ user:disable admin').split(), stdout=subprocess.PIPE)
        
        link = "/etc/nginx/sites-enabled/nextcloud.conf"
        dst = "/etc/nginx/sites-available/nextcloud.conf"
        if os.path.exists(link):
            return
        os.symlink(dst, link)
        #generovat mail s heslom pre nextcloud@cezmatrix.sk

