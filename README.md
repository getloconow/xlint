# PR function linter
lints currently modified funtion for style guidelines and types.


### Jargons
PR - Pull request

#  Coding style
I decided to follow pep8 style since it is the most popular one.

# Purpose
this tool built to be used in an automated environment to score PR and enforce coding style on the code which is going to get merged to master branch.


## Enforcements

Docstring - Brief description of the function or class
Typehints - Enforce type hints ( for readability )


# Libraries and Tools

Python libraries
 - flake8
 - flake8-mypy
 - mypy-lang
 - pylint (optional)
 - pylint-django (optional)

# preferences

It is better to use Visual Studio code for development and all the linting purpose, since all the tools mentioned above is integrated into it.  
Here's the VSCODE config.

```json
{
    "python.linting.mypyArgs": [
        "--ignore-missing-imports",
        "--follow-imports=silent",
        "--check-untyped-defs",
        "--disallow-untyped-defs",
        "--quick-and-dirty"
    ],
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.autopep8Args": [
        "--ignore=E201",
    ],
    "python.linting.flake8Args": [
        "--ignore=E201",
        "--max-line-length=120"
    ],
    "editor.formatOnSave": true,
    "editor.rulers": [
        80,
        120
    ]
}
```

Django typing mypy-django right [here](https://github.com/machinalis/mypy-django). close this repo, add it to mypypath.


# Python guidelines ( necessary )

 - Necessary type hints (enforced)
 - Exceptions, list all exption with signature. ( extended systax sugar, xtyping.throws decorator)
 - The formatting job is automated by the editor. ( else follow pep8 guidlines )
The editor gives you all the hints to format your code.