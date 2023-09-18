# Title of the project

## Table of contents

- [Title of the project](#title-of-the-project)
  - [Table of contents](#table-of-contents)
- [About](#about)
- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup instructions](#setup-instructions)
- [Usage](#usage)
- [Running tests](#running-tests)
- [Release process](#release-process)

# About

<!-- A few words describing the purpose of the project -->

# Getting started

<!--  These instructions should set up the project so that it is ready for 
development and testing purposes -->

## Prerequisites

<!-- List of things that are necessary to install, e.g.:
- docker
- JDK 17
- Node.js 
-->

## Setup instructions

<!-- A step by step instruction to install the project-->

Describe what the step will be or do
```
echo "An examplary step"
```

And repeat
```
Until finished
```



# Usage

<!-- Add notes about how to run the program, e.g.: -->

Start local MongoDB
```
docker run -d -p 1020:56870 mongo
```

Start core-service
```
./start.sh --port 4334
```

Open API
    
    navigate to http://127.0.0.1:4334/explorer on your browser

# Running tests

<!-- Guide on how to run automated tests for this project -->

Set up python virtual environtment
```
source tests/python-venv
```

Run tests
```
python -m app-run-tests --logs-path logs/%Y-%M-%D__%H-%M.log
```

# Release process

<!-- Describe the release process - how to prepare a product that is 
production-ready -->

<!-- e.g:
# Release process 
- Pull the merge events into a local repository
- Update changelog and bump version
- Create the git tag
- Commit and push changelog

# Versioning scheme
This project uses semantic versioning scheme. 

Depending on the need a particular project, a release candidate may be released.
-->
