#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.3
%define		qtver		5.15.2
%define		kfname		kjobwidgets

Summary:	Widgets for showing progress of asynchronous jobs
Name:		kf6-%{kfname}
Version:	6.3.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	eff06b84d1d6303d97fc90b137595b2a
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-kcoreaddons-devel >= %{version}
BuildRequires:	kf6-knotifications-devel >= %{version}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	Qt6DBus >= %{qtver}
Requires:	Qt6Widgets >= %{qtver}
Requires:	kf6-dirs
Requires:	kf6-kcoreaddons >= %{version}
Requires:	kf6-kwidgetsaddons >= %{version}
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KJobWIdgets provides widgets for showing progress of asynchronous
jobs.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Widgets-devel >= %{qtver}
Requires:	cmake >= 3.16
Requires:	kf6-kcoreaddons-devel >= %{version}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}6_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}6_qt.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF6JobWidgets.so.6
%attr(755,root,root) %{_libdir}/libKF6JobWidgets.so.*.*
%{_datadir}/dbus-1/interfaces/kf6_org.kde.JobView.xml
%{_datadir}/dbus-1/interfaces/kf6_org.kde.JobViewServer.xml
%{_datadir}/dbus-1/interfaces/kf6_org.kde.JobViewV2.xml
%{_datadir}/qlogging-categories6/kjobwidgets.categories
%{_datadir}/qlogging-categories6/kjobwidgets.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KJobWidgets
%{_libdir}/cmake/KF6JobWidgets
%{_libdir}/libKF6JobWidgets.so
