%define		extension gnome-keyring
Summary:	Extension that enables Gnome Keyring integration
Name:		mozilla-addon-%{extension}
Version:	0.6.11
Release:	5
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications/Networking
Source0:	https://github.com/infinity0/mozilla-gnome-keyring/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f6abf2e5bc5de7ad3472998bfd68a763
Patch0:		firefox-32.patch
Patch1:		firefox-33.patch
URL:		https://github.com/infinity0/mozilla-gnome-keyring/
BuildRequires:	libgnome-keyring-devel >= 3.4.0
BuildRequires:	libstdc++-devel
BuildRequires:	pkg-config
BuildRequires:	xulrunner-devel
BuildRequires:	zip
Requires:	libgnome-keyring >= 3.4.0
ExclusiveArch:	%{x8664} %{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# this comes from install.rdf
%define		extension_id	\{6f9d85e0-794d-11dd-ad8b-0800200c9a66\}
%define		extensionsdir	%{_libdir}/mozilla/extensions

# https://developer.mozilla.org/en/XPCOM_ABI#ABI_Naming
%define		platform		unknown
%ifarch %{ix86}
%define		platform		Linux_x86-gcc3
%endif
%ifarch %{x8664}
%define		platform		Linux_x86_64-gcc3
%endif

%description
This extension replaces the default password manager in both Firefox
and Thunderbird with an implementation which stores the passwords in
Gnome keyring.

This allows for safe storage of passwords without prompting for
password after Firefox or Thunderbird has been started.

%prep
%setup -qn mozilla-gnome-keyring-%{version}
%patch0 -p1
%patch1 -p1

%{__sed} -i -e '/^CXXFLAGS/ s/$/ $(OPTFLAGS)/' Makefile

%build
# build ext for current arch only
%{__make} build-xpi \
	PLATFORM=%{platform} \
	VERSION=%{version} \
	XUL_VER_MIN=17.0 \
	CXX="%{__cxx}" \
	LDFLAGS="%{rpmldflags}" \
	OPTFLAGS="%{rpmcxxflags} -fpermissive"

%install
rm -rf $RPM_BUILD_ROOT
# Install Gecko extension
install -d $RPM_BUILD_ROOT%{extensionsdir}/%{extension_id}
cp -a xpi/* $RPM_BUILD_ROOT%{extensionsdir}/%{extension_id}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- icedove
test -L %{_libdir}/icedove/extensions/%{extension_id} || \
	ln -sf %{extensionsdir}/%{extension_id} %{_libdir}/icedove/extensions/%{extension_id}

%triggerun -- icedove
if [ "$1" = "0" ] || [ "$2" = "0" ] && [ -L %{_libdir}/icedove/extensions/%{extension_id} ]; then
	rm -f %{_libdir}/icedove/extensions/%{extension_id}
fi

%files
%defattr(644,root,root,755)
%dir %{extensionsdir}/%{extension_id}
%{extensionsdir}/%{extension_id}/chrome
%{extensionsdir}/%{extension_id}/chrome.manifest
%{extensionsdir}/%{extension_id}/defaults
%{extensionsdir}/%{extension_id}/install.rdf
%dir %{extensionsdir}/%{extension_id}/platform
%dir %{extensionsdir}/%{extension_id}/platform/%{platform}
%dir %{extensionsdir}/%{extension_id}/platform/%{platform}/components
%attr(755,root,root) %{extensionsdir}/%{extension_id}/platform/%{platform}/components/libgnomekeyring.so
