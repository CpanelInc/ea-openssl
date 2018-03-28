%define debug_package %{nil}
%define pkg_base ea-openssl
%define provider cpanel
%global _prefix /opt/%{provider}/%{pkg_base}
%global _opensslconfdir %{_prefix}/etc

# end of distribution specific definitions

Summary:    Cryptography and SSL/TLS Toolkit
Name:       ea-openssl
Version:    1.0.2n
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4544 for more details
%define release_prefix 3
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
    -Wl,-rpath=%{_prefix}/%{_lib} \
    --prefix=%{_prefix} \
    --openssldir=%{_opensslconfdir}/pki/tls \
    no-ssl2 no-ssl3 shared -fPIC \

make depend
make all
make rehash
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_prefix}/ssl/openssl1.0.2

make INSTALL_PREFIX=$RPM_BUILD_ROOT install

for lib in $RPM_BUILD_ROOT%{_prefix}/lib/*.so ; do
    chmod 755 ${lib}
    pwd
    ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_prefix}/lib/`basename ${lib}`.10
done

# so PHP et all can find it on 64 bit machines
rm -f $RPM_BUILD_ROOT%{_prefix}/lib64
ln -s %{_prefix}/lib $RPM_BUILD_ROOT/opt/cpanel/ea-openssl/lib64

## Symlink to system certs

%__rm -rf $RPM_BUILD_ROOT%{_opensslconfdir}/pki/tls/{cert.pem,certs,misc,private}
%__ln_s /etc/pki/tls/cert.pem $RPM_BUILD_ROOT%{_opensslconfdir}/pki/tls/
%__ln_s /etc/pki/tls/certs $RPM_BUILD_ROOT%{_opensslconfdir}/pki/tls/
%__ln_s /etc/pki/tls/misc $RPM_BUILD_ROOT%{_opensslconfdir}/pki/tls/
%__ln_s /etc/pki/tls/private $RPM_BUILD_ROOT%{_opensslconfdir}/pki/tls/

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
%dir %{_prefix}/
%{_prefix}/bin
%{_prefix}/lib
%{_prefix}/lib64
%docdir %{_prefix}/man
%{_prefix}/ssl
%{_prefix}/etc
%config(noreplace) %{_opensslconfdir}/pki/tls/openssl.cnf
%attr(0755,root,root) %{_prefix}/lib/libcrypto.so.1.0.0
%attr(0755,root,root) %{_prefix}/lib/libssl.so.1.0.0
%attr(0755,root,root) %{_prefix}/lib/libssl.so.10

%files devel
%defattr(-,root,root)
%{_prefix}/include

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Wed Mar 21 2018 Rishwanth Yeddula <rish@cpanel.net> - 1.0.2n-3
- EA-7327: Added further configuration for shared openssl.

* Mon Feb 19 2018 Cory McIntire <cory@cpanel.net> - 1.0.2n-2
- ZC-3456: Adjust ea-openssl to build shared.

* Tue Jan 09 2018 Cory McIntire <cory@cpanel.net> - 1.0.2n-1
- EA-7086: Update ea-openssl from 1.0.2m to 1.0.2n for CVE-2017-3737

* Tue Nov 07 2017 Dan Muey <dan@cpanel.net> - 1.0.2m-3
- EA-6812: add lib64 symlink so PHP can find what it needs

* Fri Nov 03 2017 Dan Muey <dan@cpanel.net> - 1.0.2m-2
- EA-6953: fix %files so only -devel owns includes

* Thu Nov 02 2017 Cory McIntire <cory@cpanel.net> - 1.0.2m-1
- EA-6951: Update ea-openssl from 1.0.2k to 1.0.2m

* Mon Aug 14 2017 Cory McIntire <cory@cpanel.net> - 1.0.2k-7
- EA-6671: add symlinks to system default certs

* Fri Jul 14 2017 Cory McIntire <cory@cpanel.net> - 1.0.2k-6
- EA-6544: remove CloudFlare patch to stop website breakage

* Thu Jun 08 2017 Jacob Perkins <jacob.perkins@cpanel.net> - 1.0.2k-5
- Move from experimental to production
