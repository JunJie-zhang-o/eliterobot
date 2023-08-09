#! /bin/bash
#!/usr/bin/sh

# you need to execute "pip3 install twine"
twine upload --skip-existing dist/* --verbose