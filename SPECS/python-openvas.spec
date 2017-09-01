#
# SPEC file for package python_openvas.
#

Name:           python-openvas
Version:        %{ver}
Release:        1%{?dist}
Summary:        Python wrapper for OpenVAS Scanner
Vendor:         CERN
License:        GPL3
Source:         %{name}-%{version}.tgz
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python >= 2.7
Requires:       python-progressbar
Requires:       openvas-libraries
Requires:       openvas-scanner
Prefix:         %{_prefix}

%if %{defined rhel_version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%endif

%description
Python wrapper for OpenVAS Scanner

%prep
%setup -q

%build
VERSION="%{ver}" python setup.py build

%install
VERSION="%{ver}" python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
* Thu Aug 31 2017 Yohan Pipereau <yohan.pipereau at cern.ch>
- Initial commit and build.
