AutoReqProv: no
%define debug_package %{nil}

# end of distribution specific definitions

Summary:    Cryptography and SSL/TLS Toolkit
Name:       ea-openssl
Version:    1.0.2k
Release:    2%{?dist}
License:    OpenSSL
Group:      System Environment/Libraries
URL:        https://www.openssl.org/
Vendor:     OpenSSL
Source0:    https://www.openssl.org/source/openssl-%{version}.tar.gz
BuildRoot:  %{_tmppath}/openssl-%{version}-%{release}-root-%(%{__id_u} -n)

# Build changes
Patch1: openssl-1.0.2a-enginesdir.patch
Patch2: openssl__chacha20_poly1305.patch

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
%patch2 -p1 -b .chacha20_poly1305

%build
./config --prefix=/opt/ea4/openssl --openssldir=/opt/ea4/openssl no-ssl2 no-ssl3 no-shared -fPIC


make depend
make all
make rehash
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/opt/ea4/openssl/ssl/openssl1.0.2

make INSTALL_PREFIX=$RPM_BUILD_ROOT install

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
%dir /opt/ea4/openssl/
/opt/ea4/openssl/*

%files devel
%defattr(-,root,root)
/opt/ea4/openssl/include/openssl/


%post

%postun

