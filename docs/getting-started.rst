This section exemplifies the usage of CTT with the `SockShop <https://github.com/microservices-demo/microservices-demo>`_ application. The `SockShop <https://github.com/microservices-demo/microservices-demo>`_ is an open-source microservice example implementation using Docker containers and a wide range of configurations for easy deployment (e.g., *docker-compose* and Kubernetes). We `forked the project on GitHub <https://github.com/radon-h2020/demo-ctt-sockshop>`_ and enriched it with artifacts for usage with the CTT tool as a way to showcase the process of using CTT with an existing project.

In general, the steps in CTT (detailed below) are as follows:

1. *Start* the CTT Server. 

2. *Create a project* by providing a name and the URL to the repository that is supposed to be tested.

3. *Create test artifacts* by specifying the paths to the TOSCA artifacts used for the system under test (SUT) and the test infrastructure (TI). This step collects all information necessary for the following deployment and execution steps.

4. The *create deployment* step first deploys the SUT and TI using the opera orchestrator. When both have been deployed successfully, the endpoints of the deployed services are known and can be used to execute the actual tests in the following step.

5. *Create execution* provides the TI with the test configuration including dynamic properties required for successful execution (e.g., IP address of the SUT) and then triggers the start of the test execution.

6. Finally, after the test has finished, the results of the test execution can be obtained using the *results* section of the API.

Starting CTT
~~~~~~~~~~~~

The easiest way to start CTT is by invoking the publicly available Docker container:

::

  docker run -t -i --name RadonCTT -p 18080:18080 -v /var/run/docker.sock:/var/run/docker.sock radonconsortium/radon-ctt:latest

In order to be able to deploy to AWS (e.g., use the ImageResize example), you need to enable this feature and pass your AWS credentials like shown below:

::

  docker run --rm -t -i -e CTT_FAAS_ENABLED="1" -e AWS_ACCESS_KEY_ID="<YOUR_AWS_ACCESS_KEY_ID>" -e AWS_SECRET_ACCESS_KEY="<YOUR_AWS_SECRET_ACCESS_KEY>" --name RadonCTT -p 18080:18080 -v /var/run/docker.sock:/var/run/docker.sock radonconsortium/radon-ctt:latest


To check whether the CTT server has started properly, you should be able to access the OpenAPI-based interface via a web browser: http://localhost:18080/RadonCTT/ui/

However, for the remaining step, we will interact with the CTT server via `Curl <https://curl.haxx.se/>`_.

Creating a Project
~~~~~~~~~~~~~~~~~~~~

The first step is to create a CTT project by providing a project name and a Git repository URL. The repository contains TOSCA service templates.

The following Git repository already includes a ready-to-use example with the Weaveworks SockShop application: https://github.com/radon-h2020/demo-ctt-sockshop/. 

To create a project based on the SockShop example repository, execute the following:

::

  curl -X POST "http://localhost:18080/RadonCTT/project" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"name\":\"SockShop\",\"repository_url\":\"https://github.com/radon-h2020/demo-ctt-sockshop.git\"}"

The response includes a UUID for the project that is required for the further interaction with the project. For example, the following output includes the UUID *d3cb9d75-73df-422e-9575-76e7a5775f8e* of the project that was just created:

::

  {
    "name": "SockShop",
    "repository_url": "https://github.com/radon-h2020/demo-ctt-sockshop.git",
    "uuid": "d3cb9d75-73df-422e-9575-76e7a5775f8e"
  }


Similarly, you can use the ImageResize example repository which uses AWS to deploy a example FaaS application including two S3 buckets and one Lambda function:

::

    curl -X POST "http://localhost:18080/RadonCTT/project" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"name\":\"ImageResize\",\"repository_url\":\"https://github.com/radon-h2020/demo-ctt-imageresize.git\"}"



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

This step will take a while, depending on the system and type of systems. You can watch the progress by inspecting the CTT log and watching the Docker processes:

::

  watch docker ps

The response includes the UUID of the deployment. For example, the following output includes the UUID *5f435990-8a1a-4741-a040-6db2fe552603* of the deployment that was just created:

::

  {
    "testartifact_uuid": "87a2d052-93ce-43d2-b765-74b0cef9df92",
    "uuid": "5f435990-8a1a-4741-a040-6db2fe552603"
  }

The deployed SockShop application is now reachable in the web browser via: http://localhost/

The deployed JMeter agent is reachable via *http://localhost:5000/*. However, the REST-based interface is intended to be used by the CTT server and not by end-users.

Executing the Test
~~~~~~~~~~~~~~~~~~

To execute the test, the deployment UUID needs to be provided in the next command:

::

  curl -X POST "http://localhost:18080/RadonCTT/execution" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"deployment_uuid\":\"5f435990-8a1a-4741-a040-6db2fe552603\"}"

The test is now executing. You can watch the progress in the CTT server log and by attaching to the JMeter agent log (showing raw result statistics):

:: 

  docker logs -f CTTAgent

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

  curl -X GET "http://localhost:18080/RadonCTT/result/a2c6bc9f-7c1f-4060-b80b-3c66e3487db9/download" -H  "accept: application/json" --output /tmp/Results.zip

The response includes a *Results.zip* file with the test results which is stored in `/tmp/Results.zip` after executing the command above.

For your convenience, feel free to download a sample `Results.zip <_static/Results.zip>`_. Among other contents, the file includes an HTML-based report (in the *dashboard/* directory).
