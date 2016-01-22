Summary:	Extension that enables Gnome Keyring integration
Name:		mozilla-addon-gnome-keyring
Version:	0.10
Release:	4
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
%define		extension_id		gnome-keyring-integration@sebastianwick.net

%define		extensionsdir		/usr/lib/mozilla/extensions

%define		iceweasel_dir	%{_datadir}/iceweasel/browser/extensions
%define		icedove_dir		%{_libdir}/icedove/extensions

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
install -d $RPM_BUILD_ROOT%{extensionsdir}/%{extension_id}
unzip bin/*.xpi -d $RPM_BUILD_ROOT%{extensionsdir}/%{extension_id}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- %{name} < 0.10-4
rm -f %{icedove_dir}/"{6f9d85e0-794d-11dd-ad8b-0800200c9a66}"
rm -f %{icedove_dir}/"{3550f703-e582-4d05-9a08-453d09bdfdc6}"

%triggerin -- icedove
test -L %{icedove_dir}/%{extension_id} || \
	ln -sf %{extensionsdir}/%{extension_id} %{icedove_dir}/%{extension_id}

%triggerun -- icedove
if [ "$1" = "0" ] || [ "$2" = "0" ] && [ -L %{icedove_dir}/%{extension_id} ]; then
	rm -f %{icedove_dir}/%{extension_id}
fi

%triggerin -- iceweasel
test -L %{iceweasel_dir}/%{extension_id} || \
	ln -sf %{extensionsdir}/%{extension_id} %{iceweasel_dir}/%{extension_id}

%triggerun -- iceweasel
if [ "$1" = "0" ] || [ "$2" = "0" ] && [ -L %{iceweasel_dir}/%{extension_id} ]; then
	rm -f %{iceweasel_dir}/%{extension_id}
fi

%files
%defattr(644,root,root,755)
%dir %{extensionsdir}/%{extension_id}
%{extensionsdir}/%{extension_id}/chrome.manifest
%{extensionsdir}/%{extension_id}/install.rdf
%{extensionsdir}/%{extension_id}/chrome
%{extensionsdir}/%{extension_id}/components
%{extensionsdir}/%{extension_id}/content
%{extensionsdir}/%{extension_id}/defaults
