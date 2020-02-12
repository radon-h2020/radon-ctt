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
