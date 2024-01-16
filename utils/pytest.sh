#! /bin/bash

coverage run -m pytest -vvx --capture=tee-sys --log-cli-level=INFO tests/
coverage-badge -o assets/cov.svg