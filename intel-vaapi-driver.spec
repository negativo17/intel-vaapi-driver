Name:       intel-vaapi-driver
Version:    2.3.0
Release:    2%{?dist}
Summary:    VA-API user mode driver for Intel GEN Graphics family
License:    MIT and EPL
URL:        https://01.org/linuxmedia

Source0:    https://github.com/01org/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:    %{name}.metainfo.xml
Source2:    %{name}.py

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  m4
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(intel-gen4asm) >= 1.9
BuildRequires:  pkgconfig(libdrm) >= 2.4.52
BuildRequires:  pkgconfig(libva) >= 1.1.0
BuildRequires:  pkgconfig(libva-drm) >= 1.1.0
BuildRequires:  pkgconfig(libva-wayland) >= 1.1.0
BuildRequires:  pkgconfig(libva-x11) >= 1.1.0
BuildRequires:  pkgconfig(wayland-client) >= 1.11.0
BuildRequires:  pkgconfig(wayland-scanner) >= 1.11.0
BuildRequires:  python2
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  libappstream-glib >= 0.6.3
%endif

Provides:       libva-intel-driver%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      libva-intel-driver%{?_isa} < %{?epoch:%{epoch}:}%{version}-%{release}

%description
VA-API (Video Acceleration API) user mode driver for Intel GEN Graphics family.

%prep
%autosetup

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
* Tue Feb 26 2019 Simone Caronni <negativo17@gmail.com> - 2.3.0-2
- Rename to intel-vaapi-driver, as per project name.
- Clean up SPEC file.
- Trim changelog.

* Tue Dec 18 2018 Simone Caronni <negativo17@gmail.com> - 2.3.0-1
- Update to 2.3.0.
- Import Appstream metadata from RPMFusion.
