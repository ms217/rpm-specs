%define debug_package %{nil}

Name:		node_exporter
Version:	0.12.0
Release:        1%{?dist}
Epoch:          2
Group:          Applications/System
Summary:	Prometheus exporter for machine metrics, written in Go with pluggable metric collectors.
License:	ASL 2.0
URL:		https://github.com/prometheus/node_exporter

Source0:  https://github.com/prometheus/node_exporter/releases/download/%{version}/node_exporter-%{version}.linux-amd64.tar.gz
Source1:  node_exporter.service
Source2:  node_exporter.default
Source3:  node_exporter.initd

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
%setup -q -n node_exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus/metrics
mkdir -vp %{buildroot}/usr/bin
%if %{with_systemd}
mkdir -vp %{buildroot}/usr/lib/systemd/system
%endif
mkdir -vp %{buildroot}/etc/sysconfig
install -m 755 node_exporter %{buildroot}/usr/bin/node_exporter
%if %{with_systemd}
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/node_exporter.service
%else
install -D -m 755 %{SOURCE3} %{buildroot}/%{_initrddir}/node_exporter
%endif
install -m 644 %{SOURCE2} %{buildroot}/etc/sysconfig/node_exporter



%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%if %{with_systemd}
%systemd_post node_exporter.service
%else
/sbin/chkconfig --del node_exporter
%endif

%preun
%if %{with_systemd}
%systemd_preun node_exporter.service
%else
if [ "$1" = "0" ] ; then
 /sbin/service node_exporter stop >/dev/null 2>&1
 /sbin/chkconfig --del node_exporter
fi
%endif



%postun
%if %{with_systemd}
%systemd_postun node_exporter.service
%else
/sbin/chkconfig --del node_exporter
%endif

%files
%defattr(-,root,root,-)
/usr/bin/node_exporter
%if %{with_systemd}
/usr/lib/systemd/system/node_exporter.service
%else
%{_initrddir}/node_exporter
%endif
%config(noreplace) /etc/sysconfig/node_exporter
%attr(755, prometheus, prometheus)/var/lib/prometheus/metrics

%changelog
* Fri Nov 04 2016 Michael Seevogel <michael@michaelseevogel.de> - 1:0.12.0-2
- Adjusted sources for the upcoming textfile collector package

* Wed Nov 02 2016 Michael Seevogel <michael@michaelseevogel.de> - 1:0.12.0-1
- Initial node_exporter package
- buildable on EL6 and EL7
