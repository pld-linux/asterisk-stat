#
#TODO - webapps
#TODO - patch - include in /usr/share/asterisk-stat/lib/defines.php and add file in SOURCES
#TODO - remove jgroph from source
#TODO - Subpackage for databases?
#TODO - license

%define		srcversion	2_0_1

Summary:	Asterisk-Stat: CDR Analyser
Summary(pl):	Asterisk-Stat: Analizator CDR
Name:		asterisk-stat
Version:	2.0.1
Release:	0.1
License:	-
Group:		Applications/WWW
Source0:	http://areski.net/%{name}-v2/%{name}-v%{srcversion}.tar.gz
# Source0-md5:	aad3fe2f9826e8d63dfc9bdea2315d4a
#Source1:	%{name}.conf
#Source2:	%{name}-config.php
#Patch0:	%{name}-config.patch
URL:		http://areski.net/asterisk-stat-v2/about.php
BuildRequires:	rpm-perlprov
Requires:	php
Requires:	php-cli
Requires:	php-gd
Requires:	php-mysql
Requires:	webserver
Requires:	webapps
Requires:	jpgraph
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

%prep
%setup -q -n %{name}-v2
#%patch0 -p1

find '(' -name '*.php' -o -name '*.inc' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_webappdir},%{_sysconfdir}/%{name}}

cp -aRf * $RPM_BUILD_ROOT%{_appdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_webappdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_webappdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{sysconfdir}/%{name}/

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
#%%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}-config.php
%{_datadir}/%{name}
