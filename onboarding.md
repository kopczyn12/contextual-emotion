# Onboarding document

## Table of contents

- [Onboarding document](#onboarding-document)
  - [Table of contents](#table-of-contents)
- [General description](#general-description)
- [Structure of the project repository](#structure-of-the-project-repository)
- [First steps - software setup](#first-steps---software-setup)
  - [Cloning git repositories](#cloning-git-repositories)
  - [Discord](#discord)
  - [Trello](#trello)
- [Workflow](#workflow)
- [Examples](#examples)
- [Main documentation and results](#main-documentation-and-results)
- [How to run app](#how-to-run-app)

# General description

The aim of the task is to develop a website that will display a variety of images and simultaneously analyse the user's emotions. Specifically, based on a webcam image (placed minimally on the monitor, halfway up the screen) and the displayed image on the computer/laptop monitor, the user's emotion should be detected in less than 400 ms, the object in the image that the user is looking at (eye movement) should be found and recognised, and this aspect should be verified in subsequent trials. Approximately 40 images should be displayed on the page, from which 23 objects that evoke 5 basic emotions in the user should be determined.

Assumptions and milestones of project are described in the document [plan-of-action.md](https://git.pg.edu.pl/p1305920/contextual-emotion/-/blob/master/general-docs/plan-of-action.md)

# Structure of the project repository

The repository consists of 6 folders **(model, biosignals, segmentation, app, eye-tracking, general-docs, examination)**. 
Each of these folders relates to a specific part of the project and to the general project documentation, which also includes the project assumptions and timeline.
In each folder there is a docs folder where the documentation for the respective part of the project is located and where the code will be.
In the final part of the project the different parts will be integrated in order to create a fully working application.

# First steps - software setup

If you may have any questions, do not hesitate to ask anyone in our team or post
them on the `help` channel on discord.

These items is expected to be a checklist, make sure you have access to
everything.

## Cloning git repositories

- clone the main repository 
  - using ssh: `git clone git@git.pg.edu.pl:p1305920/contextual-emotion.git`
  - using https: `git clone https://git.pg.edu.pl/p1305920/contextual-emotion.git`
`

## Discord

- the main way of communication
- you should've already received access to our channel

## Trello

Here the tasks will be assigned - you should already have access, if not please contact Michal Kopczynski

## Techstack
- Python
- JavaScript
- MERN
- MongoDB
- Jupyter Lab

## Workflow
### Commit messages

- describe what the commit is about, be short and succint, but don't be overly
  specific 
- it's best to separate a commit into a few smaller ones if it encapsules
  multiple files and directories
- include a directory and file name in the message - it makes reading commit
  history easier 
- use simple verbs, like `add, fix, update`

#### **Good** examples:

- `git commit -m "docs: onboarding.md: add important links section"`
- `git commit -m "netbsd: x86_64: fix import paths in EFI driver"`

#### **Bad** examples:

- `git commit -m "fixed a few bugs"`
- `git commit -m "update the repository after three months of development"`
- `git commit -m "added module vim and python to core-image-minimal in build/local.conf, so that it now correctly executes the correct functions"`

### Pushing changes 

- before starting doing a task pull all changes
- checkout from master and name that branch in convention "1-name-of-task/feature"
- push that branch
- create pull request
- wait for checking pull request by assign user
- if everything is good, merge bracnh, if not make changes

## Examples

Various templates, e.g. for documents, will be uploaded here.

template markdown: [project-readme-template.md](https://git.pg.edu.pl/p1305920/contextual-emotion/-/blob/master/general-docs/project-readme-template.md)

## Main documentation and results 
Here you can find the documentation and achieved results of the CxE project: [project-documentation.md](https://git.pg.edu.pl/p1305920/contextual-emotion/-/blob/master/general-docs/project-documentation.md), also here is the project review in pdf [cxe.pdf](https://git.pg.edu.pl/p1305920/contextual-emotion/-/blob/master/general-docs/CxE___Contextual_Emotion.pdf)

## How to run app
1. Plug Tobii to your computer
2. Calibrate Tobii
3. Wear Aidmed
4. Download NodeJs v. 18.12.1
5. run script run.sh, if you are in the repo just type ./run.sh

If you just want to look at the website, without doing examination just type ./run.sh without previous steps.

