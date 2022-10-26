===========
Milton Maps
===========


Analysis of GIS geospatial data sources for Milton, MA

Purpose
-------

This repository contains a reproducible analysis of geospatial datasets pertaining to the town of Milton, MA and
surrounding communities.

Datasets
--------

Retrieve the versioned datasets used to produce the analytical results in this project using `DVC <https://dvc.org/>`_ by running::

    dvc pull

Open space parcels
================

A shapefile of open and recreational space parcles in Massachusetts was obtained
from `the mass.gov website <https://www.mass.gov/info-details/massgis-data-protected-and-recreational-openspace#downloads->`_.
It is provided with the following disclaimer:

    These data are very useful for most statewide and regional planning purposes.
    However, they are not a legal record of ownership, and the user should understand that
    parcel representations are generally not based on property surveys.

Data documentation is currently `provided online <https://www.mass.gov/info-details/massgis-data-protected-and-recreational-openspace>`_
and a `PDF copy <data/docs/MassGIS_Openspace.pdf>`_ of the website as it was accessed when the data was downloaded is saved locally
in case the website is moved or modified.

The shapefile data can be re-downloaded from the mass.gov website by running::

    make refresh-openspace-data

Tax Parcels
===========

Downloaded from `mass.gov property tax parcel <https://www.mass.gov/info-details/massgis-data-property-tax-parcels>`_.
The files are offered with the following disclaimer:

    Assessor’s parcel mapping is a representation of property boundaries, not an authoritative source.
    The authoritative record of property boundaries is recorded at the registries of deeds. A legally
    authoritative map of property boundaries can only be produced by a professional land surveyor.

Data documentation is currently `provided online <https://www.mass.gov/info-details/massgis-data-property-tax-parcels>`_
and a `PDF copy <data/docs/MassGIS_PropertyTaxParcels.pdf>`_ of the website as it was accessed when the data
is saved locally in case the website is moved or modified.

Full data dictionary and other documentation are provided in the `Parcel Standard <https://www.mass.gov/doc/standard-for-digital-parcels-and-related-data-sets-version-3/download>`_.
A `PDF copy <data/docs/Mass_Parcel_Standard_Version3.pdf>`_ of the standard is saved locally in case the website is moved or modified.


Analysis
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
