# RADON Continuous Testing Tool (CTT)

## 

| Items | Contents | 
| --- | --- |
| **Description** | The Continuous Testing Tool supports RADON's continuous testing workflow. This repository contains the CTT server.  |
| **Licence**| Apache License, Version 2.0: https://opensource.org/licenses/Apache-2.0 |
| **Maintainers**| <ul><li>Thomas F. Düllmann ([@duelle](https://github.com/duelle)) </li><li>Andre van Hoorn ([@avanhoorn](https://github.com/avanhoorn)) </li></ul> |

## System Requirements

This README is currently tailored to Unix-like systems (Linux, MacOS). 

For CTT users, the following software must be installed: 

1. Python3
1. Python Virtual Environment (`virtualenv`)

For CTT developers, the following additional software must be installed: 
1. Docker 
1. Recommended: A Python IDE such as [PyCharm](https://www.jetbrains.com/pycharm/) 

## Starting the CTT Server

Execute the following steps to start start and access the CTT server:

1. Clone this repository (if not done, yet)
1. Start the CTT server by executing  `./radon_ctt_start.sh`
1. Access the CTT server's (Swagger-based) UI by visiting the following URL in the Web browser: `http://localhost:8080/RadonCTT/ui/`

## Developing/Extending the CTT Server

### Editing the CTT Server Code

1. When using an IDE: import the CTT Server repository into your IDE

### Changing the CTT REST API and Regenerating the CTT Server Stub

The CTT Server's REST API is defined in the file `radonctt-openapi.yaml`.   

1. The following options exist to edit the API definition file `radonctt-openapi.yaml`: 
   1. Use a standard text editor (or your Python IDE)    
   1. Use the [Swagger editor](https://editor.swagger.io/): 
      1. File -> Import file -> `radonctt-openapi.yaml`
      1. Edit the file in the editor
      1. File -> Save as YAML -> `radonctt-openapi.yaml`
1. For regenerating the CTT server stub, execute `generate_python_flask_stubs.sh` 

## Examples

The following sections describe the use case examples we use as first application scenarios.

In general, the steps in RadonCTT are as follows:
1. *Create a project* by providing a name and the URL to the repository that is supposed to be tested.
1. *Create test artifacts* by specifying the paths to the TOSCA artifacts used for the system under test (SUT) and the test infrastructure (TI). This step collects all information necessary for the following deployment and execution steps.
1. The *create deployment* step first deploys the SUT and TI using the opera orchestrator. When both have been deployed  successfully, the endpoints of the deployed services are known and can be used to execute the actual tests in the following step.
1. *Create execution* provides the TI with the test configuration including dynamic properties required for a successful execution (e.g., IP address of the SUT) and then triggers the start of the test execution.
1. Finally, after the test has finished, the results of the test execution can be obtained using the *results* section of the API.

### Weaveworks SockShop

The [SockShop](https://github.com/microservices-demo/microservices-demo) is an open-source microservice example implementation using docker containers and a wide range of configurations for easy deployment (e.g., `docker-compose` and Kubernetes). We [forked the project on GitHub](https://github.com/radon-h2020/demo-ctt-sockshop) and enriched it with artifacts for usage with the RadonCTT tool as a way to showcase the process of using RadonCTT with an existing project.


