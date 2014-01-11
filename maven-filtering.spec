%{?_javapackages_macros:%_javapackages_macros}
Name:             maven-filtering
Version:          1.1
Release:          2.1%{?dist}
Summary:          Shared component providing resource filtering
License:          ASL 2.0
URL:              http://maven.apache.org/shared/%{name}/index.html
Source0:          http://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip
BuildArch:        noarch

BuildRequires:    maven-local
BuildRequires:    maven-shared
BuildRequires:    plexus-build-api
BuildRequires:    plexus-containers-component-metadata

Provides:         maven-shared-filtering = 1.0-99
Obsoletes:        maven-shared-filtering < 1.0-99 

%description
These Plexus components have been built from the filtering process/code in 
Maven Resources Plugin. The goal is to provide a shared component for all 
plugins that needs to filter resources.

%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

# Replace plexus-maven-plugin with plexus-component-metadata
%pom_xpath_set "pom:plugin[pom:artifactId[text()='plexus-maven-plugin']]//pom:goal[text()='descriptor']" generate-metadata
%pom_xpath_set "pom:artifactId[text()='plexus-maven-plugin']" plexus-component-metadata

%build
# Tests use a package that is no longer present in plexus-build-api (v0.0.7)
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc DEPENDENCIES LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 19 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-1
- Update to upstream version 1.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0-10
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Nov 27 2012 Tomas Radej <tradej@redhat.com> - 1.0-9
- Added NOTICE to javadoc

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 15 2012 Tomas Radej <tradej@redhat.com> - 1.0-7
- Replaced plexus-maven-plugin with plexus-containers-component-metadata

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 31 2011 Tomas Radej <tradej@redhat.com> - 1.0-5
- Really fixed Provides/Obsoletes

* Wed Aug 31 2011 Tomas Radej <tradej@redhat.com> - 1.0-4
- Fixed Provides/Obsoletes

* Wed Aug 31 2011 Tomas Radej <tradej@redhat.com> - 1.0-3
- Added Provides/Obsoletes

* Tue Aug 16 2011 Tomas Radej <tradej@redhat.com> 1.0-2
- Removed rm -rf {buildroot}

* Tue Aug 16 2011 Tomas Radej <tradej@redhat.com> 1.0-1
- Initial release (thanks to the GULaG team)

