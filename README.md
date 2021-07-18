# Project: STOCHASTIC SINGLE-ALLOCATION HUB LOCATION

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
Run the main code containing the **gurobi** solution and the 3 heuristics by writing in the terminal
```
python3 main.py
```

Run the code to get the statistics regarding the **gurobi** solution and the 3 heuristics by writing in the terminal
``` 
python3 main2.py
```


## Text Editor

In order write good code you need a good editor. The best one that I recommend are:

1. [Visual Studio Code](https://code.visualstudio.com/) free;
1. [Sublime Text](https://www.sublimetext.com/) free for non commercial usage;
1. [PyCharm](https://www.jetbrains.com/pycharm/) free for students.

## Problem

We consider the following **two-stage stochastic SAHLP** problem:

<a href="https://www.codecogs.com/eqnedit.php?latex=min&space;\sum_{k&space;\in&space;N}&space;f_{k}z_{k}&space;&plus;&space;\sum_{s&space;\in&space;S_{w}}&space;p_{s}&space;\sum_{\substack{i,k&space;\in&space;N&space;\\&space;i&space;\neq&space;k}}&space;c_{ik}^{s}x_{ik}^{s}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?min&space;\sum_{k&space;\in&space;N}&space;f_{k}z_{k}&space;&plus;&space;\sum_{s&space;\in&space;S_{w}}&space;p_{s}&space;\sum_{\substack{i,k&space;\in&space;N&space;\\&space;i&space;\neq&space;k}}&space;c_{ik}^{s}x_{ik}^{s}" title="min \sum_{k \in N} f_{k}z_{k} + \sum_{s \in S_{w}} p_{s} \sum_{\substack{i,k \in N \\ i \neq k}} c_{ik}^{s}x_{ik}^{s}" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex=&plus;&space;\sum_{s&space;\in&space;S_{w}}&space;p_{s}&space;\sum_{i,j&space;\in&space;N}&space;\alpha&space;w_{ij}^{s}\bigg(d_{ij}z_{i}z_{j}&space;&plus;&space;\sum_{\substack{l&space;\in&space;N&space;\\&space;l&space;\neq&space;j}}&space;d_{il}z_{i}x_{jl}^{s}&space;&plus;&space;\sum_{\substack{k&space;\in&space;N&space;\\&space;i&space;\neq&space;k}}&space;d_{kj}x_{ik}^{s}z_{j}&space;&plus;&space;\sum_{\substack{k,&space;l&space;\in&space;N&space;\\&space;i&space;\neq&space;k&space;\\&space;j&space;\neq&space;l}}&space;d_{kl}x_{ik}^{s}x_{jl}^{s}\bigg)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?&plus;&space;\sum_{s&space;\in&space;S_{w}}&space;p_{s}&space;\sum_{i,j&space;\in&space;N}&space;\alpha&space;w_{ij}^{s}\bigg(d_{ij}z_{i}z_{j}&space;&plus;&space;\sum_{\substack{l&space;\in&space;N&space;\\&space;l&space;\neq&space;j}}&space;d_{il}z_{i}x_{jl}^{s}&space;&plus;&space;\sum_{\substack{k&space;\in&space;N&space;\\&space;i&space;\neq&space;k}}&space;d_{kj}x_{ik}^{s}z_{j}&space;&plus;&space;\sum_{\substack{k,&space;l&space;\in&space;N&space;\\&space;i&space;\neq&space;k&space;\\&space;j&space;\neq&space;l}}&space;d_{kl}x_{ik}^{s}x_{jl}^{s}\bigg)" title="+ \sum_{s \in S_{w}} p_{s} \sum_{i,j \in N} \alpha w_{ij}^{s}\bigg(d_{ij}z_{i}z_{j} + \sum_{\substack{l \in N \\ l \neq j}} d_{il}z_{i}x_{jl}^{s} + \sum_{\substack{k \in N \\ i \neq k}} d_{kj}x_{ik}^{s}z_{j} + \sum_{\substack{k, l \in N \\ i \neq k \\ j \neq l}} d_{kl}x_{ik}^{s}x_{jl}^{s}\bigg)" /></a>



where: 

<a href="https://www.codecogs.com/eqnedit.php?latex=\emph{c\textsubscript{ij}\textsuperscript{s}&space;=&space;d\textsubscript{ik}&space;($\chi$&space;O\textsubscript{i}\textsuperscript{s}&space;&plus;&space;$\delta$&space;D\textsubscript{i}\textsuperscript{s}})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\emph{c\textsubscript{ij}\textsuperscript{s}&space;=&space;d\textsubscript{ik}&space;($\chi$&space;O\textsubscript{i}\textsuperscript{s}&space;&plus;&space;$\delta$&space;D\textsubscript{i}\textsuperscript{s}})" title="\emph{c\textsubscript{ij}\textsuperscript{s} = d\textsubscript{ik} ($\chi$ O\textsubscript{i}\textsuperscript{s} + $\delta$ D\textsubscript{i}\textsuperscript{s}})" /></a>




subject to:



(1)   <a href="https://www.codecogs.com/eqnedit.php?latex=\quad&space;\sum_{\substack{k&space;\in&space;N&space;\\&space;i&space;\neq&space;k&space;}}&space;x_{ij}^{s}&space;=&space;1&space;-&space;z_{i}&space;\quad&space;\quad&space;i&space;\in&space;N,&space;s&space;\in&space;S_{w}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\quad&space;\sum_{\substack{k&space;\in&space;N&space;\\&space;i&space;\neq&space;k&space;}}&space;x_{ij}^{s}&space;=&space;1&space;-&space;z_{i}&space;\quad&space;\quad&space;i&space;\in&space;N,&space;s&space;\in&space;S_{w}" title="\quad \sum_{\substack{k \in N \\ i \neq k }} x_{ij}^{s} = 1 - z_{i} \quad \quad i \in N, s \in S_{w}" /></a>


(2)   <a href="https://www.codecogs.com/eqnedit.php?latex=x_{ik}^{s}&space;\leq&space;z_{k}&space;\quad&space;\quad&space;i,k&space;\in&space;N,&space;i&space;\neq&space;k,&space;s&space;\in&space;S_{w}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?x_{ik}^{s}&space;\leq&space;z_{k}&space;\quad&space;\quad&space;i,k&space;\in&space;N,&space;i&space;\neq&space;k,&space;s&space;\in&space;S_{w}" title="x_{ik}^{s} \leq z_{k} \quad \quad i,k \in N, i \neq k, s \in S_{w}" /></a>


(3)   <a href="https://www.codecogs.com/eqnedit.php?latex=z_{i}&space;\in&space;\{0,1\}&space;\quad&space;\forall&space;i&space;\in&space;N" target="_blank"><img src="https://latex.codecogs.com/gif.latex?z_{i}&space;\in&space;\{0,1\}&space;\quad&space;\forall&space;i&space;\in&space;N" title="z_{i} \in \{0,1\} \quad \forall i \in N" /></a>


(4)   <a href="https://www.codecogs.com/eqnedit.php?latex=z_{ik}^{s}&space;\in&space;\{0,1\}&space;\quad&space;\forall&space;i&space;\in&space;N,&space;s&space;\in&space;S_{w}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?z_{ik}^{s}&space;\in&space;\{0,1\}&space;\quad&space;\forall&space;i&space;\in&space;N,&space;s&space;\in&space;S_{w}" title="z_{ik}^{s} \in \{0,1\} \quad \forall i \in N, s \in S_{w}" /></a>

## main.py

In _**main.py**_ it is possible to select which dataset (_.txt_ file) contained in the _etc_ folder we would like to solve.

For instance, we can solve the dataset containing 10 nodes (10L) with fixed cost by typing:
``` 
(27)    filename = "./etc/10L"
```

Dataset options are: _10L; 10T; 20L; 20T; 25L; 25T; 40L; 40T; 50L; 50T_ and _easy_instance_ (6 nodes).


It is also possible to select the number of scenarios for our problem by modifying the variable _n_scenarios_:
``` 
(39)    n_scenarios = 5
```

_**instanceSampler.py**_ and _**sampler.py**_ are then used to generate the instances of our problem.

_**stochasticSaphlp.py**_ is used to solve the objective function using **gurobi**.

_**simpleHeu.py**_; _**heuNew.py**_ and _**heuNew2.py**_  are used to solve our problem using a heuristic.

 For every solution, _**main.py**_ prints the objective function value, the computational time and the vector _solZ_.  _**plot_results.py**_ will be used to draw the solutions.



## instanceSampler.py

The filename selected in _**main.py**_ is passed to _**instanceSampler.py**_

The dataset is read from the file and is then used to compute the instances of our problem. 

We read first the number of nodes. Each node is represented by a pair of cartesian coordinates _x_ and _y_ that will be used in order to compute the distance between the nodes, 
the distances will be written in the matrix <a href="https://www.codecogs.com/eqnedit.php?latex=d_{ij}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?d_{ij}" title="d_{ij}" /></a>

The flow between the nodes _i_ and _j_ is then read and stored the matrix <a href="https://www.codecogs.com/eqnedit.php?latex=w_{ij}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?w_{ij}" title="w_{ij}" /></a>

Additionnally we read _alpha_, _chi_ and _sigma_ and the fixed cost for each node.

## sampler.py

In  _**sampler.py**_, we use the matrix <a href="https://www.codecogs.com/eqnedit.php?latex=w_{ij}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?w_{ij}" title="w_{ij}" /></a> created in  _**instanceSampler.py**_ in order to generate the the matrix <a href="https://www.codecogs.com/eqnedit.php?latex=w_{ij}^{s}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?w_{ij}^{s}" title="w_{ij}^{s}" /></a> for each scenario by multiplying each element of the <a href="https://www.codecogs.com/eqnedit.php?latex=w_{ij}^{s}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?w_{ij}^{s}" title="w_{ij}^{s}" /></a> matrix by <a href="https://www.codecogs.com/eqnedit.php?latex=p_{i}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?p_{i}" title="p_{i}" /></a> and <a href="https://www.codecogs.com/eqnedit.php?latex=p_{j}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?p_{j}" title="p_{j}" /></a>, 2 random numbers uniformily distributed between 0.5 and 1.5

Then for each scenario we compute the outgoing flow <a href="https://www.codecogs.com/eqnedit.php?latex=O_{i}^{s}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?O_{i}^{s}" title="O_{i}^{s}" /></a>, the incoming flow <a href="https://www.codecogs.com/eqnedit.php?latex=D_{i}^{s}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?D_{i}^{s}" title="D_{i}^{s}" /></a> and the cost <a href="https://www.codecogs.com/eqnedit.php?latex=c_{ij}^{s}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?c_{ij}^{s}" title="c_{ij}^{s}" /></a> associated between each 2 nodes _i_ and _j_.

## stochasticSaphlp.py 

In _**stochasticSaphlp.py**_ the objective function is solved using **gurobi**. 

All generated instances are passed as parameters to _**stochasticSaphlp.py**_ and are used to evaluate the objective function.

First, two **gurobi** variables _X_ and _Z_ are defined where the matrix _X_ represents the connections between the nodes and the vector _Z_ indicates whether a node is a hub. The numbers contained in _X_ and _Z_ can only take the values 0 or 1

The objecive function is computed for every scenario and then we obtain _obj_funct_ by averaging the solution of every scenario by the total number of scenarios. After adding the constraints of the problem, the objective function is solved using **gurobi**. A log file is saved containing the results of the computations done by **gurobi**.

The value of the _obj_funct_, the computational time and the solution variables _solZ_ and _SolX_ computed by **gurobi** are returned back to _**main.py**_


## simpleHeu.py 

_**simpleHeu.py**_  is the first suggested heuristic for the problem.

In every scenario, a penalty function _p[i]_ is computed using the fixed cost, the outgoing flow <a href="https://www.codecogs.com/eqnedit.php?latex=O_{i}^{s}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?O_{i}^{s}" title="O_{i}^{s}" /></a>, the incoming flow <a href="https://www.codecogs.com/eqnedit.php?latex=D_{i}^{s}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?D_{i}^{s}" title="D_{i}^{s}" /></a> and the cost <a href="https://www.codecogs.com/eqnedit.php?latex=c_{ij}^{s}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?c_{ij}^{s}" title="c_{ij}^{s}" /></a> for every node. 

Every _p[i]_ is compared to the average of the _p[]_ vector, if it is less, the node will become a hub. Then we check if there are hubs with no links, change them back to nodes and connect them to the nearest hub.

After solving the vector _Z_, _**ev_x.py**_ is used to connect the non-hub nodes to the nearest hub.

The values obtained are used to evaluate the heuristic objective function in order to compare it with the **gurobi** objective function.

Then the value of the objective function, the computational time and the solution variables _solZ_ and _SolX_ are returned back to _**main.py**_

