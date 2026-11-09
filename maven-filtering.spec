Name:		maven-filtering
Version:	3.5.1
Release:	1
Summary:	Shared Maven resource filtering
Group:		Development/Java
License:	Apache-2.0
URL:		https://maven.apache.org/shared/maven-filtering/
Source0:	https://github.com/apache/maven-filtering/archive/refs/tags/maven-filtering-%{version}.tar.gz#/maven-filtering-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python
# The maven RPM holds the class jars. maven-components owns the coordinates.
BuildRequires:	maven
BuildRequires:	maven-components >= 3.10.0
BuildRequires:	java-current-devel
BuildRequires:	mvn(org.apache.maven:maven-core)
BuildRequires:	mvn(org.apache.maven:maven-model)
BuildRequires:	mvn(org.apache.maven:maven-settings)
BuildRequires:	mvn(org.sonatype.plexus:plexus-build-api)
# 1.2.0-1 provides the coordinate but has no sysjar index.
BuildRequires:	plexus-build-api >= 1.2.0-2
Requires:	plexus-build-api >= 1.2.0-2
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:	plexus-utils >= 3.6.2
Requires:	plexus-utils >= 3.6.2
BuildRequires:	mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:	plexus-interpolation >= 1.30.0
Requires:	plexus-interpolation >= 1.30.0
BuildRequires:	mvn(org.slf4j:slf4j-api)
BuildRequires:	mvn(javax.inject:javax.inject)
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

Obsoletes:	maven-shared-filtering < %{EVRD}
Provides:	maven-shared-filtering = %{EVRD}

%description
Filters Maven project resources and property files. 3.5.1 uses
plexus-interpolation 1.30 and the 0.0.7 build context. Tests are not run.

%prep
%autosetup -n maven-filtering-maven-filtering-%{version}
rm -rf src/test .github
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apache.maven.shared")
add(root, "artifactId", "maven-filtering")
add(root, "version", "%{version}")
add(root, "name", "Apache Maven Filtering")
props = ET.SubElement(root, tag("properties"))
add(props, "maven.compiler.release", "8")
add(props, "project.build.sourceEncoding", "UTF-8")
deps = ET.SubElement(root, tag("dependencies"))
for group, artifact, version, scope in (
    ("org.apache.maven", "maven-core", "3.10.0", "provided"),
    ("org.apache.maven", "maven-model", "3.10.0", "provided"),
    ("org.apache.maven", "maven-settings", "3.10.0", "provided"),
    ("org.sonatype.plexus", "plexus-build-api", "0.0.7", ""),
    ("org.codehaus.plexus", "plexus-utils", "3.6.2", ""),
    ("org.codehaus.plexus", "plexus-interpolation", "1.30.0", ""),
    ("org.slf4j", "slf4j-api", "1.7.36", ""),
    ("javax.inject", "javax.inject", "1", ""),
):
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
    if scope:
        add(dep, "scope", scope)
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY
# Sisu loads @Named classes from this index. The indexer plugin is not packaged.
python - <<'PY'
import re
from pathlib import Path
root = Path("src/main/java")
names = []
for path in sorted(root.rglob("*.java")):
    text = path.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"//.*?$", "", text, flags=re.M)
    match = re.search(r"\b(?:class|interface|enum)\s+([A-Za-z0-9_]+)", text)
    if not match:
        continue
    if "@Named" not in text[:match.start()]:
        continue
    pkg = re.search(r"(?m)^package\s+([A-Za-z0-9_.]+)\s*;", text)
    if not pkg:
        continue
    names.append(pkg.group(1) + "." + match.group(1))
if names:
    dest = Path("src/main/resources/META-INF/sisu")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "javax.inject.Named").write_text("\n".join(names) + "\n", encoding="utf-8")
PY

%files -f .mfiles
%doc README.md
