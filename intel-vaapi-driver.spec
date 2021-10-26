%global __cmake_in_source_build 1
%define _legacy_common_support 1

Name:       intel-vaapi-driver
Epoch:      1
Version:    2.4.1
Release:    3%{?dist}
Summary:    VA-API user mode driver for Intel GEN Graphics family
License:    MIT and EPL-1.0
URL:        https://01.org/linuxmedia

Source0:    https://github.com/intel/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:    %{name}.metainfo.xml
Source2:    %{name}.py
# git format-patch 6b01d08aa24937da1375263e07c3cddf5e09e3ef..HEAD
Patch0:     0001-README-fix-coverity-link.patch
Patch1:     0002-Handle-odd-resolution.patch
Patch2:     0003-Avoid-GPU-crash-with-malformed-streams.patch
Patch3:     0004-The-3D-multisample-state-needs-to-be-resent-as-part-.patch
Patch4:     0005-Fix-VP9.2-config-verification.patch

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  git
BuildRequires:  libtool
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(libdrm) >= 2.4.52
BuildRequires:  pkgconfig(libva) >= 1.4.0
BuildRequires:  pkgconfig(libva-drm) >= 1.4.0
BuildRequires:  pkgconfig(libva-wayland) >= 1.1.0
BuildRequires:  pkgconfig(libva-x11) >= 1.4.0
BuildRequires:  pkgconfig(wayland-client) >= 1.11.0
BuildRequires:  pkgconfig(wayland-scanner) >= 1.11.0
BuildRequires:  python2
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  libappstream-glib >= 0.6.3
%endif

Provides:       libva-intel-driver%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      libva-intel-driver < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libva-intel-hybrid-driver%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      libva-intel-hybrid-driver < %{?epoch:%{epoch}:}%{version}-%{release}

%description
VA-API (Video Acceleration API) user mode driver for Intel GEN Graphics family.

%prep
%autosetup -p1

%build
autoreconf -vif

%configure \
    --disable-static \
    --enable-x11 \
    --enable-wayland \
    --enable-hybrid-codec

%make_build

%install
%make_install
find %{buildroot} -name "*.la" -delete

%if 0%{?fedora} || 0%{?rhel} >= 8
# Install AppData and add modalias provides
install -pm 0644 -D %{SOURCE1} %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
%{SOURCE2} src/i965_pciids.h | xargs appstream-util add-provide %{buildroot}%{_metainfodir}/%{name}.metainfo.xml modalias
%endif

%if 0%{?fedora} || 0%{?rhel} >= 8
%check
appstream-util validate --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
%endif

%files
%license COPYING
%doc AUTHORS NEWS README
%{_libdir}/dri/i965_drv_video.so
%if 0%{?fedora} || 0%{?rhel} >= 8
%{_metainfodir}/%{name}.metainfo.xml
%endif

%changelog
* Mon Oct 25 2021 Simone Caronni <negativo17@gmail.com> - 1:2.4.1-3
- Add latest patches from master.

* Wed Apr 14 2021 Simone Caronni <negativo17@gmail.com> - 1:2.4.1-2
- Rework AppStream metadata.
- Fix license.

* Tue Jan  5 2021 Simone Caronni <negativo17@gmail.com> - 1:2.4.1-1
- Update to 2.4.1.

* Mon May 04 2020 Simone Caronni <negativo17@gmail.com> - 1:2.4.0-3
- Small updates to SPEC file, fix build on RHEL/CentOS 7.
- Obsolete also libva-intel-hybrid-driver.

* Fri Mar 20 2020 Simone Caronni <negativo17@gmail.com> - 1:2.4.0-2
- Update to official 2.4.0 release.

* Mon Oct 07 2019 Simone Caronni <negativo17@gmail.com> - 2.4.0.1-1
- Update to latest git snapshot.

* Sat Mar 09 2019 Simone Caronni <negativo17@gmail.com> - 2.3.0-3
- Add upstream patches (2.4.0-pre1).

* Tue Feb 26 2019 Simone Caronni <negativo17@gmail.com> - 2.3.0-2
- Rename to intel-vaapi-driver, as per project name.
- Clean up SPEC file.
- Trim changelog.

* Tue Dec 18 2018 Simone Caronni <negativo17@gmail.com> - 2.3.0-1
- Update to 2.3.0.
- Import Appstream metadata from RPMFusion.
