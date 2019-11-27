# type: ignore

from itertools import permutations
from typing import Any, Dict, List, Union

from .dllist import dllink
from .robin import robin

Part = Union[Dict[Any, int], List[int]]


class FMKWayGainCalc:

    __slots__ = ('totalcost', 'H', 'vertex_list', 'K', 'RR', 'deltaGainV')

    # public:

    def __init__(self, H, K: int):
        """initialization

        Arguments:
            H (Netlist):  description
            K (uint8_t):  number of partitions
        """
        self.totalcost = 0
        self.deltaGainV = list()

        self.H = H
        self.K = K
        self.RR = robin(K)

        self.vertex_list = []

        if isinstance(self.H.modules, range):
            for _ in range(K):
                self.vertex_list += [
                    list(dllink(i) for i in self.H.modules)
                ]
        elif isinstance(self.H.modules, list):
            for _ in range(K):
                self.vertex_list += [
                    {v: dllink(v) for v in self.H.modules}
                ]
        else:
            raise NotImplementedError

    def init(self, part: Part):
        """(re)initialization after creation

        Arguments:
            part (list):  description
        """
        self.totalcost = 0

        if isinstance(self.H.modules, range):
            for k in range(self.K):
                for vlink in self.vertex_list[k]:
                    vlink.key = 0
        elif isinstance(self.H.modules, list):
            for k in range(self.K):
                for vlink in self.vertex_list[k].values():
                    vlink.key = 0
        else:
            raise NotImplementedError

        for net in self.H.G.edges():
            self.__init_gain(net, part)
        return self.totalcost

    def __init_gain(self, net, part: Part):
        """initialize gain

        Arguments:
            net (node_t):  description
            part (list):  description
        """
        w, v = net
        if w == v:  # unlikely, self-loop, etc.
            return  # does not provide any gain when move
        self.__init_gain_2pin_net(net, part)

    def __modify_gain(self, v, pv, weight):
        """Modify gain

        Arguments:
            v (node_t):  description
            weight (int):  description
        """
        for k in self.RR.exclude(pv):
            self.vertex_list[k][v].key += weight

    def __init_gain_2pin_net(self, net, part: Part):
        """initialize gain for 2-pin net

        Arguments:
            net (node_t):  description
            part (list):  description
        """
        w, v = net
        part_w = part[w]
        part_v = part[v]
        weight = self.H.get_net_weight(net)
        if part_v == part_w:
            for a in [w, v]:
                self.__modify_gain(a, part_v, -weight)
        else:
            self.totalcost += weight
            self.vertex_list[part_v][w].key += weight
            self.vertex_list[part_w][v].key += weight

    def update_move_init(self):
        """update move init
        """
        self.deltaGainV = list(0 for _ in range(self.K))

    def update_move_2pin_net(self, part, move_info):
        """Update move for 2-pin net

        Arguments:
            part (list):  description
            move_info (MoveInfoV):  description

        Returns:
            dtype:  description
        """
        net, fromPart, toPart, v = move_info
        u, t = net
        w = u if u != v else t
        part_w = part[w]
        weight = self.H.get_net_weight(net)
        deltaGainW = list(0 for _ in range(self.K))

        for l in [fromPart, toPart]:
            if part_w == l:
                for k in range(self.K):
                    deltaGainW[k] += weight
                    self.deltaGainV[k] += weight
            deltaGainW[l] -= weight
            weight = -weight

        return w, deltaGainW
