Publish Church Directory
========================

A collection of scripts to publish the church directory as a PDF file to a 'well-known' web URL.

## Requirements

For the purposes of this README iti is assumed that we're running on Ubuntu 20.04 but with minor adaptation it should run on any unix-like system.

- python 3
- Jinja 2 template system for python
- Webkit to PDF utility (wkhtmltopdf)
- Virtual X server (if running in a headless server environment) (xvfb)
- PDF jam utilitiles (within texlive-extra-utils)
- sshpass (to supply password to SSH, could also be done by public key auth)
  - an appropriately secured password file (check publish-directory.sh for the expected location)

## Usage

Assuming the pre-requisites are in place it suffices to run:

```
./publish-directory.sh
```

