### Project Organization

```
├── Makefile                   <- Makefile with project operations like `make test` or `make docs`
├── README.md                  <- The top-level README for developers using this project.
├── data
│   ├── raw                    <- The initial raw data extract from the data warehouse.
│   ├── interim                <- Intermediate data that has been transformed but is not used directly for modeling or evaluation.
│   ├── processed              <- The final, canonical data sets for modeling and evaluation.
│   └── external               <- Data from third party sources.
│
├── docs                       <- Documentation templates guiding you through documentation expectations; Structured
│   │                             as a sphinx project to automate generation of formatted documents; see sphinx-doc.org for details
│   ├── figures                <- Generated graphics and figures to be used in reporting
│   └── model_documentation    <- Markdown templates for model documentation and model risk management.
│   └── _build                 <- Generated documentation as HTML, PDF, LaTeX, etc.  Do not edit this directory manually.
│
├── models                     <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks                  <- Jupyter notebooks. Naming convention is a number (for ordering),
│                                 the creator's initials, and a short `-` delimited description, e.g.
│                                 `1.0-jqp-initial-data-exploration.ipynb`.
├── references                 <- Data dictionaries, manuals, important papers, etc
│
├── pyproject.toml             <- Project configuration file; see [`setuptools documentation`](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)
│
├── poetry.lock                <- The requirements file for reproducing the analysis environment, e.g.
│                                 generated with `poetry install`; see https://python-poetry.org/docs/
│
├── .pre-commit-config.yaml    <- Default configuration for pre-commit hooks enforcing style and formatting standards
│                                 and use of a linter (`isort`, `brunette`, and `flake8`)
│
├── setup.cfg                  <- Project packaging and style configuration
│
├── setup.py                   <- Project installation script; makes project pip installable (pip install -e .) so 
│                                 project module can be imported
│
├── .dvc                       <- Data versioning cache and configuration using dvc; see https://dvc.org
│   └── config                 <- YAML formatted configuration file for dvc project; defines default remote data storage cache location;
│
├── tests                      <- Automated test scripts; 
│   └── data                   <- tests for data download and/or generation scripts
│   │   └── test_make_dataset.py
│   │
│   └── features               <- tests for feature generation scripts 
│   │   └── test_build_features.py
│   │
│   ├── models                 <- tests for model training and prediction scripts
│   │   │                         
│   │   ├── test_predict_model.py
│   │   └── test_train_model.py
│   │
│   └── visualization           <- Scripts to create exploratory and results oriented visualizations
│       └── test_visualize.py    
│
├── milton_maps                <- Source code for use in this project.
│   │
│   ├── __init__.py                               <- Makes milton_maps a Python module
│   │
│   ├── data                                      <- Scripts to download or generate data
│   │   ├── make_dataset.py                       <- Utility CLI script to extract data from database tables to local parquet files.

│   │
│   ├── features                                  <- Scripts to turn raw data into features for modeling
│   │   └── build_features.py
│   │
│   ├── models                                    <- Scripts to train models and then use trained models to make
│   │   │                                            predictions. (write outputs to `PROJECT_ROOT/models`
│   │   ├── predict_model.py
│   │   └── train_model.py
│   │
│   └── visualization                             <- Scripts to create exploratory and results oriented visualizations;
│       └── visualize.py                             (write outputs to `PROJECT_ROOT/reports/figures`

```