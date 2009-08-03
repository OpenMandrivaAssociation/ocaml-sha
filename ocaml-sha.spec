Name:           ocaml-sha
Version:        1.5
Release:        %mkrel 1
Summary:        SHA Cryptographic Hash Functions for OCaml
License:        GPL2
Group:          Development/Other
URL:            http://tab.snarc.org/projects/ocaml_sha
Source0:        http://tab.snarc.org/download/ocaml/ocaml_sha-%{version}.tar.bz2
# the command line utilities use argv.(0) (cf mlcmd_renamed)
Patch0:         ocaml-sha-1.4_sumrenamed.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  ocaml-findlib

%description
SHA is a cryptographic hash function.
This provide an interface for OCaml program to use
SHA1, SHA256 and SHA512 functions.

SHA1 implements the second implementation that produce
a 160 bit digest from its input.
SHA256 implements newer version that produce 256 bits digest.
SHA512 produces 512 bits digest.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n ocaml_sha-%{version}
%patch0 -p1

# Adding a META file
cat > META.in <<EOF
name="sha"
description="SHA cryptographic hash functions"
version="%{version}"
archive(byte)="sha1.cma sha256.cma sha512.cma"
archive(native)="sha1.cmxa sha256.cmxa sha512.cmxa"
EOF

# in case it would appear in a futur version
test -f META && (echo "Warning: there is a META file" > /dev/stderr)
test -f META || mv META.in META

%build
make       # the lib
make bins  # the progs

mkdir doc
ocamldoc  sha1.mli  sha256.mli  sha512.mli \
    -colorize-code -html  \
    -d doc

%install
rm -rf %{buildroot}
export DESTDIR=%{buildroot}
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
export DLLDIR=$OCAMLFIND_DESTDIR/stublibs
mkdir -p $OCAMLFIND_DESTDIR/stublibs
mkdir -p $OCAMLFIND_DESTDIR/sha
ocamlfind install sha META ./*.{mli,cmi,cma,a,o,cmxa} sha.cmx sha.cmo
install -d -m 0755 %{buildroot}%{_bindir}
for p in sha*sum ; do mv $p ml$p ; done
# mlcmd_renamed: rename shaXsum by mlshaXsum (conflict with coreutils)
install -m 0755 mlsha*sum %{buildroot}%{_bindir}/
install -m 0755 mlsha1sum %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%dir %{_libdir}/ocaml/sha
%{_libdir}/ocaml/sha/META
%{_libdir}/ocaml/sha/*.cma
%{_libdir}/ocaml/sha/*.cmi
%{_bindir}/mlsha1sum
%{_bindir}/mlsha256sum
%{_bindir}/mlsha512sum

%files devel
%defattr(-,root,root)
%doc sha.test.ml
%doc doc
%{_libdir}/ocaml/sha/*.a
%{_libdir}/ocaml/sha/*.o
%{_libdir}/ocaml/sha/*.cmxa
%{_libdir}/ocaml/sha/*.cmx
%{_libdir}/ocaml/sha/*.cmo
%{_libdir}/ocaml/sha/*.ml*

