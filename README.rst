===========
Milton Maps
===========


Analysis of GIS geospatial data sources for Milton, MA in transparent and reproducible Python.
Check out the source code on `GitHub <https://github.com/ahasha/milton_maps>`_.

Purpose
-------

This repository contains an example analysis combining several publicly available geospatial datasets
pertaining to the town of Milton, MA and surrounding communities.  I had two goals in putting this
together:

1. Build awareness in the Milton community of civic organizations of available sources of map data and
   how they might be used to answer questions of local interest.  Provide a starting foundation for
   anyone in town who may want to work with this data in Python.
2. Provide an example of a Python project structure that is portable, transparent and reproducibile using
   modern tools for data versioning, document generation, and python environment management.
   Namely, `dvc <dvc.org>`_ for data version control, `sphinx <https://www.sphinx-doc.org/en/master/>`_
   for document generation, and `conda <https://conda.io/>`_ for environment management.



Datasets
--------

The analyses in this project use the following public GIS data sets

Open space parcels
==================

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

Mass DOT Crash Data
===================

A crash data report for Milton, MA was requested from the Department of Transportation (MassDOT)
`IMPACT Portal <https://apps.impact.dot.state.ma.us/cdp/home>`_ using the
`Data Extraction <https://apps.impact.dot.state.ma.us/cdp/extract>`_ tool.  Crash data for the
years 2016-2022 in Milton, MA were requested via the web page, and a personalized download link was
emailed shortly thereafter.  Data documentation provided with the download link is saved in
`data/docs/MassDOT_crashdata_support_information.pdf`.

The data is provided with the following disclaimer.

    MassDOT makes no representation as to the accuracy, adequacy, reliability, availability or
    completeness of the crash records or the data collected from them and is not responsible for
    any errors or omissions in such records or data. Under no circumstance will MassDOT have any
    liability for any loss or damage incurred by any party as a result of the use of the crash
    records or the data collected from them. Furthermore, the data contained in the web-based crash
    report tool are not an official record of what transpired in a particular crash or for a particular
    crash type. If a user is interested in an official copy of a crash report, contact the
    Registry (http://www.mass.gov/rmv/).

    The City of Boston Police Department may be contacted directly for official copies of crash
    reports and for crash data pertaining to the City of Boston. In addition, any crash records
    or data provided for the years 2020 and later are subject to change at any time and are not
    to be considered up-to-date or complete. As such, open years’ of crash data are for informational
    purposes only and should not be used for analysis.

    The data posted on this website, including crash records and other reports, are collected for
    the purpose of identifying, evaluating or planning the safety enhancement of potential crash
    sites, hazardous roadway conditions or railway-highway crossings. Under federal law, this
    information is not subject to discovery and cannot be admitted into evidence in any federal or
    state court proceeding or considered for other purposes in any action for damages that involves the
    sites mentioned in these records (see 23 USC, Section 409).


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
