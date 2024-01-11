%global base_name       compress
%global short_name      commons-%{base_name}

Name:           apache-%{short_name}
Version:        1.20
Release:        3%{?dist}
Summary:        Java API for working with compressed files and archivers
License:        ASL 2.0
URL:            http://commons.apache.org/proper/commons-compress/
BuildArch:      noarch

Source0:        http://archive.apache.org/dist/commons/compress/source/%{short_name}-%{version}-src.tar.gz

Patch0:         0001-Remove-Brotli-compressor.patch
Patch1:         0002-Remove-ZSTD-compressor.patch
Patch2:         0003-Avoid-use-of-internal-Mockito-API.patch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.mockito:mockito-core)
BuildRequires:  mvn(org.osgi:osgi.core)
BuildRequires:  mvn(org.tukaani:xz)

%description
The Apache Commons Compress library defines an API for working with
ar, cpio, Unix dump, tar, zip, gzip, XZ, Pack200 and bzip2 files.
In version 1.14 read-only support for Brotli decompression has been added,
but it has been removed form this package.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n %{short_name}-%{version}-src

# Unavailable Google Brotli library (org.brotli.dec)
%patch0 -p1
%pom_remove_dep org.brotli:dec
rm -r src/{main,test}/java/org/apache/commons/compress/compressors/brotli

# Unavailable ZSTD JNI library
%patch1 -p1
%pom_remove_dep :zstd-jni
rm -r src/{main,test}/java/org/apache/commons/compress/compressors/zstandard
rm src/test/java/org/apache/commons/compress/compressors/DetectCompressorTestCase.java

# Avoid using internal Mockito APIs
%patch2 -p1

# remove osgi tests, we don't have deps for them
%pom_remove_dep org.ops4j.pax.exam:::test
%pom_remove_dep :org.apache.felix.framework::test
%pom_remove_dep :javax.inject::test
%pom_remove_dep :slf4j-api::test
rm src/test/java/org/apache/commons/compress/OsgiITest.java

# use osgi-core instead of felix-osgi-core
%pom_change_dep :org.osgi.core org.osgi:osgi.core

# Remove test that requires powermock
%pom_remove_dep org.powermock:
%pom_add_dep org.mockito:mockito-core::test
rm src/test/java/org/apache/commons/compress/compressors/z/ZCompressorInputStreamTest.java

# Generate Java 8 level bytecode when built on Java 11
%pom_xpath_replace "pom:maven.compiler.release" "<maven.compiler.release>8</maven.compiler.release>"

%build
%mvn_file  : %{short_name} %{name}
%mvn_alias : commons:
%mvn_build -- -Dcommons.osgi.symbolicName=org.apache.commons.compress

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Thu Jul 16 2020 Mat Booth <mat.booth@redhat.com> - 1.20-3
- Ensure Java 8 level bytecode when built on Java 11

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1.20-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Mon Mar 02 2020 Fabio Valentini <decathorpe@gmail.com> - 1.20-1
- Update to version 1.20.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 04 2019 Fabio Valentini <decathorpe@gmail.com> - 1.19-1
- Update to version 1.19.

* Wed Sep 18 2019 Fabio Valentini <decathorpe@gmail.com> - 1.18-7
- Migrate from the obsolete felix-osgi-core to osgi-core.

* Wed Aug 14 2019 Fabio Valentini <decathorpe@gmail.com> - 1.18-6
- Remove build-dependency on powermock

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 14 2019 Mat Booth <mat.booth@redhat.com> - 1.18-4
- Rebuild to regenerate OSGi metadata

* Thu Feb 07 2019 Mat Booth <mat.booth@redhat.com> - 1.18-3
- Fix test suite build against Mockito 2.x

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 05 2018 Marian Koncek <mkoncek@redhat.com> - 1.18-1
- Update to upstream version 1.18
- CVE-2018-11771

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 05 2018 Michael Simacek <msimacek@redhat.com> - 1.17-1
- Update to upstream version 1.17

* Mon Feb 12 2018 Michael Simacek <msimacek@redhat.com> - 1.16.1-1
- Update to upstream version 1.16.1

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 22 2017 Michael Simacek <msimacek@redhat.com> - 1.15-1
- Update to upstream version 1.15

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Roman Vais <rvais@redhat.com> - 1.14-1
- Update to upstream version 1.14
- Remove Brotli support, it is not packaged for fedora 

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Michael Simacek <msimacek@redhat.com> - 1.13-1
- Update to upstream version 1.13

* Wed Jun 22 2016 Michael Simacek <msimacek@redhat.com> - 1.12-1
- Update to upstream version 1.12

* Mon May 02 2016 Michael Simacek <msimacek@redhat.com> - 1.11-1
- Update to upstream version 1.11

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-0.3.svn1684406
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-0.2.svn1684406
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  9 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10-0.1.svn1684406
- Update to latest upstream snapshot

* Tue Oct 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-2
- Remove legacy Obsoletes/Provides for jakarta-commons

* Mon Oct 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-1
- Update to upstream version 1.9

* Wed Jul 30 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8.1-3
- Fix build-requires on apache-commons-parent

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8.1-1
- Update to upstream version 1.8.1

* Mon Mar 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8-2
- Remove dependency on maven-scm-publish-plugin

* Fri Mar 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8-1
- Update to upstream version 1.8

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.7-2
- Use Requires: java-headless rebuild (#1067528)

* Mon Jan 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7-1
- Update to upstream version 1.7

* Tue Oct 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-1
- Update to upstream version 1.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5-1
- Update to upstream version 1.5

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.4.1-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jan  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.1-4
- Bump release tag

* Tue Jan  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.1-3
- Build with xmvn
- Update to current packaging guidelines

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Sandro Mathys <red at fedoraproject.org> - 1.4.1-1
- Updated to 1.4.1
- Fixes CVE-2012-2098 Low: Denial of Service

* Fri Apr 27 2012 Sandro Mathys <red at fedoraproject.org> - 1.4-1
- Updated to 1.4

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 01 2011 Sandro Mathys <red at fedoraproject.org> - 1.3-1
- Updated to 1.3

* Thu Aug 04 2011 Sandro Mathys <red at fedoraproject.org> - 1.2-2
- Fixing mistake where different versions of the spec file got mixed up

* Thu Aug 04 2011 Sandro Mathys <red at fedoraproject.org> - 1.2-1
- Updated to 1.2

* Sat Apr 16 2011 Chris Spike <spike@fedoraproject.org> 1.1-1
- Updated to 1.1
- Adapted to current java packaging guidelines

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 11 2010 Sandro Mathys <red at fedoraproject.org> - 1.0-8
- Fixed the Maven depmap line by replacing org.apache.maven by org.apache.commons

* Mon May 31 2010 Sandro Mathys <red at fedoraproject.org> - 1.0-7
- Fixed regression with missing Provides/Obsoletes for javadocs
- Fixed changelog format

* Sun May 23 2010 Sandro Mathys <red at fedoraproject.org> - 1.0-6
- Fixed Maven depmap to use commons-compress

* Thu May 13 2010 Sandro Mathys <red at fedoraproject.org> - 1.0-5
- Added missing Provides/Obsoletes for javadocs 

* Mon May 10 2010 Sandro Mathys <red at fedoraproject.org> - 1.0-4
- Cleared some problems after the review

* Thu May 06 2010 Sandro Mathys <red at fedoraproject.org> - 1.0-3
- Now using maven2 (mvn-jpp) instead of directly calling javac & co

* Tue May 04 2010 Sandro Mathys <red at fedoraproject.org> - 1.0-2
- Renamed from jakarta-commons-compress
