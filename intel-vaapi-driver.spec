Name:       intel-vaapi-driver
Version:    2.3.0
Release:    3%{?dist}
Summary:    VA-API user mode driver for Intel GEN Graphics family
License:    MIT and EPL
URL:        https://01.org/linuxmedia

Source0:    https://github.com/01org/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:    %{name}.metainfo.xml
Source2:    %{name}.py

# Upstream patches
# git format-patch 72f10f16f7e5767492acde130eeeaa598d26a3a6..HEAD
Patch0:     0001-HEVC-encoder-correct-the-minimal-bitrate-for-VBR.patch
Patch1:     0002-Check-the-interface-from-libva-first.patch
Patch2:     0003-build-meson-compile-without-wayland-support.patch
Patch3:     0004-Revert-VPP-clear-a-surface-using-media-pipeline-on-G.patch
Patch4:     0005-Return-false-instead-of-assertion-failure.patch
Patch5:     0006-android-ignore-unimportant-compile-warnnings.patch
Patch6:     0007-android-avoid-compile-warnnings.patch
Patch7:     0008-Remove-dependency-on-EncROI-attribute-to-enable-enco.patch
Patch8:     0009-Fix-off-by-one-in-use-of-ROI-regions-in-CQP-mode.patch

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  m4
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(intel-gen4asm) >= 1.9
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
# install AppData and add modalias provides
install -pm 0644 -D %{SOURCE1} %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
%{SOURCE2} src/i965_pciids.h | xargs appstream-util add-provide %{buildroot}%{_metainfodir}/%{name}.metainfo.xml modalias
%endif

%files
%license COPYING
%doc AUTHORS NEWS README
%{_libdir}/dri/i965_drv_video.so
%{_metainfodir}/%{name}.metainfo.xml

%changelog
* Sat Mar 09 2019 Simone Caronni <negativo17@gmail.com> - 2.3.0-3
- Add upstream patches (2.4.0-pre1).

* Tue Feb 26 2019 Simone Caronni <negativo17@gmail.com> - 2.3.0-2
- Rename to intel-vaapi-driver, as per project name.
- Clean up SPEC file.
- Trim changelog.

* Tue Dec 18 2018 Simone Caronni <negativo17@gmail.com> - 2.3.0-1
- Update to 2.3.0.
- Import Appstream metadata from RPMFusion.
