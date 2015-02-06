Name:           ocaml-sha
Version:        1.7
Release:        3
Summary:        SHA Cryptographic Hash Functions for OCaml
License:        LGPL 2.1 or LGPL 3.0
Group:          Development/Other
URL:            http://tab.snarc.org/projects/ocaml_sha
Source0:        http://tab.snarc.org/download/ocaml/ocaml_sha-%{version}.tar.bz2
# the command line utilities use argv.(0) (cf mlcmd_renamed)
Patch0:         ocaml-sha-1.7_sumrenamed.patch
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml

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

%build
make       # the lib
make bins  # the progs
make doc

%install
export DESTDIR=%{buildroot}
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
export DLLDIR=$OCAMLFIND_DESTDIR/stublibs
mkdir -p $OCAMLFIND_DESTDIR/stublibs
mkdir -p $OCAMLFIND_DESTDIR/sha
ocamlfind install sha META ./*.{mli,cmi,cma,a,cmo,cmx,cmxa,so}
install -d -m 0755 %{buildroot}%{_bindir}
for p in sha*sum ; do mv $p ml$p ; done
# mlcmd_renamed: rename shaXsum to mlshaXsum (conflict with coreutils)
install -m 0755 mlsha*sum %{buildroot}%{_bindir}/

%files
%defattr(-,root,root)
%doc README
%dir %{_libdir}/ocaml/sha
%{_libdir}/ocaml/sha/META
%{_libdir}/ocaml/sha/*.cma
%{_libdir}/ocaml/sha/*.cmi
%{_libdir}/ocaml/sha/*.cmo
%{_libdir}/ocaml/stublibs/*.so*
%{_bindir}/mlsha1sum
%{_bindir}/mlsha256sum
%{_bindir}/mlsha512sum

%files devel
%defattr(-,root,root)
%doc sha.test.ml
%doc html
%{_libdir}/ocaml/sha/*.a
%{_libdir}/ocaml/sha/*.cmxa
%{_libdir}/ocaml/sha/*.cmx
%{_libdir}/ocaml/sha/*.ml*



%changelog
* Fri Mar 26 2010 Florent Monnier <blue_prawn@mandriva.org> 1.7-1mdv2010.1
+ Revision: 527566
- updated to version 1.7

* Thu Aug 06 2009 Florent Monnier <blue_prawn@mandriva.org> 1.5-5mdv2010.0
+ Revision: 410894
- corrected makefile
- incremented release number
- corrected conflict names
- corrected loadable stubs

* Mon Aug 03 2009 Florent Monnier <blue_prawn@mandriva.org> 1.5-3mdv2010.0
+ Revision: 408264
- incremented rel number
- corrected META file
- incremented rel number
- missing files now included

* Mon Aug 03 2009 Florent Monnier <blue_prawn@mandriva.org> 1.5-1mdv2010.0
+ Revision: 407795
- updated version

* Sun Jun 28 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.4-5mdv2010.0
+ Revision: 390304
- rebuild

* Wed Feb 25 2009 Florent Monnier <blue_prawn@mandriva.org> 1.4-4mdv2009.1
+ Revision: 344631
- incremented release number
- cmd tools fixed

* Fri Feb 13 2009 Florent Monnier <blue_prawn@mandriva.org> 1.4-3mdv2009.1
+ Revision: 340097
- unpackaged file(s)
- forgot to increm the rel number
- bug with sha(256|512)sum

* Fri Feb 13 2009 Florent Monnier <blue_prawn@mandriva.org> 1.4-2mdv2009.1
+ Revision: 340089
- updated release number
- conflict with coreutils

* Fri Feb 13 2009 Florent Monnier <blue_prawn@mandriva.org> 1.4-1mdv2009.1
+ Revision: 340073
- import ocaml-sha


