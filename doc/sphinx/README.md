# Documentation

## Markdown

Just browse the files.



## HTML (sphinx)

Install the doc generator:
```bash
pip install sphinx-rtd-theme
```

Load the Python modules and docstrings from this directory (doc/sphinx):
```bash
sphinx-apidoc -o . ../../src/acutils
```

Generate the HTML files:
```bash
make html
```