.. CTT documentation master file, created by
   sphinx-quickstart on Fri May 15 15:31:23 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Continuous Testing Tool
===============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Business Purpose
----------------

The *Continuous Testing Tool* (short: *CTT*) provides functionality for defining, generating, executing, and refining continuous tests of application functions, data pipelines, and microservices, as well as for reporting test results. CTT is a standalone tool that extends the `OASIS Topology and Orchestration Specification for Cloud Applications (TOSCA) <http://www.oasis-open.org/committees/tosca>`_ ecosystem and the TOSCA-based `RADON <https://radon-h2020.eu/>`_ framework. While targeting to provide a general framework for continuous quality testing, a particular focus of CTT is on testing workload-related quality attributes such as performance,  elasticity, and resource/cost efficiency. 

Technical Details
-----------------

A user defines tests by adding them to a TOSCA service template for the application under test. We have extended the set of TOSCA node types, relationship types, and policy types for expressing different types of tests and including suitable test drivers. For instance, CTT allows the definition of a load test to be executed using a configured load driver such as `JMeter <https://jmeter.apache.org/>`_. After being deployed by a TOSCA orchestrator such as `xOpera <https://github.com/xlab-si/xopera-opera>`_, the tests are executed and the test results are made available to the user. 

Via its REST-based interface, users can execute the continuous testing on-demand or include it as a part of the CI/CD process. CTT is designed as an extensible framework that allows the definition of new test types, metrics, and tools. CTT is publicly available under the `Apache License 2.0 <http://www.apache.org/licenses/>`_ open-source license. CTT will integrate and extend parts of the `ContinuITy <https://continuity-project.github.io/>`_ approach and tools for performance testing in continuous software engineering.

The following figure shows the workflow of the CTT tool. 

.. image:: imgs/ctt-workflow-1600x532.png

The following video provides a 5-minute demo.

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/35VN2edyvsc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Starting CTT
~~~~~~~~~~~~

The easiest way to start CTT is by invoking the publicly available Docker container: 

::

  docker run ...

Creating a Project
~~~~~~~~~~~~~~~~~~~~

Generating Artifacts
~~~~~~~~~~~~~~~~~~~~

Deploying the SUT and the TI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Executing the Test
~~~~~~~~~~~~~~~~~~

Inspecting Test Results
~~~~~~~~~~~~~~~~~~~~~~~

Additional Information
----------------------

Development and Downloads
~~~~~~~~~~~~~~~~~~~~~~~~~

- Project dashboard: https://github.com/orgs/radon-h2020/projects/2

- Source code repositories

  - CTT server: https://github.com/radon-h2020/radon-ctt
  - CTT agent: https://github.com/radon-h2020/radon-ctt-agent

- Demos

  - SockShop: https://github.com/radon-h2020/demo-ctt-sockshop 


References
~~~~~~~~~~

- Alim Ul Gias, André van Hoorn, Lulai Zhu, Giuliano Casale, Thomas F. Düllmann, Michael Wurster: Performance Engineering for Microservices and Serverless Applications: The RADON Approach. ICPE Companion 2020: 46-49 https://doi.org/10.1145/3375555.3383120

Contact
-------

- `Thomas F. Düllmann <https://www.iste.uni-stuttgart.de/de/institut/team/Duellmann/>`_ and `Andre van Hoorn <https://www.iste.uni-stuttgart.de/institute/team/van-Hoorn/>`_, Institute of Software Technology, University of Stuttgart, Germany

Acknowledgments
---------------

This work is being supported by the European Union’s Horizon 2020research and innovation programme (grant no. 825040, RADON).
