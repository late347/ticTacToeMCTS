# ticTacToeMCTS
python mcts algorithm with tictactoe (monte carlo tree search)

-uses anytree library


It's possible the algorithm is a little bit flawed, since the decision results are not very good for the AI's decisions.
The code requires pip install anytree

-actually as a fix to the algoritm only the walkerFuncTraversal method should be used in the mcts, because most likely it will
have traversed the tree according to the algorithm. The treeiterator-based method walkUntilLeaf probably doesnt work as intended currently...

-I just forgot to change the walkUntilLeaf into the walkerFuncTraversal!


Code was developed in PyCharm IDE, and I just took all the files from the project directory and uploaded them to this repository

useful links

I mostly tried to follow the tutorial from analyticsvidhya.com article below

https://github.com/int8/monte-carlo-tree-search

https://github.com/PetterS/monte-carlo-tree-search

https://www.analyticsvidhya.com/blog/2019/01/monte-carlo-tree-search-introduction-algorithm-deepmind-alphago/

https://int8.io/monte-carlo-tree-search-beginners-guide/#Monte_Carlo_Tree_Search_8211_basic_concepts

https://anytree.readthedocs.io/en/latest/
