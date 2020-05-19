Starting CTT
~~~~~~~~~~~~

(In progress)

The easiest way to start CTT is by invoking the publicly available Docker container:

::

  docker run -t -i --name RadonCTT -p 18080:18080 -v /var/run/docker.sock:/var/run/docker.sock radonconsortium/ctt-server:dev

To check whether the CTT server has started properly, you should be able to access the OpenAPI-based interface via a web browser: http://localhost:18080/RadonCTT/ui/

However, for the remaining step, we will interact with the CTT server via `Curl <https://curl.haxx.se/>`_.

Creating a Project
~~~~~~~~~~~~~~~~~~~~

The first step is to create a CTT project by providing a project name and a Git repository URL. The repository contains TOSCA service templates.

The following Git repository already includes a ready-to-use example: https://github.com/radon-h2020/demo-ctt-sockshop/

To create a project using the example, execute the following:

::

  curl -X POST "http://localhost:18080/RadonCTT/project" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"name\":\"SockShop\",\"repository_url\":\"https://github.com/radon-h2020/demo-ctt-sockshop.git\"}"

The response includes a UUID for the project that is required for the further interaction with the project. For example, the following output includes the UUID *d3cb9d75-73df-422e-9575-76e7a5775f8e* of the project that was just created:

::

  {
    "name": "SockShop",
    "repository_url": "https://github.com/radon-h2020/demo-ctt-sockshop.git",
    "uuid": "d3cb9d75-73df-422e-9575-76e7a5775f8e"
  }

Generating Artifacts
~~~~~~~~~~~~~~~~~~~~

To create test artifacts for the project, the paths to the TOSCA CSAR files that include the system under test (SUT) and the test infrastructure (TI) must be passed along with the previously obtained project UUID to the next command. In the example repository, the CSAR files for the SUT and TI are stored in the *radon-ctt* folder, i.e., *radon-ctt/sut.csar* and *radon-ctt/ti.csar*.

::

  curl -X POST "http://localhost:18080/RadonCTT/testartifact" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"project_uuid\":\"d3cb9d75-73df-422e-9575-76e7a5775f8e\",\"sut_tosca_path\":\"radon-ctt/sut.csar\",\"ti_tosca_path\":\"radon-ctt/ti.csar\"}"

The response includes the UUID of the created test artifacts, i.e., the executable CSAR files of the SUT and the TI. For example, the following output includes the UUID *87a2d052-93ce-43d2-b765-74b0cef9df92* of the artifacts that were just created:

::

  {
    "commit_hash": "4d1135e3d762dc81210d905932711a991b7b4373",
    "project_uuid": "d3cb9d75-73df-422e-9575-76e7a5775f8e",
    "sut_tosca_path": "radon-ctt/sut.csar",
    "ti_tosca_path": "radon-ctt/ti.csar",
    "uuid": "87a2d052-93ce-43d2-b765-74b0cef9df92"
  }

Deploying the SUT and the TI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To deploy the test artifacts (SUT and TI) using the xOpera TOSCA orchestrator, the artifact UUDI needs to be provided to the next command:

::

  curl -X POST "http://localhost:18080/RadonCTT/deployment" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"testartifact_uuid\":\"87a2d052-93ce-43d2-b765-74b0cef9df92\"}"

This step will take a while, depending on the system and type of systems as. You can watch the progress by inspecting the CTT log and watching the Docker processes:

:: 

  watch docker ps

The response includes the UUID of the deployment. For example, the following output includes the UUID *5f435990-8a1a-4741-a040-6db2fe552603* of the deployment that was just created: 

::

  {
    "testartifact_uuid": "87a2d052-93ce-43d2-b765-74b0cef9df92",
    "uuid": "5f435990-8a1a-4741-a040-6db2fe552603"
  }

The deployed SockShop application is now reachable in the web browser via: http://localhost/

The deployed JMeter agent is reachable via *http://localhost:5000/*. However, the REST-based interface is intended to be used by the CTT server and not by end users.

Executing the Test
~~~~~~~~~~~~~~~~~~

To execute the test, the deployment UUID needs to be provided in the next command:

::

  curl -X POST "http://localhost:18080/RadonCTT/execution" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"deployment_uuid\":\"5f435990-8a1a-4741-a040-6db2fe552603\"}"

The test is now executing. You can watch the progress in the CTT server log and by attaching to the JMeter agent log (showing raw result statistics):

:: 

  docker logs -f JMeterAgent

After the test has finished, the response includes the UUID of the text execution. For example, the following output includes the UUID *beead8ea-8e3e-42ec-ad1c-7e2b3e5b4492* of the most recent execution: 

::

  {
    "agent_configuration_uuid": "17321ea2-67c9-40fb-9e84-c761a39680a0",
    "agent_execution_uuid": "91905534-d423-4933-b363-d84a647ac619",
    "uuid": "beead8ea-8e3e-42ec-ad1c-7e2b3e5b4492"
  }


Creating Test Results
~~~~~~~~~~~~~~~~~~~~~~~

To create the test results, the execution UUID needs to be provided in the next command:

::

  curl -X POST "http://localhost:18080/RadonCTT/result" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"execution_uuid\":\"beead8ea-8e3e-42ec-ad1c-7e2b3e5b4492\"}"

After the creation has finished, the response includes the UUID of the test results. For example. the following output  includes the UUID *a2c6bc9f-7c1f-4060-b80b-3c66e3487db9*:

::

  {
    "execution_uuid": "beead8ea-8e3e-42ec-ad1c-7e2b3e5b4492",
    "results_file": "/tmp/RadonCTT/result/a2c6bc9f-7c1f-4060-b80b-3c66e3487db9",
    "uuid": "a2c6bc9f-7c1f-4060-b80b-3c66e3487db9"
  }


Inspecting Test Results
~~~~~~~~~~~~~~~~~~~~~~~

To inspect the test results, the execution UUID needs to be provided in the next command:

::

  curl -X GET "http://localhost:18080/RadonCTT/result/a2c6bc9f-7c1f-4060-b80b-3c66e3487db9/download" -H  "accept: application/json"

The response includes a *Results.zip* files with the test results. The file can be opened in the file manager.

Example: *Results.zip*