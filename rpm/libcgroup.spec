# based on work by The Fedora Project (2017)
# Copyright (c) 1998, 1999, 2000 Thai Open Source Software Center Ltd
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

%global soversion_major 1
%global soversion 1.0.41
%global _hardened_build 1

Summary: Library to control and monitor control groups
Name: libcgroup
Version: 0.41
Release: 16%{?dist}
License: LGPLv2+
Group: Development/Libraries
URL: http://libcg.sourceforge.net/
Source: %{name}-%{version}.tar.bz2
Patch0: bootstrap_configure.patch
#Patch0: fedora-config.patch
#Patch1: libcgroup-0.37-chmod.patch
#Patch2: libcgroup-0.40.rc1-coverity.patch
#Patch3: libcgroup-0.40.rc1-fread.patch
#Patch4: libcgroup-0.40.rc1-templates-fix.patch
#Patch5: libcgroup-0.41-lex.patch
#Patch6: libcgroup-0.41-api.c-support-for-setting-multiline-values-in-contro.patch
## resolves #1348874
#Patch7: libcgroup-0.41-api.c-fix-order-of-memory-subsystem-parameters.patch
## resolves #1384504
#Patch8: libcgroup-0.41-api.c-preserve-dirty-flag.patch

BuildRequires: automake autoconf libtool
BuildRequires: gcc, gcc-c++
BuildRequires: byacc, coreutils, flex

%description
Control groups infrastructure. The library helps manipulate, control,
administrate and monitor control groups and the associated controllers.

%package devel
Summary: Development libraries to develop applications that utilize control groups
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
It provides API to create/delete and modify cgroup nodes. It will also in the
future allow creation of persistent configuration for control groups and
provide scripts to manage that configuration.

%prep
%setup  -q  -n %{name}-%{version}/%{name}
%patch0 -p1
#%patch0 -p1 -b .config-patch
#%patch1 -p1 -b .chmod
#%patch2 -p1 -b .coverity
#%patch3 -p1 -b .fread
#%patch4 -p1 -b .templates-fix
#%patch5 -p2 -b .lex
#%patch6 -p1
#%patch7 -p1
#%patch8 -p1

%build
./bootstrap.sh
%configure --disable-daemon --disable-tools --disable-pam
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

# get rid of tool config and man files
rm -rf ${RPM_BUILD_ROOT}%{_sysconfdir}
rm -rf ${RPM_BUILD_ROOT}%{_mandir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%doc README
%{_libdir}/libcgroup.so.*

%files devel
%doc COPYING
%doc README
%{_includedir}/libcgroup.h
%{_includedir}/libcgroup/*.h
%{_libdir}/libcgroup.so
%{_libdir}/pkgconfig/libcgroup.pc
