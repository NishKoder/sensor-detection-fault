from typing import List
from setuptools import find_packages, setup


def get_requirements() -> List[str]:
    """
    Returns a list of requirements
    """
    requirements_list: List[str] = []
    with open("requirements.txt") as f:
        requirements_list.extend(
            line.strip() for line in f if not line.startswith("-e ")
        )
    return requirements_list


setup(
    name="sensor",
    version="0.0.1",
    author="Nishant Gupta",
    author_email="nishant.apple.app@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
