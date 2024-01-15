![image](./assets/img.png)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)  ![Python](https://img.shields.io/badge/python-3.10.x-green.svg) ![Repo Size](https://img.shields.io/github/repo-size/Sulstice/global-chem)  [![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/) [![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)


# global-biodiversity-score


## About

### Context

CDC Biodiversité is a subsidiary of the Caisse des Dépôts et Consignation, the largest French financial institution. It is specialized in providing biodiversity-positive solutions to businesses such as ecological offsets and biodiversity footprinting.

The Global Biodiversity Score® (GBS®) is a tool developed by CDC Biodiversité to measure corporate and investments’ biodiversity impacts.
The tool is used by an ecosystem of companies, financial institutions, consultants and
academics.

More information can be found at :
* [2022 - N18-TRAVAUX-DU-CLUB-B4B-G
BS-UK-MD-WEB.pdf](https://www.mission-economie-biodiversite.com/wp-content/uploads/2022/01/N18-TRAVAUX-DU-CLUB-B4B-GBS-UK-MD-WEB.pdf)
* [2020 - N15-TRAVAUX-DU-CLUB-B4B-GBS-UK-MD-WEB.pdf](http://www.mission-economie-biodiversite.com/wp-content/uploads/2020/09/N15-TRAVAUX-DU-CLUB-B4B-GBS-UK-MD-WEB.pdf)


### Goals

The GBS can assess biodiversity of various commodities such as agricultural crops :
* The biodiversity impact results are expressed in MSA.km² (mean species abundance times km²)
and could be detailed by pressure on such as land use or climate change.

* The goal of this exercise is to compute the total static biodiversity loss due to land use caused
by wheat in every country (in MSA.km²) in 2019.


## Installation

### Clone the repository

Please clone the repository using the following command :

* for https :
```bash
https://github.com/AlexandreGazagnes/Global-Biodiversity-Score.git
```
* for ssh :
```bash
git clone git@github.com:AlexandreGazagnes/Global-Biodiversity-Score.git
```

### Install the dependencies

The project uses [Poetry](https://python-poetry.org/) to manage its dependencies. Please install it using the following command :

```bash
pip install poetry
```

Then, please install the dependencies using the following command :

```bash
poetry install
```

Alternatively, you can install the dependencies using the following command :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r ./utils/requirements-dev.txt
```

## Usage

The project is divided into 3 parts :
* *core* : contains the core functions of the project
* *front* : contains the front-end of the project
* *api* : api of the project


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License

[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)