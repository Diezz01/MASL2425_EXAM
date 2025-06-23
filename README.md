# MASL2425_Exam

This project was developed as part of the *Multiagent System Lab* course of the University of Camerino.  
## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Diezz01/MASL2425_EXAM.git
cd MASL2425_EXAM
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
```
### 3. Activate the Virtual Environment

```bash
.\.venv\Scripts\activate
```
### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Application
### 1. Using web interface
Here using the GUI provided by mesa is possible to run a a simulation with custom parameters
```bash
python python .\mesa_run.py 
```
### 2. Machine learning results
Generate a CSV file containing the simulation results using random parameters.
```bash
python python .\simulation_ml.py    
```
Run the jupyter notebook
```bash
jupyter notebook ./machine_learning.ipynb
```
