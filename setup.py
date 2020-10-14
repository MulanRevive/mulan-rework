import setuptools

with open("README.md", encoding="utf-8", mode="r") as readme:
    longDescription = readme.read()

setuptools.setup(
    name="ulang",
    version="0.0.14.1",
    license="GNU GPLv3",
    author="吴烜",
    author_email="mulanrevive@gmail.com",
    entry_points = {
        "console_scripts": ['木兰 = 木兰.中:中']
        },
    description="木兰编程语言重现",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    url="https://www.oschina.net/p/mulan-rework",
        project_urls={
        "Source": "https://gitee.com/MulanRevive/mulan-rework",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'rply',
    ],
    python_requires="== 3.7.*"
)