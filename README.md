<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/apast005/QMS">
    <img src="Data-recording-UI/images/PathsUp.gif" alt="Logo" width="150" height="120">
  </a>

  <h3 align="center">Enabling Wearable Technology on Patients with High Body Mass Index</h3>

  <p align="center">
    The project aims to provide researchers with a User Interface to control a medical device in development, which keeps measurements of blood pressure and diabetes through the analysis of wavelength and light absorption using a spectrometer. Additionally, the project includes the use of Cloud Computing for Data Analytics from the gathered device data.
    <br />
    <a href="https://github.com/CPRGB/Senior_Design_2020.git"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/apast005/QMS">View Demo</a>
    ·
    <a href="https://github.com/apast005/QMS/issues">Report Bug</a>
    ·
    <a href="https://github.com/apast005/QMS/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [References Used](#references)
* [Acknowledgments](#acknowledgments)



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

The end goal of this project is to create wearable devices that monitor blood preasure levels and heart rate for overweight population. A user interface (UI) is being developed with different functionalities to facilitate researchers work when logging in patient's information and perform data recorderings. This UI will be running on a Raspberry Pi computer and will allow researchers to start recording sessions and save the gathered data to a database. The data recorded will be processed by an algorithm and displayed on a website accesible by multiple researchers around the world.
### Built With

* [Python3]()
* [Matplotlib]()
* [Microsoft Azure]()
* [Rapberry Pi]()



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This code was run and tested on a Raspberry Pi 3b+ that was connected to a STS spectrometer from Ocean Optics. This two components are essential to make this code functional. However, [THIS](https://github.com/jonathanvanschenck/python-seatease) emulator can be used to run and test the code from any computer in the absence of a Raspberry Pi and/or spectrometer.  
* Python-seabreeze
```sh
pip install seabreeze
seabreeze_os_setup
```
For more information about this library [click here](https://github.com/ap--/python-seabreeze)

### Installation

1. Clone the repo
```sh
git clone https://github.com/CPRGB/Senior_Design_2020.git
```
2. CONTINUE...


<!-- USAGE EXAMPLES -->
## Usage

The graphical user interface makes pretty easy the interaction.

* The "Log in" page authenticates the researcher that will start the data recording on the patient. This screen also allows a new researcher to create an account and recover password in case they forget.
<p align="center">
  <a href="https://github.com/apast005/QMS">
    <img src="Data-recording-UI/images/PathsUp.gif" alt="Logo" width="500" height="600">
  </a>
<p align="center">

* The "Sign up" page is just to create a new user(researcher) and it asks for some basic information. 
<p align="center">
  <a href="https://github.com/apast005/QMS">
    <img src="Data-recording-UI/images/PathsUp.gif" alt="Logo" width="500" height="600">
  </a>
<p align="center">


_For more examples, please refer to the [Documentation](https://example.com)_



<!-- ROADMAP -->
## Roadmap
1. Increase Usability      
    - [X] Download the appropriate components from GitHub and produce useful messages and/or log files for users as appropriate.  
    - [ ] Outputs of these test benches also should be displayed in the terminal or into log files in ways that make sense
    - [ ] A user should be able to turn interactive mode on or off (for
              * Example:  Windows users executing these test benches over Putty

2. Automate component integration/testing
    - [X] Automate this process through scripts that could process these dependency files and check if dependencies have been installed
    - [ ] Test benches for components should be automatically executed upon installation to validate a working component.

3. Documentation is in PDF table that specifies the module name, dependencies, inputs, outputs, and an English description of the component.  
    - [ ] Alternative environment for documentation like Unix “man” pages.

4. See the [open issues](https://github.com/apast005/QMS/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

This is my first time trying Shell Scripting to automate a task.  Any feedback/suggestions is greatly appreciated and I thank you for taking the time
to help me grow and provide a contribution to the open source community.

Below is a template from a README template I used that is listed in Acknowledgments
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Alex Pastoriza - apast005@fiu.edu

Project Link: [https://github.com/apast005/QMS](https://github.com/apast005/QMS)



<!-- REFERENCES -->
## References

* [Intel Installation Guide](https://www.intel.com/content/dam/www/programmable/us/en/pdfs/literature/manual/quartus_install.pdf#page=12&zoom=auto,-207,693)
* [Intel Quick Start Guide](https://fpgasoftware.intel.com/static/quick_start_guide/quick_start_guide_20.1_en.pdf)
* [Quartus Manual](https://www.intel.com/content/dam/www/programmable/us/en/pdfs/literature/manual/quartus_install.pdf)
* [Intel Installation FAQS](https://www.intel.com/content/www/us/en/programmable/downloads/software/faq/installation-faq.html?erpm_id=8905536_ts1601556901225#_Toc361418227)
* [Intel's Download Center](https://fpgasoftware.intel.com/20.1/?edition=lite)
* []()



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
* [Template for README](https://github.com/othneildrew/Best-README-Template/blob/master/BLANK_README.md)
* []()
* []()





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/apast005/QMS.svg?style=flat-square
[contributors-url]: https://github.com/apast005/QMS/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/apast005/QMS.svg?style=flat-square
[forks-url]: https://github.com/apast005/QMS/network/members
[stars-shield]: https://img.shields.io/github/stars/apast005/QMS.svg?style=flat-square
[stars-url]: https://github.com/apast005/QMS/stargazers
[issues-shield]: https://img.shields.io/github/issues/apast005/QMS.svg?style=flat-square
[issues-url]: https://github.com/apast005/QMS/issues
[license-shield]: https://img.shields.io/github/license/apast005/QMS.svg?style=flat-square
[license-url]: https://github.com/apast005/QMS/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-blue.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/alexander-pastoriza
[product-screenshot]: images/screenshot.png
