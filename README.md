# Project Template

In this file, we give you some general guideline and advices for this project. You need two components:

1. Python 3.6
1. gurobi

## Python

Linux users should have python already installed in their PC. For the other users it is strongly recommended to install **Anaconda** and to use its terminal for installing new packages. You can find details [here](https://www.anaconda.com/distribution/) and [there](https://www.anaconda.com/distribution/#download-section). 


## gurobi
gurobi is a commercial software. See [here](https://www.gurobi.com/)


## Python packages:
Probably you will need to install several packages (e.g., pulp, numpy, networkx, matplotlib, etc). In linux our suggestion is to use pip
~~~
pip3 install <package name>
~~~
e.g., 
~~~
pip3 install networkx
~~~
For windows is suggest to use conda.
~~~
conda install -c conda-forge pulp 
~~~


## Run the code:
Run the main code containing the **gurobi** solution and the heuristic(s) by writing in the terminal
```
python3 main.py
```

Run the code to get the statistics regarding the **gurobi** solution and the heuristic(s) by writing in the terminal
``` 
python3 main2.py
```


## Text Editor

In order write good code you need a good editor. The best one that I recommend are:

1. [Visual Studio Code](https://code.visualstudio.com/) free;
1. [Sublime Text](https://www.sublimetext.com/) free for non commercial usage;
1. [PyCharm](https://www.jetbrains.com/pycharm/) free for students.

## Project

In the project we consider the following simple problem:
$$
min \sum_{k \in N} f_{k}z_{k} + \sum_{s \in S_{w}} p_{s} \sum_{\substack{i,k \in N \\ i \neq k}} c_{ik}^{s}x_{ik}^{s} + \sum_{s \in S_{w}} p_{s} \sum_{i,j \in N} \alpha w_{ij}^{s}\bigg(d_{ij}z_{i}z_{j} + \sum_{\substack{l \in N \\ l \neq j}} d_{il}z_{i}x_{jl}^{s} + \sum_{\substack{k \in N \\ i \neq k}} d_{kj}x_{ik}^{s}z_{j} + \sum_{\substack{k, l \in N \\ i \neq k \\ j \neq l}} d_{kl}x_{ik}^{s}x_{jl}^{s}\bigg)
$$

$$
where: \emph{c\textsubscript{ij}\textsuperscript{s} = d\textsubscript{ik} ($\chi$ O\textsubscript{i}\textsuperscript{s} + $\delta$ D\textsubscript{i}\textsuperscript{s}) }
$$


subject to:


$$
 \quad \sum_{\substack{k \in N \\ i \neq k }} x_{ij}^{s} = 1 - z_{i} \quad \quad i \in N,   s \in S_{w}
$$

$$
x_{ik}^{s} \leq z_{k} \quad \quad i,k \in N, i \neq k,  s \in S_{w}
$$

$$
z_{i} \in \{0,1\} \quad \forall i \in N
$$

$$
 z_{ik}^{s} \in \{0,1\} \quad \forall i \in N, s \in S_{w}
$$



