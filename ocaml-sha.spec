# The upstream Makefile doesn't work "as is" on Mandriva.
# On Debian too, there the Makefile was replaced by a custom
# one with OCamlMakefile.  With this way the lib is not build
# in the same way than the upstream.
# A lot of OCaml users are under Debian.

Name:           ocaml-sha
Version:        1.4
Release:        %mkrel 1
Summary:        SHA Cryptographic Hash Functions for OCaml
License:        GPL2
Group:          Development/Other
URL:            http://tab.snarc.org/projects/ocaml_sha
Source0:        http://tab.snarc.org/download/ocaml/ocaml_sha-%{version}.tar.bz2
# I don't understand this patch, let's trust its author
Patch0:         ocaml-sha-fixed-makefile.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  ocaml-findlib
# used to generate the documentation
BuildRequires:  ocamlmakefile
BuildRequires:  tetex-latex
BuildRequires:  gzip

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

# custom Makefile which uses OCamlMakefile
cat > Makefile.cust <<EOF
OCAMLMAKEFILE = /usr/share/ocamlmakefile/OCamlMakefile

SOURCES =             \
    sha.ml            \
    sha1.ml           \
    sha1.mli          \
    sha1_stubs.c      \
    sha256.ml         \
    sha256.mli        \
    sha256_stubs.c    \
    sha512.ml         \
    sha512.mli        \
    sha512_stubs.c

RESULT = sha

-include \$(OCAMLMAKEFILE)
EOF

# patch the upstream's Makefile
%patch0 -p1

# Adding a META file
cat > META.in <<EOF
name="sha"
description="SHA cryptographic hash functions"
version="%{version}"
archive(byte)="sha.cma"
archive(native)="sha.cmxa"
EOF

# in case it would appear in a futur version
test -f META && (echo "Warning: there is a META file" > /dev/stderr)
test -f META || mv META.in META

%build
# upstream's Makefile
make       # the lib
make bins  # the progs

# custom's Makefile
make -f Makefile.cust doc
gzip --best doc/sha/latex/doc.ps

%install
rm -rf %{buildroot}
export DESTDIR=%{buildroot}
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
export DLLDIR=$OCAMLFIND_DESTDIR/stublibs
mkdir -p $OCAMLFIND_DESTDIR/stublibs
mkdir -p $OCAMLFIND_DESTDIR/sha
ocamlfind install sha META ./{*.mli,*.cmi,*.cma,*.a,*.cmxa,*.cmx}
install -d -m 0755 %{buildroot}%{_bindir}
for p in sha*sum ; do mv $p ml$p ; done
install -m 0755 mlsha*sum %{buildroot}%{_bindir}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%dir %{_libdir}/ocaml/sha
%{_libdir}/ocaml/sha/META
%{_libdir}/ocaml/sha/*.cma
%{_libdir}/ocaml/sha/*.cmi
%{_bindir}/mlsha*sum

%files devel
%defattr(-,root,root)
%doc sha.test.ml
%doc doc/sha/html
%doc doc/sha/latex/*.{dvi,ps.gz,pdf}
%{_libdir}/ocaml/sha/*.a
%{_libdir}/ocaml/sha/*.cmxa
%{_libdir}/ocaml/sha/*.cmx
%{_libdir}/ocaml/sha/*.ml*

