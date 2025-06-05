#
# Conditional build:
%bcond_with	sse2		# SSE2 instructions
%bcond_with	tests		# tests

%define		gcc_ver 		6:8
%define		libdrm_ver		2.4.121
%define		llvm_ver		15.0.0
%define		zlib_ver		1.2.8

%ifarch %{x86_with_sse2}
%define		with_sse2	1
%endif
Summary:	OSMesa (off-screen renderer) library
Summary(pl.UTF-8):	Biblioteka OSMesa (renderująca bitmapy w pamięci)
Name:		Mesa-libOSMesa
Version:	25.0.5
Release:	1
License:	MIT
Group:		X11/Libraries
Source0:	https://archive.mesa3d.org/mesa-%{version}.tar.xz
# Source0-md5:	7135bf390ee1b0b002870f76661fdca3
URL:		https://www.mesa3d.org/
BuildRequires:	bison >= 2.4.1
BuildRequires:	elfutils-devel
BuildRequires:	flex >= 2.5.35
BuildRequires:	gcc >= %{gcc_ver}
BuildRequires:	glslang >= 11.3.0
%ifnarch %{arch_with_atomics64}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libdrm-devel >= %{libdrm_ver}
BuildRequires:	libstdc++-devel >= %{gcc_ver}
BuildRequires:	libunwind-devel
BuildRequires:	llvm-devel >= %{llvm_ver}
BuildRequires:	llvm-libclc
BuildRequires:	meson >= 1.4.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-Mako >= 0.8.0
BuildRequires:	python3-PyYAML
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sed >= 4.0
BuildRequires:	spirv-tools-devel >= 2024.3
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	xz
BuildRequires:	zlib-devel >= %{zlib_ver}
BuildRequires:	zstd-devel
Requires:	zlib%{?_isa} >= %{zlib_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# libGLESv1_CM, libGLESv2, libGL, libOSMesa:
#  _glapi_tls_Dispatch is defined in libglapi, but it's some kind of symbol ldd -r doesn't notice(?)
%define		skip_post_check_so	libGLESv1_CM.so.1.* libGLESv2.so.2.* libGL.so.1.* libOSMesa.so.* libGLX_mesa.so.0.*

%description
OSMesa (off-screen renderer) library.

%description -l pl.UTF-8
Biblioteka OSMesa (renderująca bitmapy w pamięci).

%package devel
Summary:	Header file for OSMesa (off-screen renderer) library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki OSMesa (renderującej bitmapy w pamięci)
License:	MIT
Group:		Development/Libraries
Requires:	%{name}-libOSMesa%{?_isa} = %{version}-%{release}
# for <GL/gl.h> only
Requires:	OpenGL-devel
Obsoletes:	Mesa-libOSMesa-static < 18.3

%description devel
Header file for OSMesa (off-screen renderer) library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki OSMesa (renderującej bitmapy w pamięci).

%prep
%setup -q -n mesa-%{version}

%build
%meson \
	-Dplatforms= \
	-Dallow-kcmp=enabled \
	-Dandroid-libbacktrace=disabled \
	-Ddri-drivers-path=%{_libdir}/xorg/modules/dri \
	-Degl=disabled \
	-Dexpat=disabled \
	-Dgallium-d3d12-video=disabled \
	-Dgallium-d3d12-graphics=disabled \
	-Dgallium-drivers=llvmpipe \
	-Dgallium-nine=false \
	-Dgallium-opencl=disabled \
	-Dgallium-rusticl=false \
	-Dgallium-va=disabled \
	-Dgallium-vdpau=disabled \
	-Dgallium-xa=disabled \
	-Dgbm=disabled \
	-Dgles1=disabled \
	-Dgles2=disabled \
	-Dglvnd=disabled \
	-Dglx=disabled \
	-Dintel-rt=disabled \
	-Dlibunwind=enabled \
	-Dllvm=enabled \
	-Dlmsensors=disabled \
	-Dmicrosoft-clc=disabled \
	-Dosmesa=true \
	-Dpower8=disabled \
	-Dshader-cache=enabled \
	-Dshared-glapi=enabled \
	-Dshared-llvm=enabled \
	-Dsse2=%{__true_false sse2} \
	-Dvalgrind=disabled \
	-Dvulkan-drivers= \
	-Dxlib-lease=disabled \
	-Dxmlconfig=disabled \
	-Dzstd=enabled

%meson_build

%{?with_tests:%meson_test}

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

# provided by libglvnd (cannot enable libglvnd here without hardware renderers support)
%{__rm} $RPM_BUILD_ROOT%{_includedir}/GL/{gl,glcorearb,glext}.h
%{__rm} $RPM_BUILD_ROOT%{_includedir}/KHR/khrplatform.h

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOSMesa.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libOSMesa.so.8

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOSMesa.so
%{_includedir}/GL/osmesa.h
%{_pkgconfigdir}/osmesa.pc
