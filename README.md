# data-science-viz

## Virtual enviroments

Usage of virtual enviroments to make sure that the project is compatible in every machine.

To create a new virtual enviroment `python -m venv <directory>` In this case it is important to use the naming convention for the directory as .venv or .env. (This folder will be ignore in the .gitignore file).

How to activate the virtual enviroment?

- Windows venv activation:

```
# In cmd.exe
venv\Scripts\activate.bat
# In PowerShell
venv\Scripts\Activate.ps1
```

- Linux and MacOS venv activation:

```
source myvenv/bin/activate
```

For all platforms it is needed just to call `deactivate` and you are out from this env.

Everytime a package is installed, for example: `pip install numpy`, the requirements.txt file should be updated. To catch up the updated version in a new virtual enviroment you can call `pip install -r requirements.txt` and that is, you project is ready to go.

## Software Requirements

- Python 3.12.2
- anaconda Command line client (version 1.12.3)
- pip 24.0

All the required packages will be listed on the `requirements.txt` file.

## Project planning:

A copy of the project planning will be at [Project Notes](./notes/project_plan.md). Otherwise use the link to contribute online at [Hackmd - Planning](https://hackmd.informatik.uni-bremen.de/j6lQBfpTSDOP7SPxjBKXQg).

## Python Scripts - Jupyter

The idea is to showcase cenarios the jupyter notebooks are optimal. But for software development they are not great. For now it is not possible to keep the versions fo the software since it is recoginized as an executable by GIT system.

Convert (all) Jupyter notebooks to python:

```
jupyter nbconvert *.ipynb  --to="python"
```

Convert python scripts to jupyter (the package p2j should be in the requirements list):

```
p2j script.py
```

## Our Project:

The folder structure follow as this:

```
project_wild_fire
├── docs
├── output
├── sample
├── src
└── tests
```

## References:

- [Virtual Env](https://python.land/virtual-environments/virtualenv)
- [Classes Slides](https://nc.uni-bremen.de/index.php/s/MWxosSLCQxKPapZ)
- [Jupyter Uni Bremen](https://jupyter.uni-bremen.de/)
- [Forschung Professor: Klimageographie](https://www.uni-bremen.de/geographie/personen/personen-a-z/prof-dr-ben-marzeion)

## Tasks

| Task Description                                                                         | Assignee | Status      |
| ---------------------------------------------------------------------------------------- | -------- | ----------- |
| Write Exposé                                                                             | @all     | In Progress |
| Extract information from the DWD portal                                                  | -        | Not Started |
| Extract information from the Brandstatistik PDF's                                        | -        | Not Started |
| Filter/Clean/Convert Raw data DWD Portal                                                 | -        | Not Started |
| Filter/Clean/Convert Raw data Brandstatistik                                             | -        | Not Started |
| Creating a unique env to test models with our stable database                            | -        | Not Started |
| Developing basic visualisation functions to help evaluate the model development          | -        | Not Started |
| Deep analysis in the model training - here each pearson could train a model (if nessary) | -        | Not Started |
| Visualisation techniques discussion - Focus on formats, display, intereaction            | -        | Not Started |
| Visualisation design discussion - Focus on colors, text, size                            | -        | Not Started |
| Writting unit tests for each application (arrange - act - assert)                        | -        | Not Started |
| Code refactoring - reduce redudancy                                                      | -        | Not Started |
