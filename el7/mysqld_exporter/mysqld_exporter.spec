%define debug_package %{nil}

Name:		mysqld_exporter
Version:	0.9.0
Release:	24.1%{?dist}
Group:          Applications/System
Summary:	Prometheus exporter for MySQL compatible Server metrics, written in Go.
License:	ASL 2.0
URL:		https://github.com/prometheus/mysqld_exporter

Source0:  https://github.com/prometheus/mysqld_exporter/releases/download/%{version}/mysqld_exporter-%{version}.linux-amd64.tar.gz
Source1:  mysqld_exporter.service
Source2:  mysqld_exporter.default
Source3:  mysqld_exporter.initd
Source4:  my.cnf

%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Prometheus exporter for MySQL compatible Server metrics, written in Go.

%prep
%setup -q -n mysqld_exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
%if %{with_systemd}
mkdir -vp %{buildroot}/usr/lib/systemd/system
%endif
mkdir -vp %{buildroot}/etc/sysconfig
mkdir -vp %{buildroot}/etc/prometheus
install -m 755 mysqld_exporter %{buildroot}/usr/bin/mysqld_exporter
%if %{with_systemd}
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/mysqld_exporter.service
%else
install -D -m 755 %{SOURCE3} %{buildroot}/%{_initrddir}/mysqld_exporter
%endif
install -m 644 %{SOURCE2} %{buildroot}/etc/sysconfig/mysqld_exporter
install -m 644 %{SOURCE4} %{buildroot}/etc/prometheus/.my.cnf




%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%if %{with_systemd}
%systemd_post mysqld_exporter.service
%else
/sbin/chkconfig --del mysqld_exporter
%endif

%preun
%if %{with_systemd}
%systemd_preun mysqld_exporter.service
%else
if [ "$1" = "0" ] ; then
 /sbin/service mysqld_exporter stop >/dev/null 2>&1
 /sbin/chkconfig --del mysqld_exporter
fi
%endif



%postun
%if %{with_systemd}
%systemd_postun mysqld_exporter.service
%else
/sbin/chkconfig --del mysqld_exporter
%endif

%files
%defattr(-,root,root,-)
/usr/bin/mysqld_exporter
%if %{with_systemd}
/usr/lib/systemd/system/mysqld_exporter.service
%else
%{_initrddir}/mysqld_exporter
%endif
%config(noreplace) /etc/sysconfig/mysqld_exporter
%config(noreplace) /etc/prometheus/.my.cnf
%attr(755, prometheus, prometheus)/var/lib/prometheus


%changelog
* Wed Nov 09 2016 Michael Seevogel <michael@michaelseevogel.de> - 1:0.9.0-2
- Systemd fixes

* Wed Nov 09 2016 Michael Seevogel <michael@michaelseevogel.de> - 1:0.9.0-1
- First RPM Package Release of the mysqld_exporter
