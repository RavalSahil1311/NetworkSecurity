from setuptools import find_packages, setup
from typing import List


def get_requirements() -> List[str]:
    """This Function will return list of requirements"""
    try:
        requirement_list: List[str] = []
        with open("requirements.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != "-e .":
                    requirement_list.append(requirement)
        return requirement_list
    except FileNotFoundError:
        print("Requirements.txt not found")


setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Sahil Raval",
    author_email="ravalsahil1311@gmail.com",
    packeges=find_packages(),
    install_requires=get_requirements(),
)

if __name__ == "__main__":
    print(get_requirements())
