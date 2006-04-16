# TODO
# - register uid in PLD-doc/uid_gid.db.txt and use it
Summary:	A calendar and mail server
Summary(pl):	Serwer kalendarza i poczty
Name:		hula
Version:	r1164
Release:	1
License:	LGPL
Group:		Daemons
Source0:	http://chameleon.mozilla.org/~justdave/hula/%{name}-%{version}.tar.gz
# Source0-md5:	5a3fd9f490e1f0060668ee1316c27522
Source1:	%{name}.init
URL:		http://www.hula-project.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,postun):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Provides:	user(hula)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hula is a calendar and mail server. The project is focused on building
a calendar and mail server that people love to use, instead of broadly
trying to build a "groupware server" that managers want to deploy.

%description -l pl
Hula to serwer kalendarza i poczty. Projekt ten skupia siê na
stworzeniu serwera kalendarza i poczty, który ludzie lubiliby u¿ywaæ,
zamiast próbowaæ stworzyæ "serwer pracy grupowej", który menad¿erowie
chcieliby wdro¿yæ.

%package devel
Summary:	Development files for hula
Summary(pl):	Pliki programistyczne serwera hula
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files for developing add-ons for
hula.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe do tworzenia dodatków dla serwera
hula.

%prep
%setup -q

%build
./autogen.sh \
	--with-user=hula
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/hula

# remove all .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/connmgr/*.la \
	$RPM_BUILD_ROOT%{_libdir}/hulamdb/*.la \
	$RPM_BUILD_ROOT%{_libdir}/*.la \
	$RPM_BUILD_ROOT%{_libdir}/modweb/*.la

# remove empty or irrelevant doco
rm $RPM_BUILD_ROOT/{ChangeLog,INSTALL,NEWS}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Create system user for hula
# TODO: use specific uid
%useradd -c "Hula" -s /sbin/nologin -r hula

%post
/sbin/ldconfig
/sbin/chkconfig --add hula

%preun
if [ "$1" = 0 ]; then
	%service hula stop
	/sbin/chkconfig --del hula
fi

%postun
if [ "$1" = "0" ]; then
	/sbin/ldconfig
	%userremove lula
fi

%files
%defattr(644,root,root,755)
%doc HACKING TODO AUTHORS README style-guide.html
#%attr(754,root,root) /etc/rc.d/init.d/hula
%attr(755,root,root) %{_bindir}/hulasqlite
%attr(755,root,root) %{_bindir}/mwcomp
%attr(755,root,root) %{_sbindir}/hulaavirus
%attr(755,root,root) %{_sbindir}/hulaantispam
%attr(755,root,root) %{_sbindir}/hulacalagent
%attr(755,root,root) %{_sbindir}/hulaconnmgr
%attr(755,root,root) %{_sbindir}/huladmc
%attr(755,root,root) %{_sbindir}/hulaforward
%attr(755,root,root) %{_sbindir}/hulageneric
%attr(755,root,root) %{_sbindir}/hulaimap
%attr(755,root,root) %{_sbindir}/hulamailprox
%attr(755,root,root) %{_sbindir}/hulamanager
%attr(755,root,root) %{_sbindir}/hulamodweb
%attr(755,root,root) %{_sbindir}/hulanmap
%attr(755,root,root) %{_sbindir}/hulapluspack
%attr(755,root,root) %{_sbindir}/hulapop3
%attr(755,root,root) %{_sbindir}/hularules
%attr(755,root,root) %{_sbindir}/hulasendmail
%attr(755,root,root) %{_sbindir}/hulasetup
%attr(755,root,root) %{_sbindir}/hulasmtp
%attr(755,root,root) %{_sbindir}/hulastats
%attr(755,root,root) %{_sbindir}/hulawebadmin
%dir %{_libdir}/connmgr
%{_libdir}/connmgr/libcmlists.so
%{_libdir}/connmgr/libcmrbl.so
%{_libdir}/connmgr/libcmrdns.so
%{_libdir}/connmgr/libcmuser.so
%dir %{_libdir}/hulamdb
%{_libdir}/hulamdb/libmdbfile.so
%dir %{_libdir}/modweb
%{_libdir}/modweb/aurora.ctp
%{_libdir}/modweb/libmwcal.so
%{_libdir}/modweb/libmwmail.so
%{_libdir}/modweb/libmwpref.so
%{_libdir}/modweb/public.ctp
%dir %{_libdir}/netmail/schemas
%{_libdir}/netmail/schemas/webadmin.sch
%dir %{_pkgconfigdir}
%{_pkgconfigdir}/hula.pc
%dir %{_libdir}/webadmin
%{_libdir}/webadmin/1stdobj.wat
%{_libdir}/webadmin/5nmail.wat
%{_libdir}/webadmin/5nmuser.wat
%{_libdir}/webadmin/6nmlist.wat
%{_libdir}/webadmin/6pluspck.wat
%{_libdir}/webadmin/7nmlistu.wat
%{_libdir}/webadmin/8certgen.wat
%{_libdir}/webadmin/chooser.wat
%{_libdir}/webadmin/webadmin.wat
%attr(755,root,root) %{_libdir}/libhulaconnio.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulaconnmgr.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulaical.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulaical2.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulalogger.so.0
%attr(755,root,root) %{_libdir}/libhulalogger.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulamanagement.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulamdb.so.0
%attr(755,root,root) %{_libdir}/libhulamdb.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulamemmgr.so.0
%attr(755,root,root) %{_libdir}/libhulamemmgr.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulamsgapi.so.0
%attr(755,root,root) %{_libdir}/libhulamsgapi.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulanmap.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulastreamio.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulautil.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulaxpl.so.0
%attr(755,root,root) %{_libdir}/libhulaxpl.so.0.0.0
%{_libdir}/libwacert.so
%attr(755,root,root) %{_libdir}/libwacert.so.0
%attr(755,root,root) %{_libdir}/libwacert.so.0.0.0
%{_libdir}/libwanmail.so
%attr(755,root,root) %{_libdir}/libwanmail.so.0
%attr(755,root,root) %{_libdir}/libwanmail.so.0.0.0
%attr(755,root,root) %{_libdir}/libwastats.so.0.0.0
%{_libdir}/libwastdobj.so
%attr(755,root,root) %{_libdir}/libwastdobj.so.0
%attr(755,root,root) %{_libdir}/libwastdobj.so.0.0.0

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/hula
%{_includedir}/hula/calendar.ary
%{_includedir}/hula/calendar.tok
%{_includedir}/hula/cmlib.h
%{_includedir}/hula/connmgr.h
%{_includedir}/hula/connio.h
%{_includedir}/hula/hulautil.h
%{_includedir}/hula/libical.h
%{_includedir}/hula/logger.h
%{_includedir}/hula/management.h
%{_includedir}/hula/mdb.h
%{_includedir}/hula/memmgr.h
%{_includedir}/hula/modweb.ary
%{_includedir}/hula/modweb.h
%{_includedir}/hula/modweb.tok
%{_includedir}/hula/msgaddr.h
%{_includedir}/hula/msgapi.h
%{_includedir}/hula/msgdate.h
%{_includedir}/hula/msgftrs.h
%{_includedir}/hula/mwmail.ary
%{_includedir}/hula/mwmail.tok
%{_includedir}/hula/mwpfsave.c
%{_includedir}/hula/mwpfsave.h
%{_includedir}/hula/mwpref.ary
%{_includedir}/hula/mwpref.tok
%{_includedir}/hula/mwsignup.ary
%{_includedir}/hula/mwsignup.tok
%{_includedir}/hula/mwtempl.h
%{_includedir}/hula/mwtom.ary
%{_includedir}/hula/mwtom.tok
%{_includedir}/hula/nmap.h
%{_includedir}/hula/nmlib.h
%{_includedir}/hula/rfc2231.h
%{_includedir}/hula/rulesrv.h
%{_includedir}/hula/streamio.h
%{_includedir}/hula/wacert.ary
%{_includedir}/hula/wacert.tok
%{_includedir}/hula/wanmail.ary
%{_includedir}/hula/wanmail.tok
%{_includedir}/hula/wastats.ary
%{_includedir}/hula/wastats.tok
%{_includedir}/hula/wastdobj.ary
%{_includedir}/hula/wastdobj.tok
%{_includedir}/hula/webadmin.ary
%{_includedir}/hula/webadmin.h
%{_includedir}/hula/webadmin.tok
%{_includedir}/hula/xpl.h
%{_includedir}/hula/xplold.h
%{_includedir}/hula/xplresolve.h
%{_includedir}/hula/xplschema.h
%{_includedir}/hula/xplservice.h
%{_includedir}/hula/xplthread.h
%{_includedir}/hula/xplutil.h
%{_libdir}/libhulaconnio.a
%{_libdir}/libhulaconnmgr.a
%{_libdir}/libhulaical.a
%{_libdir}/libhulaical2.a
%{_libdir}/libhulalogger.a
%{_libdir}/libhulalogger.so
%{_libdir}/libhulamanagement.a
%{_libdir}/libhulamdb.a
%{_libdir}/libhulamdb.so
%{_libdir}/libhulamemmgr.a
%{_libdir}/libhulamemmgr.so
%{_libdir}/libhulanmap.a
%{_libdir}/libhulamsgapi.a
%{_libdir}/libhulamsgapi.so
%{_libdir}/libhulastreamio.a
%{_libdir}/libhulautil.a
%{_libdir}/libhulaxpl.a
%{_libdir}/libhulaxpl.so
%{_libdir}/libwacert.a
%{_libdir}/libwanmail.a
%{_libdir}/libwastats.a
%{_libdir}/libwastdobj.a
%dir %{_libdir}/connmgr
%{_libdir}/connmgr/libcmlists.a
%{_libdir}/connmgr/libcmrbl.a
%{_libdir}/connmgr/libcmrdns.a
%{_libdir}/connmgr/libcmuser.a
%dir %{_libdir}/hulamdb
%{_libdir}/hulamdb/libmdbfile.a
%dir %{_libdir}/modweb
%{_libdir}/modweb/libmwcal.a
%{_libdir}/modweb/libmwmail.a
%{_libdir}/modweb/libmwpref.a
%dir %{_libdir}/webadmin
%{_libdir}/webadmin/9stats.wat

# unpackaged:
%if 0
%{_includedir}/hula/calcmd.h
%{_includedir}/hula/hulaagent.h
%{_includedir}/hula/hulacheck.h
%{_includedir}/hula/hulathreadpool.h
%{_includedir}/hula/libical/ical.h
%{_includedir}/hula/libical/icalarray.h
%{_includedir}/hula/libical/icalattach.h
%{_includedir}/hula/libical/icalcalendar.h
%{_includedir}/hula/libical/icalclassify.h
%{_includedir}/hula/libical/icalcluster.h
%{_includedir}/hula/libical/icalcomponent.h
%{_includedir}/hula/libical/icalderivedparameter.h
%{_includedir}/hula/libical/icalderivedproperty.h
%{_includedir}/hula/libical/icalderivedvalue.h
%{_includedir}/hula/libical/icaldirset.h
%{_includedir}/hula/libical/icaldirsetimpl.h
%{_includedir}/hula/libical/icalduration.h
%{_includedir}/hula/libical/icalenums.h
%{_includedir}/hula/libical/icalerror.h
%{_includedir}/hula/libical/icalfileset.h
%{_includedir}/hula/libical/icalfilesetimpl.h
%{_includedir}/hula/libical/icalgauge.h
%{_includedir}/hula/libical/icalgaugeimpl.h
%{_includedir}/hula/libical/icallangbind.h
%{_includedir}/hula/libical/icalmemory.h
%{_includedir}/hula/libical/icalmessage.h
%{_includedir}/hula/libical/icalmime.h
%{_includedir}/hula/libical/icalparameter.h
%{_includedir}/hula/libical/icalparser.h
%{_includedir}/hula/libical/icalperiod.h
%{_includedir}/hula/libical/icalproperty.h
%{_includedir}/hula/libical/icalrecur.h
%{_includedir}/hula/libical/icalrestriction.h
%{_includedir}/hula/libical/icalset.h
%{_includedir}/hula/libical/icalspanlist.h
%{_includedir}/hula/libical/icalss.h
%{_includedir}/hula/libical/icalssyacc.h
%{_includedir}/hula/libical/icaltime.h
%{_includedir}/hula/libical/icaltimezone.h
%{_includedir}/hula/libical/icaltypes.h
%{_includedir}/hula/libical/icalvalue.h
%{_includedir}/hula/libical/icalvcal.h
%{_includedir}/hula/libical/port.h
%{_includedir}/hula/libical/pvl.h
%{_includedir}/hula/libical/sspm.h
%{_includedir}/hula/libical/vcaltmp.h
%{_includedir}/hula/libical/vcc.h
%{_includedir}/hula/libical/vobject.h
%{_includedir}/hula/libical2.h
%{_includedir}/hula/log4c.h
%{_includedir}/hula/log4c/appender.h
%{_includedir}/hula/log4c/appender_type_mmap.h
%{_includedir}/hula/log4c/appender_type_stream.h
%{_includedir}/hula/log4c/appender_type_stream2.h
%{_includedir}/hula/log4c/appender_type_syslog.h
%{_includedir}/hula/log4c/buffer.h
%{_includedir}/hula/log4c/category.h
%{_includedir}/hula/log4c/defs.h
%{_includedir}/hula/log4c/init.h
%{_includedir}/hula/log4c/layout.h
%{_includedir}/hula/log4c/layout_type_basic.h
%{_includedir}/hula/log4c/layout_type_dated.h
%{_includedir}/hula/log4c/location_info.h
%{_includedir}/hula/log4c/logging_event.h
%{_includedir}/hula/log4c/priority.h
%{_includedir}/hula/log4c/rc.h
%{_includedir}/hula/log4c/version.h
%{_libdir}/hula/Hula.Sharp.dll
%{_libdir}/hula/Hula.Sharp.dll.mdb
%{_libdir}/hula/HulaIndexer.exe
%{_libdir}/hula/HulaIndexer.exe.config
%{_libdir}/hula/HulaIndexer.exe.mdb
%{_libdir}/hula/HulaWeb.exe
%{_libdir}/hula/HulaWeb.exe.config
%{_libdir}/hula/HulaWeb.exe.mdb
%{_libdir}/hula/Lucene.Net.dll
%{_libdir}/hula/Mono.WebServer.dll
%{_libdir}/hula/calcmd/bin/Hula.CalCmd.dll
%{_libdir}/hula/calcmd/bin/Hula.CalCmd.dll.mdb
%{_libdir}/hula/calcmd/web.config
%{_libdir}/hula/dav/bin/Hula.Dav.dll
%{_libdir}/hula/dav/bin/Hula.Dav.dll.mdb
%{_libdir}/hula/dav/bin/Lucene.Net.dll
%{_libdir}/hula/dav/bin/Mono.WebServer.dll
%{_libdir}/hula/dav/bin/log4net.dll
%{_libdir}/hula/dav/web.config
%{_libdir}/hula/hulamonohelper
%{_libdir}/hula/import/bin/Hula.Import.dll
%{_libdir}/hula/import/bin/Hula.Import.dll.mdb
%{_libdir}/hula/import/web.config
%{_libdir}/hula/log4net.dll
%{_libdir}/hula/queue/bin/Hula.Queue.dll
%{_libdir}/hula/queue/bin/Hula.Queue.dll.mdb
%{_libdir}/hula/queue/web.config
%{_libdir}/hula/search/bin/Hula.Search.dll
%{_libdir}/hula/search/bin/Hula.Search.dll.mdb
%{_libdir}/hula/search/web.config
%attr(755,root,root) %{_libdir}/libhulacalcmd.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulalog4c.so.0.0.0
%attr(755,root,root) %{_libdir}/libical-hula.so.0.0.0
%attr(755,root,root) %{_libdir}/libicalss-hula.so.0.0.0
%attr(755,root,root) %{_libdir}/libicalvcal-hula.so.0.0.0
%{_libdir}/libhulacalcmd.a
%{_libdir}/libhulalog4c.a
%{_pkgconfigdir}/hula-sharp.pc
%attr(755,root,root) %{_sbindir}/hulaadmin
%attr(755,root,root) %{_sbindir}/hulabackup
%attr(755,root,root) %{_sbindir}/hulacalcmd
%attr(755,root,root) %{_sbindir}/hulaindexer
%attr(755,root,root) %{_sbindir}/hulaqueue
%attr(755,root,root) %{_sbindir}/hulaweb
%attr(755,root,root) %{_sbindir}/mdbtool
%{_datadir}/hula/zoneinfo
%endif
