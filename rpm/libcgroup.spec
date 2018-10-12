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
Release: 16
License: LGPLv2+
Group: Development/Libraries
URL: http://libcg.sourceforge.net/
Source: %{name}-%{version}.tar.bz2
Patch0: bootstrap_configure.patch

BuildRequires: automake autoconf libtool
BuildRequires: gcc, gcc-c++
BuildRequires: byacc, coreutils, flex

%description
Control groups infrastructure. The library helps manipulate, control,
administrate and monitor control groups and the associated controllers.

%package devel
Summary: Development libraries to develop applications that utilize control groups
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
It provides API to create/delete and modify cgroup nodes. It will also in the
future allow creation of persistent configuration for control groups and
provide scripts to manage that configuration.

%prep
%setup  -q  -n %{name}-%{version}/%{name}
%patch0 -p1

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
