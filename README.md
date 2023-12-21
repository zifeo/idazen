# idazen

[![PyPI version](https://badge.fury.io/py/idazen.svg)](https://badge.fury.io/py/idazen)

Take control over your Ikea IDÅSEN standing desk without hassle and stay ZEN 🙌.

## Getting started

```
# pypi
pip install idazen

# pipx
pipx install idazen

# master
pip install --upgrade git+https://github.com/zifeo/idazen.git
```

### MacOS

You may need to add your Terminal (or other) app to the Bluetooth allowlist
`System Preferences > Security & Privacy > Bluetooth`.

## Usage

```
> idazen scan
Scanning 10s...
Found: Desk 7764 (3C9D3306-3B80-4D68-8670-AC9451083BC5)
Use "idazen save 3C9D3306-3B80-4D68-8670-AC9451083BC5" or "idazen scan --save"
```

```
> idazen move 78
Height set to 78.22
```
