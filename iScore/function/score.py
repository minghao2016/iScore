import os
import numpy as np

class iscore(object):

    def __init__(self,graphrank_out='GraphRank.out', energy_out='Energy.out',
                 weights = [0.941,0.041,0.217,0.032]):

        self.graphrank_out = graphrank_out
        self.energy_out = energy_out
        self.weights = weights

        self.features = dict()

        self.read_energy()
        self.read_graphrank()
        self.score()
        self.print()

    def read_energy(self):
        """Read the energy poutput file."""

        with open(self.energy_out,'r') as f:
            data = f.readlines()

        for line in data[1:]:
            mol,vdw,clb,des = line.split()
            if mol not in self.features:
                self.features[mol] = dict()

            self.features[mol]['evdw'] = float(vdw)
            self.features[mol]['ec'] = float(clb)
            self.features[mol]['edesolv'] = float(des)

    def read_graphrank(self):
        """Read the graph rank output file."""

        with open(self.graphrank_out,'r') as f:
            data = f.readlines()

        for line in data[1:]:
            l = line.split()
            mol = l[0]
            if mol not in self.features:
                self.features[mol] = dict()
            self.features[mol]['grank'] = float(l[-1])

    def score(self):
        """compute and output the iScore."""

        for mol,feat in self.features.items():
            data = [feat['grank'],feat['evdw'],feat['ec'],feat['edesolv']]
            self.features[mol]['iscore'] = self._scoring_function(data,self.weights)

    def print(self):
        """Print the energy terms."""

        fname='iScorePredict.dat'
        f = open(fname,'w')
        f.write('{:10} {:>14}     {:>14}     {:>14}     {:>14}     {:>14}\n'.format('#Name','GraphRank','nEVDW','nEC','nEDESOLV','iScore'))
        for name,feat in  self.features.items():
            st = "{:10} {: 14.3f}     {: 14.3f}     {: 14.3f}     {: 14.3f}     {: 14.3f}\n"
            f.write(st.format(name,feat['grank'],feat['evdw'],feat['ec'],feat['edesolv'],feat['iscore']))
        f.close()

    @staticmethod
    def _scoring_function(features,weights):

        if isinstance(weights,list):
            weights = np.array(weights)
        if isinstance(features,list):
            features = np.array(features)

        return np.sum(features*weights)