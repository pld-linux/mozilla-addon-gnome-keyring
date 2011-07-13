%define		extension gnome-keyring
Summary:	Extension that enables Gnome Keyring integration
Name:		mozilla-addon-%{extension}
Version:	0.5.1
Release:	0.1
License:	GPL
Group:		X11/Applications/Networking
Source0:	https://github.com/mdlavin/firefox-gnome-keyring/tarball/master#/%{name}-%{version}.tgz
# Source0-md5:	148bf938edeaa641aa5b6c7f70bbf599
URL:		https://github.com/mdlavin/firefox-gnome-keyring
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkg-config
BuildRequires:	zip
BuildRequires:	xulrunner-devel
ExclusiveArch:	%{x8664} %{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# this comes from install.rdf
%define		extension_id	\{6f9d85e0-794d-11dd-ad8b-0800200c9a66\}
%define		extensionsdir	%{_libdir}/mozilla/extensions
%ifarch %{ix86}
%define		arch	x86
%endif
%ifarch %{x8664}
%define		arch	x86_64
%endif

%description
This extension replaces the default password manager in both Firefox
and Thunderbird with an implementation which stores the passwords in
Gnome keyring.

This allows for safe storage of passwords without prompting for
password after Firefox or Thunderbird has been started.

%prep
%setup -qc
mv *-gnome-keyring-*/* .

rm -vf *.xpi
rm -rf lib

# remove dep to build both arch
sed -i -e ' /^build-xpi:/s,build-library-.*,,' Makefile

grep 'VERSION.*= %{version}' Makefile

%build
# build ext for current arch only
%{__make} build-library-%{arch} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags}"
# this one will subst version in install.rdf
%{__make} build-xpi

%install
rm -rf $RPM_BUILD_ROOT
# Install Gecko extension
install -d $RPM_BUILD_ROOT%{extensionsdir}/%{extension_id}
cp -a xpi/* $RPM_BUILD_ROOT%{extensionsdir}/%{extension_id}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{extensionsdir}/%{extension_id}
%{extensionsdir}/%{extension_id}/chrome.manifest
%{extensionsdir}/%{extension_id}/install.rdf
%dir %{extensionsdir}/%{extension_id}/platform
%dir %{extensionsdir}/%{extension_id}/platform/Linux_*-gcc3/components
%attr(755,root,root) %{extensionsdir}/%{extension_id}/platform/Linux_*-gcc3/components/libgnomekeyring.so
