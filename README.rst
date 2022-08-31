IdentityGenerator
======================================

.. |buildstatus|_
.. |coverage|_
.. |docs|_
.. |packageversion|_

.. docincludebegin

This module generates synthesized full names. First and last names are sampled based on their frequency (i.e., weighted sampling). The source of the names are as follows:

* https://www.ssa.gov/oact/babynames/limits.html (first names)
* https://www.census.gov/topics/population/genealogy/data/2010_surnames.html (last names)


Quick Start (command line)
-----------

.. code-block:: sh

   $ python ./src/IdentityGenerator.py --num_samples 100

This returns synthesized 100 full names. By adding `--output_file_path`, the generated names are stored. The example is as follows:

.. code-block:: sh

   $ python ./src/IdentityGenerator.py --num_samples 100 --output_path ./data/test.csv

The command above generates `test.csv` file under `data` folder. The file contains 100 full names.