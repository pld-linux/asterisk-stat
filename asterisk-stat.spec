# TODO
# - remove jgraph from source
# - license

%define		srcversion	2_0_1
Summary:	Asterisk-Stat: CDR Analyser
Summary(pl):	Asterisk-Stat: Analizator CDR
Name:		asterisk-stat
Version:	2.0.1
Release:	0.2
License:	? (contains Freeware, LGPL, QPL parts)
Group:		Applications/WWW
Source0:	http://areski.net/asterisk-stat-v2/%{name}-v%{srcversion}.tar.gz
# Source0-md5:	aad3fe2f9826e8d63dfc9bdea2315d4a
Source1:	%{name}.conf
Source2:	%{name}-config.php
Patch0:		%{name}-config.patch
URL:		http://areski.net/asterisk-stat-v2/about.php
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.264
Requires:	%{name}(DB_Driver) = %{version}-%{release}
Requires:	adodb >= 4.67-1.17
Requires:	jpgraph
Requires:	php
Requires:	php-cli
Requires:	php-gd
Requires:	webapps
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_webappdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Asterisk-Stat is providing different reports & Graph to allow the
Asterisk-admin to analyse quickly and easily the traffic on their
Asterisk server. All the graphic & reports are based over the CDR
database.

%description -l pl
Asterisk-Stat udostêpnia ró¿ne raporty i wykresy pozwalaj±ce
administratorowi Asteriska szybko i ³atwo przeanalizowaæ ruch na
serwerze Asteriska. Wszystkie wykresy i raporty s± oparte na bazie
danych CDR.

%package db-mysql
Summary:	Asterisk-stat DB Driver for MySQL
Summary(pl):	Sterownik bazy danych MySQL dla Asterisk-stat
Group:		Applications/WWW
Requires:	php-mysql
Provides:	%{name}(DB_Driver) = %{version}-%{release}

%description db-mysql
This virtual package provides MySQL database backend for Asterisk-stat.

%description db-mysql -l pl
Ten wirtualny pakiet dostarcza backend bazy danych MySQL dla
Asterisk-stat.

%package db-pgsql
Summary:	Asterisk-stat DB Driver for PostgreSQL
Summary(pl):	Sterownik bazy danych PostgreSQL dla Asterisk-stat
Group:		Applications/WWW
Requires:	php-pgsql
Provides:	%{name}(DB_Driver) = %{version}-%{release}

%description db-pgsql
This virtual package provides PostgreSQL database backend for
Asterisk-stat.

%description db-pgsql -l pl
Ten wirtualny pakiet dostarcza backend bazy danych PostgreSQL dla
Asterisk-stat.

%prep
%setup -q -n %{name}-v2
%patch0 -p1

find '(' -name '*.php' -o -name '*.inc' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_webappdir},%{_sysconfdir}/%{name}}

cp -aRf * $RPM_BUILD_ROOT%{_appdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_webappdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_webappdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_webappdir}/config.php

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc CHANGELOG.txt
%dir %attr(750,root,http) %{_webappdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webappdir}/config.php
%config(noreplace) %verify(not md5 mtime size) %{_webappdir}/apache.conf
%config(noreplace) %verify(not md5 mtime size) %{_webappdir}/httpd.conf
%{_datadir}/%{name}

%files db-mysql
%defattr(644,root,root,755)

%files db-pgsql
%defattr(644,root,root,755)
