# pygorpmrustinfo

pygorpmrustinfo is a unified Python package that exposes the former rpmdb, rust audit, and Go build-info helpers through a single Go-backed extension.

## Why this package exists

The older split packages each relied on their own Go runtime and native extension. That approach is fragile in Python environments because Go's `c-shared` mode can be unstable when multiple Go runtimes are loaded into the same process. This is the problem described in [Go issue #65050](https://go.dev/issue/65050): loading multiple `c-shared` Go libraries in one process can lead to panics, crashes, or other runtime failures.

This consolidation is meant to reduce that risk by keeping a single Go runtime in play, while also reducing memory usage compared with loading several separate native extensions.

## Deprecation notice for the old scripts

The legacy entry points and package names are being deprecated. The replacement package is pygorpmrustinfo, and the compatibility scripts remain available only for transition:

- `get_go_info`
- `get_rpm_info`
- `get_rust_audit`
- the older standalone package names for the previous split implementations

These legacy scripts remain available for compatibility, but new work should target `pygorpmrustinfo` instead.

## Installation

```bash
pip install pygorpmrustinfo
```

## Usage

The package provides the same high-level functionality as the older helpers, but through one unified interface. If you are coming from the old packages, the main change is that you install and import one package instead of three separate ones.

### CLI

```bash
get_go_info /path/to/go.mod
get_rpm_info /path/to/Packages
get_rust_audit /path/to/rust-binary
```

These scripts are preserved for compatibility, but the recommended path is to depend on `pygorpmrustinfo` directly.

### Python API

```python
import json
import pygorpmrustinfo

# Go build metadata
res = pygorpmrustinfo.get_go_build_info("/path/to/go.mod")
print(json.dumps(res, indent=4))

# RPM database metadata
res = pygorpmrustinfo.get_rpm_db_info("/path/to/Packages")
print(json.dumps(res, indent=4))

# Rust audit metadata
res = pygorpmrustinfo.get_rust_audit("/path/to/rust-binary")
print(json.dumps(res, indent=4))
```

### Example: Go build info

```python
import pygorpmrustinfo

info = pygorpmrustinfo.get_go_build_info("/path/to/go.mod")
print(info["GoVersion"])
print(info["Path"])
```

Example result:

```python
{
    "GoVersion": "go1.18.4",
    "Path": "github.com/example/project",
    "Main": {
        "Path": "github.com/example/project",
        "Version": "(devel)",
        "Sum": "",
        "Replace": null
    },
    "Deps": []
}
```

### Example: RPM database info

```python
import pygorpmrustinfo

packages = pygorpmrustinfo.get_rpm_db_info("/path/to/Packages")
for package in packages:
    print(package.get("Name"), package.get("Version"))
```

Example result:

```python
[
    {
        "Name": "bash",
        "Version": "5.1",
        "Release": "1.el9"
    }
]
```

### Example: Rust audit info

```python
import pygorpmrustinfo

packages = pygorpmrustinfo.get_rust_audit("/path/to/rust-binary")
for package in packages.get("packages", []):
    print(package.get("name"), package.get("version"))
```

Example result:

```python
{
    "packages": [
        {
            "name": "serde",
            "version": "1.0.197",
            "kind": "build"
        }
    ]
}
```

The functions always return a dictionary. On error you may see a structure like:

```python
{
    "error": "path error:/path/to/missing/file"
}
```

## Migration from the old packages

If you previously used one of the older packages, the migration is straightforward:

- replace `pyrpmdb` with `pygorpmrustinfo` and call `get_rpm_db_info(...)`
- replace `pyrustaudit` with `pygorpmrustinfo` and call `get_rust_audit(...)`
- replace `pygobuildinfo` with `pygorpmrustinfo` and call `get_go_build_info(...)`, `get_go_mod(...)`, or `get_go_sum(...)`

For dependency declarations, update requirements, `pyproject.toml`, `setup.cfg`, or `setup.py` to depend on `pygorpmrustinfo` instead of the old package names.

## Notes

- The consolidation is primarily a stability and resource-usage improvement.
- It is also a practical mitigation for the risks documented in [Go issue #65050](https://go.dev/issue/65050).
- If you are maintaining older automation, consider switching to the unified package now so you are not tied to the deprecated script-based workflow.
