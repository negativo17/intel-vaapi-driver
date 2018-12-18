Name:       libva-intel-driver
Version:    2.3.0
Release:    1%{?dist}
Summary:    Hardware video decode support for Intel integrated graphics
License:    MIT and EPL
URL:        https://01.org/linuxmedia

Source0:    https://github.com/01org/intel-vaapi-driver/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:    intel-vaapi-driver.metainfo.xml
Source2:    parse-intel-vaapi-driver.py

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

Provides:       intel-vaapi-driver = %{version}-%{release}

%description
Hardware video decode support for Intel integrated graphics.

%prep
%autosetup -n intel-vaapi-driver-%{version}

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
mkdir -p %{buildroot}%{_datadir}/appdata/
install -pm 0644 %{SOURCE1} %{buildroot}%{_datadir}/appdata/
fn=%{buildroot}%{_datadir}/appdata/intel-vaapi-driver.metainfo.xml
%{SOURCE2} src/i965_pciids.h | xargs appstream-util add-provide ${fn} modalias
%endif

%files
%license COPYING
%doc AUTHORS NEWS README
%{_libdir}/dri/i965_drv_video.so
%{_datadir}/appdata/intel-vaapi-driver.metainfo.xml

%changelog
* Tue Dec 18 2018 Simone Caronni <negativo17@gmail.com> - 2.3.0-1
- Update to 2.3.0.
- Import Appstream metadata from RPMFusion.

* Thu Jul 20 2017 Simone Caronni <negativo17@gmail.com> - 1.8.3-1
- Update to 1.8.3.

* Mon Nov 21 2016 Simone Caronni <negativo17@gmail.com> - 1.7.3-1
- Update to 1.7.3.

* Tue Sep 20 2016 Simone Caronni <negativo17@gmail.com> - 1.7.2-1
- Update to 1.7.2.

* Sun Jul 03 2016 Simone Caronni <negativo17@gmail.com> - 1.7.1-1
- Update to 1.7.1.

* Sat Jun 04 2016 Simone Caronni <negativo17@gmail.com> - 1.7.0-2
- Update to 1.7.0.

* Mon Apr 04 2016 Simone Caronni <negativo17@gmail.com> - 1.6.2-2
- Add license macro.
- Update build requirements.
- Always enable ASM code generation.
- Simplify SPEC file.
- Regenerate configure script to avoid runpath and to make wayland optional at
  configure time.

* Thu Dec 17 2015 Nicolas Chauvet <kwizart@gmail.com> - 1.6.2-1
- Update to 1.6.2

* Sat Oct 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 1.6.1-1
- Update to 1.6.1

* Tue May 05 2015 Nicolas Chauvet <kwizart@gmail.com> - 1.5.1-1
- Update to 1.5.1

* Tue Oct 28 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.4.1-1
- Update to 1.4.1

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 02 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.3.1-1
- Update to 1.3.1

* Sat Apr 12 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.3.0-2
- Add missing wayland-scanner BR

* Sat Apr 12 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.3.0-1
- Update to 1.3.0

* Tue Mar 04 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.2.2-2
- Backport patch - rhbz#3193

* Mon Feb 17 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.2.2-1
- Update to 1.2.2

* Tue Oct 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.1-1
- Update to 1.2.1

* Wed Jun 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-1
- Update to 1.2.0

* Wed Mar 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0.20-1
- Update to 1.0.20
- Spec file clean-up

* Fri Nov 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.19-1
- Update to 1.0.19

* Fri Aug 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.18-4
- Update to final 1.0.18

* Wed Jul 11 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.18-3
- Switch to pkgconfig(libudev)

* Mon Jun 04 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.18-1
- Update to 1.0.18

* Sat May 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.15-4
- Introduce --with gen4asm

* Tue Jan 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.15-3
- Add BR intel-gen4asm
- Move pre-built asm code
- Adjust license with EPL

* Mon Jan 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.15-2
- Spec cleanup

* Thu Nov 03 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.15-1
- Rename the package to libva-intel-driver

* Sun Aug 07 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.14-1
- Update to 1.0.14

* Sat Jun 11 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.13-2
- Fix typo when building --with full
- Requires at least the same libva version.

* Wed Jun 08 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.13-1
- Update to 1.0.13

* Sun Apr 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.12-1
- Update to 1.0.12

* Thu Mar 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.10-1
- Switch to additional package using the freedesktop version
- Add git rev from today as patch

* Mon Feb 21 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.10-1
- Update to 1.0.10

* Tue Jan 25 2011 Adam Williamson <awilliam@redhat.com> - 1.0.8-1
- bump to new version
- fix modded tarball to actually not have i965 dir
- merge with the other spec I seem to have lying around somewhere

* Wed Nov 24 2010 Adam Williamson <awilliam@redhat.com> - 1.0.6-1
- switch to upstream from sds branch (sds now isn't carrying any very
  interesting changes according to gwenole)
- pull in the dont-install-test-programs patch from sds
- split out libva-utils again for multilib purposes
- drop -devel package obsolete/provides itself too

* Tue Nov 23 2010 Adam Williamson <awilliam@redhat.com> - 0.31.1-3.sds4
- drop obsoletes and provides of itself (hangover from freeworld)

* Tue Nov 23 2010 Adam Williamson <awilliam@redhat.com> - 0.31.1-2.sds4
- fix the tarball to actually remove the i965 code (duh)

* Thu Oct 7 2010 Adam Williamson <awilliam@redhat.com> - 0.31.1-1.sds4
- initial package (based on package from elsewhere by myself and Nic
  Chauvet with i965 driver removed)
