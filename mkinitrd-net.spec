%define name mkinitrd-net
%define version 1.10
%define release %mkrel 31
%define uclibcver 0.9.28
%define busyboxver 1.01

Summary: Network-booting initrd builder 
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
Source1: http://belnet.dl.sourceforge.net/sourceforge/etherboot/mknbi-1.4.3.tar.bz2
Source2: http://www.busybox.net/downloads/busybox-%{busyboxver}.tar.bz2
Source3: http://www.uclibc.org/downloads/uClibc-%{uclibcver}.tar.bz2
Source4: ftp://ftp.linux-wlan.org/pub/linux-wlan-ng/linux-wlan-ng-0.1.13.tar.bz2
Source5: uClibc-%{uclibcver}.config
Source6: busybox-%{busyboxver}.config
Patch0: mkinitrd-net_ppc_build.patch
Patch1: mkinitrd-net_integrated_nfs.patch
Patch2: mkinitrd-net_uclibc_0.9.28.patch
Patch3: mkinitrd-net-new-etherboot-include.patch
Patch4: mkinitrd-net-boot-devfs.patch
Patch5: mkinitrd-net-2.6-support.patch
Patch6: mkinitrd-net-stubborn-nic.patch
Patch8: mkinitrd-net-gcc4.patch
Patch9: mknitrd-net_udev.patch
Patch10: mkinitrd-net-uclibc-toolchain.patch
Patch11: mkinitrd-net-drop-udhcp.patch
Patch12: mkinitrd-net-optional-wlanctl.patch
Patch13: mkinitrd-net-mknbi.patch
Patch14: mknbi-1.4.3-memcmp.patch
Patch15: mkinitrd-net-modprobe-fix.patch
Patch16: mkinitrd-net-count.patch
Patch17: include-modules-set-version.patch
Patch18: mkinitrd-net-unionfs.patch
Patch19: mkinitrd-net-pegasus.patch
Patch20: mkinitrd-net-userargs.patch
Patch21: mkinitrd-net-config.patch

License: GPL/LGPL/MPL
Group: System/Kernel and hardware
URL: http://www.fensystems.co.uk/SRPMS.fensys
Requires: tftp-server binutils
BuildRequires: kernel-source
BuildRequires: glibc-static-devel
Obsoletes: mknbi
Provides: mknbi
ExclusiveArch: %{ix86} ppc

%description
mkinitrd-net allows you to build initial ramdisk images (initrds) suitable
for use with Etherboot and other network-booting software.  This package
contains two main utilities: mkinitrd-net (to build an initrd containing a
specified set of network-card modules) and mknbi (to generate
Etherboot-usable NBI images from a given kernel and initrd).  It also
contains a helper script mknbi-set which will maintain sets of initrds to
match all your currently-installed kernels.

mkinitrd-net uses code from the uClibc, busybox, and Etherboot
projects.

%prep
%setup -q -n initrd -a1 -a2 -a3 -a4
%patch1 -p1 -b .nfs
%patch2 -p1 -b .uclibc
%patch3 -p1 -b .old
%patch4 -p1 -b .devfs
%patch5 -p1 -b .26
%patch6 -p1 -b .nic
%patch9 -p1 -b .udev
%patch8 -p1 -b .gcc4
%patch10 -p1 -b .toolchain
%patch11 -p1 -b .udhcp
%patch12 -p1 -b .wlan
%patch13 -p1 -b .mknbi
%patch14 -p1 -b .memcmp
%patch15 -p1 -b .modprobe
%patch16 -p1 -b .count
%patch17 -p0 -b .set-version
%patch18 -p1 -b .unionfs
%patch19 -p1 -b .pegasus
%patch20 -p1 -b .userargs
%patch21 -p1 -b .config

cp %{SOURCE5} uClibc-%{uclibcver}/.config
cp %{SOURCE6} busybox-%{busyboxver}/.config
%ifarch ppc
%patch0 -p1 -b .ppc
%endif
perl -pi -e "s|fill_from_spec_file_with_perl|$RPM_BUILD_DIR/initrd/uClibc|" uClibc-%{uclibcver}/.config

%build
make LIBDIR=%{_libdir}/mknbi

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall tftpbootdir=$RPM_BUILD_ROOT%{_localstatedir}/tftpboot
touch $RPM_BUILD_ROOT%{_sysconfdir}/dhcpd.conf.etherboot-pcimap.include

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/mknbi-set.conf
%config(noreplace) %{_sysconfdir}/dhcpd.conf.etherboot.include
%ghost %{_sysconfdir}/dhcpd.conf.etherboot-pcimap.include
%{_bindir}/mknbi-*
%{_bindir}/mkelf-*
%{_bindir}/nbitoelf
%{_bindir}/dis*
%{_bindir}/mkinitrd-net
%{_bindir}/include-modules
%{_libdir}/mknbi
%{_libdir}/mkinitrd-net
%{_mandir}/man*/*
%doc README
%doc AUTHORS.busybox LICENSE.busybox
%doc COPYING.wlanctl LICENSE.wlanctl THANKS.wlanctl
%doc COPYING.uClibc
%docdir %{_docdir}/mknbi*
%{_docdir}/mknbi*

