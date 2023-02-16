# rBuild
rBuild is a series of tools for building a Linux distribution. It's main goals are to make it easier to build ISOs and core packages for distributions.
At the moment, rBuild is only functional to create Fedora based distros, but it is planned to support other distributions in the future.
Configuing a distribution can be done with a simple YAML config file to set distro properties (which may be different across certain distro build tools), and it will soon be used to generate packages as well.

The latest versions of risiOS (37.1.1+) have been built using rBuild.

### Work in Progress!!!!!!

Currently only the bare basic functionality of rBuild has been implemented and cannot be used yet. For example, there is no cli interface yet, and only a Python API. It is also missing many planned features.
It also worth noting rBuild is not yet API stable, so api changes may occur and this is not recommended for outside production use yet.

### Development Progress
- [x] yaml parsing
- [ ] kickstart building
  - [ ] Fedora based distributions
    - [x] iso building
      - [ ] package building (drop in replacements with branding modifications)
        - [x] fedora-logos
        - [ ] fX-backgrounds
        - [ ] fedora-repositories
        - [ ] anaconda config (see anaconda-risi package)
  - [ ] Alma based distributions
  - [ ] Potentially other distributions
