.. highlight:: shell

=========================
Reproduce the Analyses
=========================

Download Souce Code
-------------------

Download the source code for Milton Maps from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/ahasha/milton_maps

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/ahasha/milton_maps/tarball/master

Install Software Dependencies
-----------------------------

The python package environment for this analysis is managed using
`conda <https://conda.io/projects/conda/en/latest/index.html>`_.
If not already installed on your system, I recommend installing the Anaconda python distribution
as detailed `here <https://conda.io/projects/conda/en/latest/user-guide/install/index.html>`_.  For a
quicker startup requiring less disk space, you may prefer to install the Miniconda distribution.

I strongly recommend installing `mamba`, which is a C++ port of the `conda` package manager.
It provides significantly faster dependency resolution, which can cause fresh environment
set ups to be very time consuming with conda.  Mamba should be installed in the *conda base
environment* only:

.. code-block:: console

    $ conda install -c conda-forge mamba

With conda/mamba installed, the analytical environment for this project is created
and activated with the following terminal commands:

.. code-block:: console

    $ mamba env create -f environment.yml
    $ conda activate milton-maps

This installs all package dependencies of the project and also the project's shared
module `milton_maps` in "editable" mode, so that local changes to the project files will be loaded
when the `milton_maps` is imported.

When you are done working with the project, deactivate the conda environment with

.. code-block:: console

    $ conda deactivate

Get Data Sources
----------------

This project uses `DVC <https://dvc.org/>`_ to store versioned data compatible with the
the current state of the code in the git repository.  The data repository is hosted in
a public Google Drive which you should be able to read from but not write to.

The following command will retried both the raw and processed data sets necessary to
run the analysis notebooks

.. code-block:: console

    $ dvc pull

This command will open a google authentication workflow in your browser, and you will
need to grant permissions for DVC to access data using your google account. If
you have issues with access, reach out to
`ahasha@sustainablemilton.org <mailto:ahasha@sustainablemilton.org>`_ for assistance.

Running Analysis Notebooks
--------------------------

After running `dvc pull`, you should be able to directly execute the analyses
notebooks in `notebooks` by running

.. code-block:: console

    $ jupyter notebook &

and opening the desired notebook from the UI.  The notebooks use cleaned and
transformed data from the `data/processed` directory that I have generated using a
`dvc` pipeline and stored in the data repository, so these pipelines do not need to
be re-run in order to execute the notebooks.

Reproducing or Modifying Data Cleaning Pipeline
-------------------------------------------------

If you want to reproduce or modify the cleaned and transformed datasets used by
the notebooks, you should first delete the processed data by running

.. code-block:: console

    $ make clean-processed-data

Then execute the `dvc` data processing pipeline by running

.. code-block:: console

    $ dvc repro -f

This executes a DAG of data processing stages defined in `dvc.yaml`, intelligently
running only those stages where an output is missing or an input has been modified.
The `-f` or "force" flag ensures that the processing stages are recalculated and not
pulled from the dvc cache.  Then run

.. code-block:: console

    $ dvc status

`dvc` computes a checksum of each of the output files to determine if they have been
modified.  If the results have been reproduced exactly in your local environment, you
should see the message

.. code-block:: console

    Data and pipelines are up to date.

.. _Github repo: https://github.com/ahasha/milton_maps
.. _tarball: https://github.com/ahasha/milton_maps/tarball/master
