-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

Format: 1.0
Source: linux-hwe-6.17
Binary: linux-hwe-6.17-headers-6.17.0-19, linux-hwe-6.17-tools-6.17.0-19, linux-hwe-6.17-cloud-tools-6.17.0-19, linux-image-unsigned-6.17.0-19-generic, linux-image-unsigned-6.17.0-19-generic-dbgsym, linux-image-6.17.0-19-generic, linux-image-6.17.0-19-generic-dbgsym, linux-modules-6.17.0-19-generic, linux-modules-extra-6.17.0-19-generic, linux-headers-6.17.0-19-generic, linux-lib-rust-6.17.0-19-generic, linux-tools-6.17.0-19-generic, linux-cloud-tools-6.17.0-19-generic, linux-buildinfo-6.17.0-19-generic, linux-modules-ipu6-6.17.0-19-generic, linux-modules-ipu7-6.17.0-19-generic, linux-modules-iwlwifi-6.17.0-19-generic, linux-modules-usbio-6.17.0-19-generic, linux-modules-vision-6.17.0-19-generic, linux-image-unsigned-6.17.0-19-generic-64k, linux-image-unsigned-6.17.0-19-generic-64k-dbgsym, linux-modules-6.17.0-19-generic-64k, linux-modules-extra-6.17.0-19-generic-64k, linux-headers-6.17.0-19-generic-64k, linux-lib-rust-6.17.0-19-generic-64k,
 linux-tools-6.17.0-19-generic-64k, linux-cloud-tools-6.17.0-19-generic-64k, linux-buildinfo-6.17.0-19-generic-64k, linux-modules-ipu6-6.17.0-19-generic-64k, linux-modules-ipu7-6.17.0-19-generic-64k, linux-modules-iwlwifi-6.17.0-19-generic-64k, linux-modules-usbio-6.17.0-19-generic-64k,
 linux-modules-vision-6.17.0-19-generic-64k
Architecture: all amd64 armhf arm64 ppc64el s390x
Version: 6.17.0-19.19~24.04.2
Maintainer: Ubuntu Kernel Team <kernel-team@lists.ubuntu.com>
Standards-Version: 3.9.4.0
Vcs-Git: git://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/noble -b hwe-6.17
Testsuite: autopkgtest
Testsuite-Triggers: @builddeps@, build-essential, fakeroot, fuse-overlayfs, gcc-multilib, gdb, git, python3, snapd
Build-Depends: gcc-13, gcc-13-aarch64-linux-gnu [arm64] <cross>, gcc-13-arm-linux-gnueabihf [armhf] <cross>, gcc-13-powerpc64le-linux-gnu [ppc64el] <cross>, gcc-13-riscv64-linux-gnu [riscv64] <cross>, gcc-13-s390x-linux-gnu [s390x] <cross>, gcc-13-x86-64-linux-gnu [amd64] <cross>, autoconf <!stage1>, automake <!stage1>, bc <!stage1>, bindgen-0.65 [amd64 arm64 armhf ppc64el riscv64 s390x], bison <!stage1>, clang-19 [amd64 arm64 armhf ppc64el riscv64 s390x], cpio, curl <!stage1>, debhelper-compat (= 10), default-jdk-headless <!stage1>, dkms <!stage1>, flex <!stage1>, gawk <!stage1>, java-common <!stage1>, kmod <!stage1>, libaudit-dev <!stage1>, libcap-dev <!stage1>, libdebuginfod-dev [amd64 arm64 armhf ppc64el s390x riscv64] <!stage1>, libdw-dev <!stage1>, libelf-dev <!stage1>, libiberty-dev <!stage1>, liblzma-dev <!stage1>, libnewt-dev <!stage1>, libnuma-dev [amd64 arm64 ppc64el s390x] <!stage1>, libpci-dev <!stage1>, libssl-dev <!stage1>, libstdc++-13-dev, libtool <!stage1>, libtraceevent-dev [amd64 arm64 armhf ppc64el s390x riscv64] <!stage1>, libtracefs-dev [amd64 arm64 armhf ppc64el s390x riscv64] <!stage1>, libudev-dev <!stage1>, libunwind8-dev [amd64 arm64 armhf ppc64el] <!stage1>, makedumpfile [amd64] <!stage1>, openssl <!stage1>, pahole [amd64 arm64 armhf ppc64el s390x riscv64] | dwarves (>= 1.21) [amd64 arm64 armhf ppc64el s390x riscv64] <!stage1>, pkg-config <!stage1>, python3 <!stage1>, python3-dev <!stage1>, python3-setuptools, rsync [!i386] <!stage1>, rust-1.82-src [amd64 arm64 armhf ppc64el riscv64 s390x], rustc-1.82 [amd64 arm64 armhf ppc64el riscv64 s390x], rustfmt-1.82 [amd64 arm64 armhf ppc64el riscv64 s390x], uuid-dev <!stage1>, zstd <!stage1>
Build-Depends-Indep: asciidoc <!stage1>, bzip2 <!stage1>, python3-docutils <!stage1>, sharutils <!stage1>, xmlto <!stage1>
Package-List:
 linux-buildinfo-6.17.0-19-generic deb kernel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1
 linux-buildinfo-6.17.0-19-generic-64k deb kernel optional arch=arm64 profile=!stage1
 linux-cloud-tools-6.17.0-19-generic deb devel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1
 linux-cloud-tools-6.17.0-19-generic-64k deb devel optional arch=arm64 profile=!stage1
 linux-headers-6.17.0-19-generic deb devel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1
 linux-headers-6.17.0-19-generic-64k deb devel optional arch=arm64 profile=!stage1
 linux-hwe-6.17-cloud-tools-6.17.0-19 deb devel optional arch=amd64,armhf profile=!stage1
 linux-hwe-6.17-headers-6.17.0-19 deb devel optional arch=all profile=!stage1
 linux-hwe-6.17-tools-6.17.0-19 deb devel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1
 linux-image-6.17.0-19-generic deb kernel optional arch=armhf,ppc64el profile=!stage1
 linux-image-6.17.0-19-generic-dbgsym deb devel optional arch=armhf,ppc64el profile=!stage1
 linux-image-unsigned-6.17.0-19-generic deb kernel optional arch=amd64,arm64,s390x profile=!stage1
 linux-image-unsigned-6.17.0-19-generic-64k deb kernel optional arch=arm64 profile=!stage1
 linux-image-unsigned-6.17.0-19-generic-64k-dbgsym deb devel optional arch=arm64 profile=!stage1
 linux-image-unsigned-6.17.0-19-generic-dbgsym deb devel optional arch=amd64,arm64,s390x profile=!stage1
 linux-lib-rust-6.17.0-19-generic deb devel optional arch=amd64 profile=!stage1
 linux-lib-rust-6.17.0-19-generic-64k deb devel optional arch=amd64 profile=!stage1
 linux-modules-6.17.0-19-generic deb kernel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1
 linux-modules-6.17.0-19-generic-64k deb kernel optional arch=arm64 profile=!stage1
 linux-modules-extra-6.17.0-19-generic deb kernel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1
 linux-modules-extra-6.17.0-19-generic-64k deb kernel optional arch=arm64 profile=!stage1
 linux-modules-ipu6-6.17.0-19-generic deb kernel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1
 linux-modules-ipu6-6.17.0-19-generic-64k deb kernel optional arch=arm64 profile=!stage1
 linux-modules-ipu7-6.17.0-19-generic deb kernel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1
 linux-modules-ipu7-6.17.0-19-generic-64k deb kernel optional arch=arm64 profile=!stage1
 linux-modules-iwlwifi-6.17.0-19-generic deb kernel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1
 linux-modules-iwlwifi-6.17.0-19-generic-64k deb kernel optional arch=arm64 profile=!stage1
 linux-modules-usbio-6.17.0-19-generic deb kernel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1
 linux-modules-usbio-6.17.0-19-generic-64k deb kernel optional arch=arm64 profile=!stage1
 linux-modules-vision-6.17.0-19-generic deb kernel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1
 linux-modules-vision-6.17.0-19-generic-64k deb kernel optional arch=arm64 profile=!stage1
 linux-tools-6.17.0-19-generic deb devel optional arch=amd64,armhf,arm64,ppc64el,s390x profile=!stage1
 linux-tools-6.17.0-19-generic-64k deb devel optional arch=arm64 profile=!stage1
Checksums-Sha1:
 4628a8ca90eb9ae3b9edc9054c4e187fa5b05472 248671329 linux-hwe-6.17_6.17.0.orig.tar.gz
 d3d53517b2a7423728848d2a84790f877711f022 2356935 linux-hwe-6.17_6.17.0-19.19~24.04.2.diff.gz
Checksums-Sha256:
 a5623ec5af79da8807e1467e43a1888461c7a445fb1e17533fe45f0fdf4394e3 248671329 linux-hwe-6.17_6.17.0.orig.tar.gz
 2e5766938a4504f0f1cc812c34abca40a78b6de3be7e818dd1378aab28ef139a 2356935 linux-hwe-6.17_6.17.0-19.19~24.04.2.diff.gz
Files:
 9987e29d84285075cf506ddd403dd887 248671329 linux-hwe-6.17_6.17.0.orig.tar.gz
 b8a1fd804c2c32c863fc267720b0bbf5 2356935 linux-hwe-6.17_6.17.0-19.19~24.04.2.diff.gz
Ubuntu-Compatible-Signing: ubuntu/4 pro/3

-----BEGIN PGP SIGNATURE-----

iQJRBAEBCgA7FiEEfiwIK8Bxx+qw8pSyuvL3+R/lFUsFAmmrSrAdHG1hbnVlbC5k
aWV3YWxkQGNhbm9uaWNhbC5jb20ACgkQuvL3+R/lFUv9dw//Z2aw75zVnxegun5F
h4x+2EkqXJSltLqDIRiuCTfjj1V/pvU5aNQ7ThGtGqWWwFTEJfX6mz9zmilGH8Yg
DEQx/4L81QYmn6eOFxgWPmj5v5ILl8fhZyxc6A58U/EMVVSpes2aRQP6DbaZEqxB
l4oxo78I8RPAo5g+3m1XmgyTHRwlgLoLs8lQFnbT/6A4WZ/XuLcGsHpC7tOC70cV
XoLKBnMk4kGIvC9kcQ8IgOqqFvIuOYsbAoUcZ+dEbPmbBNn+pKLQsczddAYL6jdk
3T82koga+4Q+XRb6LPVmrK3Ix4NKcZoEbY1hgLo7Mm6OFpe/oOC/7W+Ept9fLaOO
s2aScpU1PO3NbBrehjSO4hc0VBrVz9KfyNyNVlXotDMCf+7d39jH504tEcJDqMqG
TGMgCZstveze/PF8z/Nlu27xy2IkhQG4SGtUQDsCqgrvpVLmt9AZg2vbA/hWuAPM
y1KkSclj/+M5tgcQyIrZPhnIRIGVvQTgW3rTOB5PxiXwaTVQzamWRadXIZlk8mzW
5gkFA/Hm4CxRwfC/g7izRwnAnSQwIDBA8Jpz4r16IE5LBP9WeCX4RjEnc0ACwMQu
iWqcY0GvXylRekDAYVRNbGYwKpIuEo+sJQSaqAKScSVQQgZmfIG1urjntEU/CEjo
W8o6F7T3yDIqG+AzxXUwzev85uk=
=KmV6
-----END PGP SIGNATURE-----
