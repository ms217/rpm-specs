%define debug_package %{nil}

# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries


Name:		prometheus
Version:	1.4.1
Release:	7.1%{?dist}
Group:          Applications/System
Summary:	Prometheus monitoring system and time series database
License:	ASL 2.0
URL:		https://github.com/prometheus/prometheus

Source0:  https://github.com/prometheus/prometheus/releases/download/v%{version}/prometheus-%{version}.linux-amd64.tar.gz
Source1:  prometheus.service
Source2:  prometheus.default
Source3:  prometheus.initd
Source4:  prometheus.yml

%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Prometheus exporter for machine metrics, written in Go with pluggable metric collectors.

%prep
%setup -q -n prometheus-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/usr/bin
%if %{with_systemd}
mkdir -vp %{buildroot}/usr/lib/systemd/system
%endif
mkdir -vp %{buildroot}/etc/sysconfig
mkdir -vp %{buildroot}/etc/prometheus
install -m 755 prometheus %{buildroot}/usr/bin/prometheus
%if %{with_systemd}
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/prometheus.service
%else
install -D -m 755 %{SOURCE3} %{buildroot}/%{_initrddir}/prometheus
%endif
install -m 644 %{SOURCE2} %{buildroot}/etc/sysconfig/prometheus
install -m 644 %{SOURCE4} %{buildroot}/etc/prometheus/prometheus.yml



%pre
getent group prometheus >/dev/null || groupadd -r prometheus >/dev/null 2>&1 || :
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus >/dev/null 2>&1 || :
exit 0

%post
%if %{with_systemd}
%systemd_post prometheus.service
%else
/sbin/chkconfig --del prometheus
%endif

%preun
%if %{with_systemd}
%systemd_preun prometheus.service
%else
if [ "$1" = "0" ] ; then
 /sbin/service prometheus stop >/dev/null 2>&1
 /sbin/chkconfig --del prometheus
fi
%endif



%postun
%if %{with_systemd}
%systemd_postun prometheus.service
%else
/sbin/chkconfig --del prometheus
%endif
/usr/sbin/userdel prometheus >/dev/null 2>&1 || :
/usr/sbin/groupdel prometheus >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
/usr/bin/prometheus
%if %{with_systemd}
/usr/lib/systemd/system/prometheus.service
%else
%{_initrddir}/prometheus
%endif
%config(noreplace) /etc/sysconfig/prometheus
%config(noreplace) /etc/prometheus/prometheus.yml


%changelog
* Mon Nov 28 2016 Michael Seevogel <michael@michaelseevogel.de> - 1:1.4.1-1
- Initial prometheus package

