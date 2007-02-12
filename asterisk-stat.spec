# TODO
# - license
%define		srcversion	2_0_1
Summary:	Asterisk-Stat: CDR Analyser
Summary(pl.UTF-8):	Asterisk-Stat: Analizator CDR
Name:		asterisk-stat
Version:	2.0.1
Release:	0.4
License:	? (contains Freeware, LGPL, QPL parts)
Group:		Applications/WWW
Source0:	http://areski.net/asterisk-stat-v2/%{name}-v%{srcversion}.tar.gz
# Source0-md5:	aad3fe2f9826e8d63dfc9bdea2315d4a
Source1:	%{name}.conf
Source2:	%{name}-config.php
Patch0:		%{name}-config.patch
Patch1:		%{name}-jpgraph.patch
URL:		http://areski.net/asterisk-stat-v2/about.php
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.264
Requires:	%{name}(DB_Driver) = %{version}-%{release}
Requires:	adodb >= 4.67-1.17
Requires:	jpgraph
Requires:	php(gd)
Requires:	php-cli
Requires:	webapps
Requires:	webserver
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Asterisk-Stat is providing different reports & Graph to allow the
Asterisk-admin to analyse quickly and easily the traffic on their
Asterisk server. All the graphic & reports are based over the CDR
database.

%description -l pl.UTF-8
Asterisk-Stat udostępnia różne raporty i wykresy pozwalające
administratorowi Asteriska szybko i łatwo przeanalizować ruch na
serwerze Asteriska. Wszystkie wykresy i raporty są oparte na bazie
danych CDR.

%package db-mysql
Summary:	Asterisk-stat DB Driver for MySQL
Summary(pl.UTF-8):	Sterownik bazy danych MySQL dla Asterisk-stat
Group:		Applications/WWW
Requires:	php(mysql)
Provides:	%{name}(DB_Driver) = %{version}-%{release}

%description db-mysql
This virtual package provides MySQL database backend for
Asterisk-stat.

%description db-mysql -l pl.UTF-8
Ten wirtualny pakiet dostarcza backend bazy danych MySQL dla
Asterisk-stat.

%package db-pgsql
Summary:	Asterisk-stat DB Driver for PostgreSQL
Summary(pl.UTF-8):	Sterownik bazy danych PostgreSQL dla Asterisk-stat
Group:		Applications/WWW
Requires:	php(pgsql)
Provides:	%{name}(DB_Driver) = %{version}-%{release}

%description db-pgsql
This virtual package provides PostgreSQL database backend for
Asterisk-stat.

%description db-pgsql -l pl.UTF-8
Ten wirtualny pakiet dostarcza backend bazy danych PostgreSQL dla
Asterisk-stat.

%prep
%setup -q -n %{name}-v2
%patch0 -p1
%patch1 -p1

rm -drf jpgraph_lib
find '(' -name '*.php' -o -name '*.inc' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}
cp -aRf * $RPM_BUILD_ROOT%{_appdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/config.php

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc CHANGELOG.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%{_appdir}

%files db-mysql
%defattr(644,root,root,755)

%files db-pgsql
%defattr(644,root,root,755)
