from setuptools import find_packages
from setuptools import setup
import os

if "VERSION" in os.environ:
    # Version is set by the environment
    version = os.getenv("VERSION")
else:
    # Assuming local development
    try:
        # Try to get latest version from git, add +develop
        import subprocess
        version = "{}+develop".format(
            subprocess.check_output(["git","describe","--abbrev=0"]).decode().rstrip('\r\n')
        )
    except:
        # Default to '0.0.1+develop'
        version = '0.0.1+develop'
        
setup(
    name='example',
    version=version,
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    description='...'
)
