iScore Workflow
========================

One of the mainfeature of the software are the serial and MPI binaries that fully automatize the workflow and that can be used directly from the command line. To illustrate the use of these binaries go to the folder ``iScore/example/training_set/``. This folder contains the subfolders ``pdb/`` and ``pssm/`` that contain the PDB and PSSM files of our training set. The binary class corresponding to these PDBs are specified in the file 'caseID.lst'.

Training a model using iScore can be done in a single line using MPI binaries with the command :


``$ mpiexec -n 2 iScore.train.mpi``


This command will first generate the graphs of the conformations stored in ``pdb/`` using the PSSM contained in ``pssm/`` as features. These graphs will be stored as pickle file  in ``graph/``. The command  will then compute the pairwise kernels of these graphs and store the kernel files in ``kernel/``. Finally it will train a SVM model using the kernel files and the ``caseID.lst`` file that contains the binary class of the model.

The calculated graphs and the svm model are stored in a single tar file called here ``training_set.tar.gz``. This file contains all the information needed to predict binary classes of a test set using the trained model.

To predict binary classes (and decision values) of new conformations go to the subfoler ``test/``. Here 5 conformations are specified by the PDB and PSSM files stored in ``pdb/`` and ``pssm/`` that we want to use as a test set. Ranking these conformations can be done in a single command using :

``$ mpiexec -n 2 iScore.predict.mpi --archive ../training_set.tar.gz``

This command will use first compute the graph of the comformation in the test set and store them in `graph/`. The binary will then compute the pair wise kernels of each graph in the test set with all the graph contained in the training set that are stored in the tar file. These kernels will be stored in ``kernel/``. Finally the binary will use the trained SVM model contained in the tar file to predict the binary class and decision value of the conformations in the test set. The results are then stored in a text file and a pickle file ``iScorePredict.pkl`` and ``iScorePredict.txt``. Opening the text file you will see :

+--------+--------+---------+-------------------+
|Name    |   label|     pred|     decision_value|
+--------+--------+---------+-------------------+
|1ACB_2w |   None |       0 |           -0.994  |
+--------+--------+---------+-------------------+
|1ACB_3w |   None |       0 |           -0.994  |
+--------+--------+---------+-------------------+
|1ACB_1w |   None |       0 |           -0.994  |
+--------+--------+---------+-------------------+
|1ACB_4w |   None |       0 |           -0.994  |
+--------+--------+---------+-------------------+
|1ACB_5w |   None |       0 |           -0.994  |
+--------+--------+---------+-------------------+


The ground truth label are here all None because they were not provided in the test set. This can simply be done by adding a ``caseID.lst`` in the ``test/`` subfolder.


Serial Binaries
------------------------

Serial binaries are also provided and can be used in a similar way than  the MPI binaries : ``iscore.train`` and ``iscore.predict``



