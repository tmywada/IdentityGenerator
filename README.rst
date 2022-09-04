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

Parameters
-----------

.. code-block:: sh

   {
       "female_ratio": 0.5,     
       "decades_start": 1940,        
       "decades_end": 2000,
       "last_names_range_start": 1,  
       "last_names_range_end": 400,
       "first_names_range_start": 1,
       "first_names_range_end": 400,    
       "random_seed": 4649,    
       "weighted_sampling": true
   }

* ``female_ratio``: number of female name / total number of names (female + male). Default value is 0.5, and male and female names are equally sampled.
* ``decades_start`` and `decades_end` define considered decades.
* ``last_names_range_start`` and ``last_names_range_end`` define ranking range. Top 400 names are selected with ``last_names_range_start`` and ``last_names_range_end`` of 1 and 400, respectively.
* ``first_names_range_start`` and ``first_names_range_end`` define ranking range.
* ``random_seed`` is used for random sampling.
* ``weighted_sampling`` defines whether sampling is weighted. If this is set to ``false``, system picks names uniformly.

Note that number of last names is 1000. If set value (i.e., ``last_names_range_end`` is greater than 1000), set value is overwritten to 1000.





