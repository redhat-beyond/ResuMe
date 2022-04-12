
# CONTRIBUTING
When contributing to this repository, please first discuss the change you wish to make via issue, GitHub, or any other method with the owners of this repository before making a change.

Please follow our code of conduct in all your interactions with the project.

### Project maintainers
- [Nati Fridman](https://github.com/natifridman)
- [Avi Biton](https://github.com/abiton1)
- [Elyasaf Halle](https://github.com/halleelyasaf)

### Project team
- [Alon Shakaroff](https://github.com/AlonShakaroff)
- [Omer Cohen Shor](https://github.com/OmerCS8)
- [Tomer Newman](https://github.com/TomerNewmanPrograms)
- [Yuli Suliman](https://github.com/yulisuliman)
- [Matan Peretz](https://github.com/MatanP12)

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards
Examples of behavior that contributes to creating a positive environment include:
-   Using welcoming and inclusive language
-   Being respectful of differing viewpoints and experiences
-   Gracefully accepting constructive criticism
-   Focusing on what is best for the community
-   Showing empathy towards other community members

Examples of unacceptable behavior by participants include:
-   The use of sexualized language or imagery and unwelcome sexual attention or advances
-   Trolling, insulting/derogatory comments, and personal or political attacks
-   Public or private harassment
-   Publishing others' private information, such as a physical or electronic address, without explicit permission
-   Other conduct which could reasonably be considered inappropriate in a professional setting

### Our Responsibilities
Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned to this Code of Conduct, or to ban temporarily or permanently any contributor for other behaviors that they deem inappropriate, threatening, offensive, or harmful.

### Scope

This Code of Conduct applies both within project spaces and in public spaces when an individual is representing the project or its community. Examples of representing a project or community include using an official project e-mail address, posting via an official social media account, or acting as an appointed representative at an online or offline event. Representation of a project may be further defined and clarified by project maintainers.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team on GitHub. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances. The project team is obligated to maintain confidentiality with regard to the reporter of an incident. Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good faith may face temporary or permanent repercussions as determined by other members of the project's leadership.

### Attribution
This Code of Conduct is adapted from the  [Contributor Covenant](http://contributor-covenant.org/), version 1.4, available at  [http://contributor-covenant.org/version/1/4](http://contributor-covenant.org/version/1/4/)

## Codding standard

We expect all Python code to conform to the [PEP8](https://www.python.org/dev/peps/pep-0008) standard.

## Pull Requests(PR) 

 - Each Pull Request should focus on single repository principle.
 - **The Pull Request should not break any of the existing functionality**
 - <ins>Description-</ins> the PR description should explain what changes have been made, and why. In addition, they should include a link to the relevant `issue`
 - Each PR should include 1-5 `commits`
 - Make sure the PR passes CI checks, therefore you need to run `pipenv run flake8 --max-line-length 120` and `pipenv run python -m pytest -v` inside your VM before submitting a new PR.
 - Each pull request requires the approval of at least <ins>2 team members</ins> before merging.
 - Update the ReadMe if needed.

## Issues

some tips for good issue reporting:
- The title Must be clear, and describe what the issue is about.
- The description of the issue must include a clear explanation about the reasons for doing the work.
- Status Labels(Optional):
  - Status/New - An issue that was just created, in addition unlabeled issues are considered new.
  - Status/Backlog - A issue that was discussed and accepted for work.
  - Status/In progress - An issue that is being worked on.

## Getting started

### Prerequisites
 - Install [Vagrant](https://www.vagrantup.com/downloads).
 - Install [Virtual Box](https://www.virtualbox.org/wiki/Downloads).

### Getting a copy of the repository 
1. Go to the [ResuMe](https://github.com/redhat-beyond/ResuMe) GitHub repository.
2.  Fork the repository and create a separate branch regarding your contribution.
3. Clone your forked repository to your local machine. the command should be something like: `git clone https://github.com/<YOUR_GITHUB_NAME>/ResuMe.git`
4. Open any terminal and navigate to the project directory.
5. Run the `vagrant up` command.

After the dependencies were installed and the VM initialized, you can proceed working on the project code.