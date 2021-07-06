# RADON Continuous Testing Tool (CTT)

![build (master)](https://img.shields.io/jenkins/build?jobUrl=http%3A%2F%2F217.172.12.165%3A8080%2Fjob%2FCTT%2Fjob%2Fradon-ctt%2Fjob%2Fmaster%2F&style=plastic)
![tests (master)](https://img.shields.io/jenkins/tests?compact_message&jobUrl=http%3A%2F%2F217.172.12.165%3A8080%2Fjob%2FCTT%2Fjob%2Fradon-ctt%2Fjob%2Fmaster%2F&style=plastic)
![coverage (master)](https://img.shields.io/jenkins/coverage/cobertura?jobUrl=http%3A%2F%2F217.172.12.165%3A8080%2Fjob%2FCTT%2Fjob%2Fradon-ctt%2Fjob%2Fmaster%2F&style=plastic)

| Items                    | Contents                                                     |
| ------------------------ | ------------------------------------------------------------ |
| **Short Description**    | The Continuous Testing Tool (CTT) provides the functionality for defining, generating, executing, and refining continuous tests of application functions, data pipelines and microservices, as well as for reporting test results. While targeting to provide a general framework for continuous quality testing in RADON, a particular focus of CTT is on testing workload-related quality attributes such as performance, elasticity, and resource/cost efficiency. |
| **Documentation**        | <ul><li>*D3.4 – Continuous Testing Tool I*</li></li>*D3.5 – Continuous Testing Tool II*</li></ul> available at https://radon-h2020.eu/public-deliverables/ |
| **Stand-Alone Tutorial** | https://continuous-testing-tool.readthedocs.io/              |
| **Video**                | https://youtu.be/35VN2edyvsc                                 |
| **Source code**          | <ul><li>https://github.com/radon-h2020/radon-ctt (CTT Server)</li><li>https://github.com/radon-h2020/radon-ctt-agent (CTT Agent)</li><li>https://github.com/radon-h2020/radon-ctt-agent-plugins (CTT Agent Plugins)</li><li>https://github.com/radon-h2020/radon-particles (Includes CTT-related types)</li><li>https://github.com/radon-h2020/demo-ctt-sockshop (CTT SockShop Demo)</li><li>https://github.com/radon-h2020/demo-ctt-imageresize (CTT Thumbnail Demo)</li></ul> |
| **Licence**              | [Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0) |
| **Contact**              | <ul><li>Thomas F. Düllmann ([@duelle](https://github.com/duelle)) </li><li>Andre van Hoorn ([@avanhoorn](https://github.com/avanhoorn)) </li></ul> |



## System Requirements

This README is currently tailored to Unix-like systems (Linux, MacOS). 

For CTT users, there are two modes of operation: 

- Docker-based execution (recommended). Therefore, Docker needs to be installed (`sudo apt-get install docker.io docker-compose`).
- Native execution. Therefore, Python3  and the Python Virtual Environment (`virtualenv`) need to be installed (`sudo apt-get install python3 python3-virtualenv`)

For CTT developers, the following additional software must be installed: 
1. Docker 
1. Recommended: A Python IDE such as [PyCharm](https://www.jetbrains.com/pycharm/) 

## Using the CTT Server

In general, the steps in RadonCTT are as follows:

1. Start the CTT Server.
1. *Create a project* by providing a name and the URL to the repository that is supposed to be tested.
1. *Create test artifacts* by specifying the paths to the TOSCA artifacts used for the system under test (SUT) and the test infrastructure (TI). This step collects all information necessary for the following deployment and execution steps.
1. The *create deployment* step first deploys the SUT and TI using the opera orchestrator. When both have been deployed  successfully, the endpoints of the deployed services are known and can be used to execute the actual tests in the following step.
1. *Create execution* provides the TI with the test configuration including dynamic properties required for a successful execution (e.g., IP address of the SUT) and then triggers the start of the test execution.
1. Finally, after the test has finished, the results of the test execution can be obtained using the *results* section of the API.

### Docker-based Execution (Recommended)

For the Docker-based execution using the latest Docker containers, please follow the steps provided on https://continuous-testing-tool.readthedocs.io/.

### Native execution

Execute the following steps to start start and access the CTT server:

1. Clone this repository (if not done, yet)
1. Start the CTT server by executing  `./radon_ctt_start.sh`
1. Access the CTT server's (Swagger-based) UI by visiting the following URL in the Web browser: `http://localhost:8080/RadonCTT/ui/`
1. Follow the next steps according to  https://continuous-testing-tool.readthedocs.io/.

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


