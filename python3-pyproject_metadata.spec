#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_with	tests	# unit tests

%define		module	pyproject_metadata
Summary:	PEP 621 metadata parsing
Summary(pl.UTF-8):	Analiza metadanych PEP 621
Name:		python3-%{module}
Version:	0.9.0
Release:	3
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.debian.net/pyproject_metadata/%{module}-%{version}.tar.gz
# Source0-md5:	d947b3c632f4aee9cf23bb5950ac02f9
URL:		https://pypi.org/project/pyproject-metadata/
BuildRequires:	python3-build
BuildRequires:	python3-flit_core
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.7
%if %{with tests}
BuildRequires:	python3-packaging >= 19.0
BuildRequires:	python3-pytest >= 6.2.4
%if "%{py3_ver}" == "3.7"
BuildRequires:	python3-typing_extensions
%endif
%if "%{_ver_lt %{py3_ver} 3.11}" == "1"
BuildRequires:	python3-exceptiongroup
BuildRequires:	python3-tomli >= 1.0.0
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo >= 2023.9.10
BuildRequires:	python3-myst_parser
BuildRequires:	python3-sphinx_autodoc_typehints >= 1.10.0
BuildRequires:	sphinx-pdg-3 >= 7.0
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project does not implement the parsing of pyproject.toml
containing PEP 621 metadata.

Instead, given a Python data structure representing PEP 621 metadata
(already parsed), it will validate this input and generate a PEP
643-compliant metadata file (e.g. PKG-INFO).

%description -l pl.UTF-8
Ten projekt nie implementuje analizy plików pyproject.toml,
zawierających metadane PEP 621, ale po przekazaniu (już
przeanalizowanej) struktury danych metadanych PEP 621, sprawdza jej
poprawność i generuje plik metadanych zgodny z PEP 643 (np. PKG-INFO).

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/_build/html
rm -rf docs/_build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
