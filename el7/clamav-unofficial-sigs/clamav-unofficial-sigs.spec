Name:           clamav-unofficial-sigs
Version:        5.1.1
Release:        1%{?dist}
Summary:        Scripts to download unoffical clamav signatures 
Group:          Applications/System
License:        BSD
URL:            https://github.com/extremeshok/clamav-unofficial-sigs
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       clamav clamav-update rsync gnupg diffutils curl bind-utils

%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)
%global with_systemd 1
%else
%global with_systemd 0
%endif


%if %{with_systemd}
#BuildRequires: systemd-devel
BuildRequires: systemd-units
Requires: systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-sysv
%else
Requires: crontabs
Requires(preun): initscripts
Requires(postun): initscripts
%endif



%description
This package contains scripts and configuration files
that provide the capability to download, test, and 
update the 3rd-party signature databases provide by 
Sanesecurity, SecuriteInfo, MalwarePatrol, OITC, 
INetMsg and ScamNailer.

%prep
%setup -q
tar xzvf %SOURCE0
#sed -i 's:/usr/local/bin/:/usr/bin/:' cron.d/clamav-unofficial-sigs
#sed -i 's:-c /usr/local/etc/clamav-unofficial-sigs.conf:\&>/dev/null:' cron.d/clamav-unofficial-sigs
#sed -i 's:/var/log/clamav-unofficial-sigs.log:/var/log/clamav-unofficial-sigs/clamav-unofficial-sigs.log:' logrotate.d/clamav-unofficial-sigs
sed -i 's:/usr/unofficial-dbs:%{_localstatedir}/lib/%{name}:' config/master.conf
#sed -i 's:/var/log:%{_localstatedir}/log/%{name}:' config/master.conf
sed -i 's:/path/to/ham-test/directory:%{_localstatedir}/lib/%{name}/ham-test:' config/master.conf
sed -i 's:"clamav":"clamupdate":' config/master.conf
sed -i 's:/var/run/clamd.pid:/var/run/clamd.scan/clamd.pid:' config/master.conf
sed -i 's:user_configuration_complete="no":user_configuration_complete="yes":' config/master.conf
sed -i 's:enable_logging="no":enable_logging="yes":' config/master.conf
#sed -i 's:root:clamupdate:g' logrotate.d/clamav-unofficial-sigs
sed -i 's:default_config="/etc/clamav-unofficial-sigs.conf":default_config="/etc/clamav-unofficial-sigs/clamav-unofficial-sigs.conf":' clamav-unofficial-sigs.sh
sed -i 's/\/usr\/local\/bin\/clamav-unofficial-sigs.sh/\/usr\/bin\/clamav-unofficial-sigs.sh/' systemd/clamav-unofficial-sigs.service


%build
#nothing to do here

%install
rm -rf $RPM_BUILD_ROOT
install -d -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
#install -d -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
#install -d -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -d -p $RPM_BUILD_ROOT%{_bindir}
install -d -p $RPM_BUILD_ROOT%{_mandir}/man8
install -d -p $RPM_BUILD_ROOT%{_localstatedir}/log/%{name}
install -d -p $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}
install -d -p $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/ham-test
install -d -p $RPM_BUILD_ROOT%{_unitdir}

#install unit files in case that we are on a Systemd distro
%if 0%{?fedora} || 0%{?rhel} >= 7
install -p -m0644 systemd/clamav-unofficial-sigs.service $RPM_BUILD_ROOT%{_unitdir}/clamav-unofficial-sigs.service
install -p -m0644 systemd/clamav-unofficial-sigs.timer $RPM_BUILD_ROOT%{_unitdir}/clamav-unofficial-sigs.timer
install -p -m0644 systemd/clamd.scan.service $RPM_BUILD_ROOT%{_unitdir}/clamd.scan.service
%endif





install -p -m0755 clamav-unofficial-sigs.sh $RPM_BUILD_ROOT%{_bindir}/clamav-unofficial-sigs.sh


#install -p -m0644 cron.d/clamav-unofficial-sigs $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/clamav-unofficial-sigs
#install -p -m0644 logrotate.d/clamav-unofficial-sigs $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/clamav-unofficial-sigs
install -p -m0644 clamav-unofficial-sigs.8 $RPM_BUILD_ROOT%{_mandir}/man8/clamav-unofficial-sigs.8
pushd $RPM_BUILD_ROOT%{_mandir}/man8/
ln -s clamav-unofficial-sigs.8 clamav-unofficial-sigs.sh.8
popd
install -p -m0644 config/master.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/master.conf
install -p -m0644 config/os.centos6.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/os.centos6.conf
install -p -m0644 config/os.centos7.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/os.centos7.conf
install -p -m0644 config/user.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/user.conf



%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.md LICENSE
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/os.centos6.conf
%config(noreplace) %{_sysconfdir}/%{name}/os.centos7.conf
%config(noreplace) %{_sysconfdir}/%{name}/user.conf
%config(noreplace) %{_sysconfdir}/%{name}/master.conf
#%config(noreplace) %{_sysconfdir}/cron.d/*
#%config(noreplace) %{_sysconfdir}/logrotate.d/*
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_unitdir}/clamav-unofficial-sigs.service
%{_unitdir}/clamav-unofficial-sigs.timer
%{_unitdir}/clamd.scan.service
%endif
%{_bindir}/*
%{_mandir}/man8/*
%attr(0755,clamupdate,clamupdate) %dir %{_localstatedir}/log/%{name}
%attr(0755,clamupdate,clamupdate) %dir %{_localstatedir}/lib/%{name}
%attr(0755,clamupdate,clamupdate) %dir %{_localstatedir}/lib/%{name}/ham-test


%post
%if %{with_systemd}
#we are at least on RHEL >= 7, so check if we upgrade an older version of clamav-unofficial-sigs that used a cronjob instead of Systemd timers
if [ -f /etc/cron.d/clamav-unofficial-sigs ];
then
rm -f /etc/cron.d/clamav-unofficial-sigs
fi
#reload unit files
systemctl daemon-reload
#enable timer
/usr/bin/systemctl enable clamav-unofficial-sigs.timer >/dev/null 2>&1 ||:
/usr/bin/systemctl start clamav-unofficial-sigs.timer >/dev/null 2>&1 ||:
/usr/bin/clamav-unofficial-sigs.sh --install-logrotate >/dev/null 2>&1 ||:
%else
/usr/bin/clamav-unofficial-sigs.sh --install-cron >/dev/null 2>&1 ||:
/usr/bin/clamav-unofficial-sigs.sh --install-logrotate >/dev/null 2>&1 ||:
%endif

%postun
%if %{with_systemd}
/usr/bin/systemctl stop clamav-unofficial-sigs.timer >/dev/null 2>&1 ||:
/usr/bin/systemctl disable clamav-unofficial-sigs.timer >/dev/null 2>&1 ||:
if [ -f /usr/lib/systemd/system/clamav-unofficial-sigs.service ]
then
rm -f /usr/lib/systemd/system/clamav-unofficial-sigs.service
fi

if [ -f /usr/lib/systemd/system/clamav-unofficial-sigs.timer ]
then
rm -f /usr/lib/systemd/system/clamav-unofficial-sigs.timer
fi

if [ -f /usr/lib/systemd/system/clamd.scan.service ]
then
rm -f /usr/lib/systemd/system/clamd.scan.service
fi
#reload unit files
systemctl daemon-reload
%else
#remove cronjob
if [ -f /etc/cron.d/clamav-unofficial-sigs ];
then
rm -f /etc/cron.d/clamav-unofficial-sigs
fi
%endif

#remove logrotate file
if [ -f /etc/logrotate.d/clamav-unofficial-sigs ];
then
rm -f /etc/logrotate.d/clamav-unofficial-sigs
fi




%changelog
* Wed Apr 13 2016 Michael Seevogel <michael at michaelseevogel.de> - 5.1.1-1
- Update to 5.1.1

* Fri Apr 08 2016 Michael Seevogel <michael at michaelseevogel.de> - 5.1.0-1
- Update to 5.1.0

* Thu Apr 07 2016 Michael Seevogel <michael at michaelseevogel.de> - 5.0.6-1
- Update to 5.0.6

* Sun Apr 03 2016 Michael Seevogel <michael at michaelseevogel.de> - 5.0.5-4
- Update to 5.0.5

* Mon Jul 20 2015 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.7.2-1
- Update to upstream
- EPEL7 branch
- New source URL and URL at sourceforge (see also debian bug#734593)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 07 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 3.7.1-11
- Add a missing requirement on crontabs to spec file
- Fixes RHBZ#988602

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 Andrew Colin Kissa <andrew@topdog.za.net> - 3.7.1-8
- FIX: bugzilla #842180

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Apr 23 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 3.7.1-5
- FIX: bugzilla #683139

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 02 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 3.7.1-3
- Fixes requested by reviewer

* Thu Dec 23 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 3.7.1-2
- Fixes requested by reviewer

* Tue Jul 20 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 3.7.1-1
- upgraded to latest upstream

* Thu Apr 22 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 3.7-3
- Fix sed error

* Mon Mar 15 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 3.7-2
- Fix the cron entry

* Tue Mar 09 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 3.7-1
- Initial packaging
