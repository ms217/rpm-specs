%define debug_package %{nil}

Name:		node_exporter_textcollectors
Version:	0.0.1
Release:	1%{?dist}
Group:		Applications/System
Summary:	A Collection of Scripts that expose metrics to the node_exporter textfile collector plugin.
License:	GPLv3+
URL:		https://github.com/donmichelangelo/node_exporter_textcollectors

Source0:  https://github.com/donmichelangelo/node_exporter_textcollectors/releases/download/%{version}/node_exporter_textcollectors-%{version}.tar.gz

BuildArchitectures: noarch

Requires: smartmontools
Requires: bind-utils
Requires: node_exporter

%description
A Collection of Scripts that expose metrics to the node_exporter textfile collector plugin.

%prep
%setup -q -n node_exporter_textcollectors-%{version}

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/node_exporter/textfile_collector
mkdir -vp %{buildroot}/usr/lib64/node_exporter/collectors
install -m 755 collectors/env.sh %{buildroot}/usr/lib64/node_exporter/collectors/env.sh
install -m 755 collectors/node_exporter_dovecot %{buildroot}/usr/lib64/node_exporter/collectors/node_exporter_dovecot
install -m 755 collectors/node_exporter_smart %{buildroot}/usr/lib64/node_exporter/collectors/node_exporter_smart
install -m 755 collectors/node_exporter_senderscore %{buildroot}/usr/lib64/node_exporter/collectors/node_exporter_senderscore






#%pre

#%post

#%preun

#%postun

%files
%defattr(-,root,root,-)
/usr/lib64/node_exporter/collectors/env.sh
/usr/lib64/node_exporter/collectors/node_exporter_dovecot
/usr/lib64/node_exporter/collectors/node_exporter_smart
/usr/lib64/node_exporter/collectors/node_exporter_senderscore
%attr(755, prometheus, prometheus)/var/lib/node_exporter/textfile_collector

