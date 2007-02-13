# TODO:
# - create -libs (to make -devel installable without server)?
# - are static modules (%{_libdir}/*/*.a) usable for anything?
Summary:	A calendar and mail server
Summary(pl.UTF-8):	Serwer kalendarza i poczty
Name:		hula
Version:	r1164
Release:	1.3
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
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,postun):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Provides:	group(hula)
Provides:	user(hula)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hula is a calendar and mail server. The project is focused on building
a calendar and mail server that people love to use, instead of broadly
trying to build a "groupware server" that managers want to deploy.

%description -l pl.UTF-8
Hula to serwer kalendarza i poczty. Projekt ten skupia się na
stworzeniu serwera kalendarza i poczty, który ludzie lubiliby używać,
zamiast próbować stworzyć "serwer pracy grupowej", który menadżerowie
chcieliby wdrożyć.

%package devel
Summary:	Development files for hula
Summary(pl.UTF-8):	Pliki programistyczne serwera hula
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files for developing add-ons for
hula.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia dodatków dla serwera
hula.

%package static
Summary:	Static libraries for hula
Summary(pl.UTF-8):	Statyczne biblioteki hula
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libraries for hula.

%description static -l pl.UTF-8
Statyczne biblioteki hula.

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

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 171 hula
%useradd -u 171 -c "Hula" -g 171 -s /sbin/nologin -r hula

%post
/sbin/ldconfig
/sbin/chkconfig --add hula
%service hula restart

%preun
if [ "$1" = 0 ]; then
	%service hula stop
	/sbin/chkconfig --del hula
fi

%postun
if [ "$1" = "0" ]; then
	/sbin/ldconfig
	%userremove lula
	%groupremove lula
fi

%files
%defattr(644,root,root,755)
%doc HACKING TODO AUTHORS README style-guide.html
#%attr(754,root,root) /etc/rc.d/init.d/hula
%attr(755,root,root) %{_bindir}/hulasqlite
%attr(755,root,root) %{_bindir}/mwcomp
%attr(755,root,root) %{_sbindir}/hulaadmin
%attr(755,root,root) %{_sbindir}/hulaantispam
%attr(755,root,root) %{_sbindir}/hulaavirus
%attr(755,root,root) %{_sbindir}/hulabackup
%attr(755,root,root) %{_sbindir}/hulacalagent
%attr(755,root,root) %{_sbindir}/hulacalcmd
%attr(755,root,root) %{_sbindir}/hulaconnmgr
%attr(755,root,root) %{_sbindir}/huladmc
%attr(755,root,root) %{_sbindir}/hulaforward
%attr(755,root,root) %{_sbindir}/hulageneric
%attr(755,root,root) %{_sbindir}/hulaimap
%attr(755,root,root) %{_sbindir}/hulaindexer
%attr(755,root,root) %{_sbindir}/hulamailprox
%attr(755,root,root) %{_sbindir}/hulamanager
%attr(755,root,root) %{_sbindir}/hulamodweb
%attr(755,root,root) %{_sbindir}/hulanmap
%attr(755,root,root) %{_sbindir}/hulapluspack
%attr(755,root,root) %{_sbindir}/hulapop3
%attr(755,root,root) %{_sbindir}/hulaqueue
%attr(755,root,root) %{_sbindir}/hularules
%attr(755,root,root) %{_sbindir}/hulasendmail
%attr(755,root,root) %{_sbindir}/hulasetup
%attr(755,root,root) %{_sbindir}/hulasmtp
%attr(755,root,root) %{_sbindir}/hulastats
%attr(755,root,root) %{_sbindir}/hulaweb
%attr(755,root,root) %{_sbindir}/hulawebadmin
%attr(755,root,root) %{_sbindir}/mdbtool

%dir %{_libdir}/connmgr
%attr(755,root,root) %{_libdir}/connmgr/lib*.so
%dir %{_libdir}/hulamdb
%attr(755,root,root) %{_libdir}/hulamdb/lib*.so
%dir %{_libdir}/modweb
%{_libdir}/modweb/*.ctp
%attr(755,root,root) %{_libdir}/modweb/lib*.so
%dir %{_libdir}/netmail
%dir %{_libdir}/netmail/schemas
%{_libdir}/netmail/schemas/webadmin.sch
%dir %{_pkgconfigdir}
%{_pkgconfigdir}/hula.pc
%dir %{_libdir}/webadmin
%{_libdir}/webadmin/*.wat

%attr(755,root,root) %{_libdir}/libhulacalcmd.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulaconnio.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulaconnmgr.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulaical.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulaical2.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulalog4c.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulalogger.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulamanagement.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulamdb.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulamemmgr.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulamsgapi.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulanmap.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulastreamio.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulautil.so.0.0.0
%attr(755,root,root) %{_libdir}/libhulaxpl.so.0.0.0
%attr(755,root,root) %{_libdir}/libical-hula.so.0.0.0
%attr(755,root,root) %{_libdir}/libicalss-hula.so.0.0.0
%attr(755,root,root) %{_libdir}/libicalvcal-hula.so.0.0.0
%attr(755,root,root) %{_libdir}/libwacert.so.0.0.0
%attr(755,root,root) %{_libdir}/libwanmail.so.0.0.0
%attr(755,root,root) %{_libdir}/libwastats.so.0.0.0
%attr(755,root,root) %{_libdir}/libwastdobj.so.0.0.0

%dir %{_libdir}/hula
%attr(755,root,root) %{_libdir}/hula/hulamonohelper
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

%{_libdir}/hula/calcmd
%{_libdir}/hula/dav
%{_libdir}/hula/import
%{_libdir}/hula/queue
%{_libdir}/hula/log4net.dll
%{_libdir}/hula/search
%{_datadir}/hula/zoneinfo

%files devel
%defattr(644,root,root,755)
%{_includedir}/hula
%dir %{_libdir}/webadmin
%{_libdir}/webadmin/9stats.wat
%{_pkgconfigdir}/hula-sharp.pc

%attr(755,root,root) %{_libdir}/libhulacalcmd.so
%attr(755,root,root) %{_libdir}/libhulaconnio.so
%attr(755,root,root) %{_libdir}/libhulaconnmgr.so
%attr(755,root,root) %{_libdir}/libhulaical.so
%attr(755,root,root) %{_libdir}/libhulaical2.so
%attr(755,root,root) %{_libdir}/libhulalog4c.so
%attr(755,root,root) %{_libdir}/libhulalogger.so
%attr(755,root,root) %{_libdir}/libhulamanagement.so
%attr(755,root,root) %{_libdir}/libhulamdb.so
%attr(755,root,root) %{_libdir}/libhulamemmgr.so
%attr(755,root,root) %{_libdir}/libhulamsgapi.so
%attr(755,root,root) %{_libdir}/libhulanmap.so
%attr(755,root,root) %{_libdir}/libhulastreamio.so
%attr(755,root,root) %{_libdir}/libhulautil.so
%attr(755,root,root) %{_libdir}/libhulaxpl.so
%attr(755,root,root) %{_libdir}/libical-hula.so
%attr(755,root,root) %{_libdir}/libicalss-hula.so
%attr(755,root,root) %{_libdir}/libicalvcal-hula.so
%attr(755,root,root) %{_libdir}/libwacert.so
%attr(755,root,root) %{_libdir}/libwanmail.so
%attr(755,root,root) %{_libdir}/libwastats.so
%attr(755,root,root) %{_libdir}/libwastdobj.so

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%dir %{_libdir}/connmgr
%{_libdir}/connmgr/lib*.a
%dir %{_libdir}/hulamdb
%{_libdir}/hulamdb/lib*.a
%dir %{_libdir}/modweb
%{_libdir}/modweb/lib*.a
