Prerequisites
----------------------

This project was created in a Python 3.6 environment. It will be easier to set up the project if you install [Anaconda](https://conda.io/docs/user-guide/install/download.html) or [Miniconda](https://conda.io/miniconda.html). Other options, such as [PyEnv](https://github.com/pyenv/pyenv) and classic virtual environment (i.e. `venv`), will also work.


Installation and Setup
----------------------

Run the following commands in Terminal:

```sh
git clone https://github.com/colin-c6/Airplanes_Project.git && cd /Airplanes_Project
conda env create -f environment.yml
pip install -r requirements.txt
```

Running the Program With Greedy Algorihtm
-------------------

From the project directory (in Terminal), run this command

```sh
python main_greedy.py

```
Running the Program With Exhaustive Algorithm
-------------------

From the project directory (in Terminal), run this command

```sh
python main_exhaustive.py
```

Running the Program With Your Own CSV file
-------------------

From the project directory (in Terminal), run this command

```sh
python main_greedy.py 'path to csv'
or
python main_exhaustive.py 'path to csv'
```

Running the Tests
------------------

From the project directory (in Terminal), run this command

```sh
python performance_testing_main.py
```

