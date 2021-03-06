<?php
$CONFIG = array (
	'datadirectory' => '%installpath/nextcloud/data',
	'default_language' => 'en',
	'defaultapp' => 'files',
	'knowledgebaseenabled' => true,
	'enable_avatars' => true,
	'allow_user_to_change_display_name' => false,
	'remember_login_cookie_lifetime' => 3600,
	'session_lifetime' => 3600,
	'session_keepalive' => true,
	'token_auth_enforced' => true,
	'auth.bruteforce.protection.enabled' => true,
	'skeletondirectory' => '%installpath/nextcloud/core/skeleton',
	'lost_password_link' => 'https://%hostname/accounts/password_reset/',
	'mail_domain' => 'cezmatrix.sk',
	'mail_from_address' => '%domain',
	'mail_smtpdebug' => false,
	'mail_smtpmode' => 'sendmail',
	'mail_smtphost' => '127.0.0.1',
	'mail_smtpport' => 25,
	'mail_smtptimeout' => 10,
	'mail_smtpsecure' => '',
	'mail_smtpauthtype' => 'LOGIN',
	'mail_smtpname' => 'nextcloud@%domain',
	'mail_smtppassword' => 'TODO',
	'overwriteprotocol' => 'https',
	'overwritehost' => 'cloud.%domain',
	'overwritewebroot' => '/',
	'htaccess.RewriteBase' => '/',
	'log_rotate_size' => 10485760,
	'user_backends' => array(
		array(
			'class'=>'OC_User_IMAP',
			'arguments'=>array('{localhost:143/novalidate-cert}')
		)
  	),
); 
