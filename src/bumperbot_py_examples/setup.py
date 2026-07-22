from setuptools import find_packages, setup

package_name = "bumperbot_py_examples"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="syed",
    maintainer_email="serveronthego1@gmail.com",
    description="publisher_member_function",
    license="Apache 2.0",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            # always add a main function to your python scripts and call it here
            "publisher_member_function = bumperbot_py_examples.publisher_member_function:main",
            "subscriber_member_function = bumperbot_py_examples.subscriber_member_function:main",
        ],
    },
)
