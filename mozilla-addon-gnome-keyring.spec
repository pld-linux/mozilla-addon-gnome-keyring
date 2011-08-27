%define		extension gnome-keyring
Summary:	Extension that enables Gnome Keyring integration
Name:		mozilla-addon-%{extension}
Version:	0.5.1.1
Release:	0.1
License:	GPL
Group:		X11/Applications/Networking
Source0:	https://github.com/mdlavin/firefox-gnome-keyring/tarball/master#/%{name}-%{version}.tgz
# Source0-md5:	18335895a18ea14a2c221559ed848018
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
%define		platform		%(gcc --version --verbose 2>&1 | grep 'Target:' | cut '-d ' -f2)

%description
This extension replaces the default password manager in both Firefox
and Thunderbird with an implementation which stores the passwords in
Gnome keyring.

This allows for safe storage of passwords without prompting for
password after Firefox or Thunderbird has been started.

%prep
%setup -qc
mv *-gnome-keyring-*/* .

%build
# build ext for current arch only
%{__make} build-xpi \
	VERSION=%{version} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags}"

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
%dir %{extensionsdir}/%{extension_id}/platform/%{platform}
%dir %{extensionsdir}/%{extension_id}/platform/%{platform}/components
%attr(755,root,root) %{extensionsdir}/%{extension_id}/platform/%{platform}/components/libgnomekeyring.so
