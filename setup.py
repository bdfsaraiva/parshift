from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="py-participation-shifts",
    packages=find_packages(exclude=["notebooks", "docs"]),
    version="0.12.0",
    author="Bruno D. Ferreira-Saraiva",
    author_email="bruno.saraiva@ulusofona.pt",
    description="py Participation Shift description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bdfsaraiva/py-Participation-Shifts/",
    project_urls={
        "Documentation": "https://bdfsaraiva.github.io/py-Participation-Shifts/",
        "Source Code": "https://github.com/bdfsaraiva/py-Participation-Shifts/",
    },
    keywords="nlp sbert embeddings participation-shifts",
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=base_packages,
#     extras_require={
#         "test": test_packages,
#         "docs": docs_packages,
#         "dev": dev_packages,
#         "flair": flair_packages,
#         "spacy": spacy_packages,
#         "use": use_packages,
#         "gensim": gensim_packages
#     },
    python_requires='>=3.8',
)
