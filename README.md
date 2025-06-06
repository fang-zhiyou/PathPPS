

### PathPPS: A Lightweight Privacy-Preserving Shortest Path Query Scheme for Path Navigation Service

This is the associated artifact for the paper "PathPPS: A Lightweight Privacy-Preserving Shortest Path Query Scheme for Path Navigation Service".

#### Detailed Usage

Our experiments assume prior installation of Python 3 via the conda. First clone the repository. A list of dependancies can be found in requirements.txt.

Folder datasets contain the datasets of the six real world road networks, including Beijing, Chicago, Feicheng, Sparse1, Sparse2 and Sparse3. The Philadelphia is denoted as Feicheng.

In `benchmark.py` file, please set the parameter and run the code.

Lastly, please run the code in conda environment.

```python
python Benchmark.py
```


#### Others

GTKandPathGES.zip contains the source code of GTK and PathGES(CCS 2024) scheme.

gen_dataset.py can generate a grid-based map automatically.
