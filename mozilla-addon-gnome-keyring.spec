# TODO
# - setup symlink for firefox in post script
Summary:	Extension that enables Gnome Keyring integration
Name:		mozilla-addon-gnome-keyring
Version:	0.10
Release:	3
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications/Networking
Source0:	https://github.com/swick/mozilla-gnome-keyring/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e633c093acd2ab86d342fb83fefb95f0
Patch0:		firefox-version.patch
URL:		https://github.com/swick/mozilla-gnome-keyring/
# libgnome-keyring.so.0 is dlopened (content/gnome-keyring.js)
Requires:	libgnome-keyring
# not noarch due to %{_libdir} use in triggers
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# nothing to put there
%define		_enable_debug_packages	0

# this comes from install.rdf
%define		extension_ffox_id	\{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
%define		extension_tbird_id	\{3550f703-e582-4d05-9a08-453d09bdfdc6\}
%define		extension_id		gnome-keyring-integration@sebastianwick.net

%define		extensionsdir		/usr/lib/mozilla/extensions

%description
This extension replaces the default password manager in both Firefox
and Thunderbird with an implementation which stores the passwords in
Gnome keyring.

This allows for safe storage of passwords without prompting for
password after Firefox or Thunderbird has been started.

%prep
%setup -qn mozilla-gnome-keyring-%{version}
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}/%{extension_ffox_id}/%{extension_id}
install -d $RPM_BUILD_ROOT%{extensionsdir}/%{extension_tbird_id}

ln -s %{extensionsdir}/%{extension_ffox_id}/%{extension_id} $RPM_BUILD_ROOT%{extensionsdir}/%{extension_tbird_id}/%{extension_id}

unzip bin/*.xpi -d $RPM_BUILD_ROOT%{extensionsdir}/%{extension_ffox_id}/%{extension_id}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- icedove
test -L %{_libdir}/icedove/extensions/%{extension_tbird_id} || \
	ln -sf %{extensionsdir}/%{extension_tbird_id} %{_libdir}/icedove/extensions/%{extension_tbird_id}

%triggerun -- icedove
if [ "$1" = "0" ] || [ "$2" = "0" ] && [ -L %{_libdir}/icedove/extensions/%{extension_tbird_id} ]; then
	rm -f %{_libdir}/icedove/extensions/%{extension_tbird_id}
fi

%files
%defattr(644,root,root,755)
%dir %{extensionsdir}/%{extension_ffox_id}
%dir %{extensionsdir}/%{extension_ffox_id}/%{extension_id}
%{extensionsdir}/%{extension_ffox_id}/%{extension_id}/chrome.manifest
%{extensionsdir}/%{extension_ffox_id}/%{extension_id}/install.rdf
%{extensionsdir}/%{extension_ffox_id}/%{extension_id}/chrome
%{extensionsdir}/%{extension_ffox_id}/%{extension_id}/components
%{extensionsdir}/%{extension_ffox_id}/%{extension_id}/content
%{extensionsdir}/%{extension_ffox_id}/%{extension_id}/defaults
%dir %{extensionsdir}/%{extension_tbird_id}
%{extensionsdir}/%{extension_tbird_id}/%{extension_id}
