AutoReqProv: no
%define debug_package %{nil}

# end of distribution specific definitions

Summary:    Cryptography and SSL/TLS Toolkit
Name:       ea-openssl
Version:    1.0.2k
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4544 for more details
%define release_prefix 6
Release: %{release_prefix}%{?dist}.cpanel
License:    OpenSSL
Group:      System Environment/Libraries
URL:        https://www.openssl.org/
Vendor:     OpenSSL
Source0:    https://www.openssl.org/source/openssl-%{version}.tar.gz
BuildRoot:  %{_tmppath}/openssl-%{version}-%{release}-root-%(%{__id_u} -n)

# Build changes
Patch1: openssl-1.0.2a-enginesdir.patch

Provides: ea-openssl

%description
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library. The project is managed by a worldwide community of volunteers that use the Internet to communicate, plan, and develop the OpenSSL toolkit and its related documentation.
OpenSSL is based on the excellent SSLeay library developed by Eric Young and Tim Hudson. The OpenSSL toolkit is licensed under an Apache-style license, which basically means that you are free to get and use it for commercial and non-commercial purposes subject to some simple license conditions.

%package devel
Summary: Files for development of applications which will use OpenSSL
Group: Development/Libraries
Requires: krb5-devel%{?_isa}, zlib-devel%{?_isa}
Requires: pkgconfig

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

#%package static
#Summary:  Libraries for static linking of applications which will use OpenSSL
#Group: Development/Libraries
#Requires: %{name}-devel%{?_isa} = %{version}-%{release}
#
#%description static
#OpenSSL is a toolkit for supporting cryptography. The openssl-static
#package contains static libraries needed for static linking of
#applications which support various cryptographic algorithms and
#protocols.

%prep
%setup -q -n openssl-%{version}

%patch1 -p1 -b .enginesdir

%build
./config \
	--prefix=/opt/cpanel/ea-openssl \
	--openssldir=/opt/cpanel/ea-openssl \
	no-ssl2 no-ssl3 no-shared -fPIC

make depend
make all
make rehash
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/opt/cpanel/ea-openssl/ssl/openssl1.0.2

make INSTALL_PREFIX=$RPM_BUILD_ROOT install

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
%dir /opt/cpanel/ea-openssl/
/opt/cpanel/ea-openssl/*

%files devel
%defattr(-,root,root)
/opt/cpanel/ea-openssl/include/openssl/


%post

%postun

%changelog
* Fri Jul 14 2017 Cory McIntire <cory@cpanel.net> - 1.0.2k-6
- EA-6544: remove CloudFlare patch to stop website breakage

* Thu Jun 08 2017 Jacob Perkins <jacob.perkins@cpanel.net> - 1.0.2k-5
- Move from experimental to production
