# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Union

from .dllist import dllink

Part = Union[Dict[Any, int], List[int]]


class FMBiGainCalc:

    __slots__ = ('totalcost', 'H', 'vertex_list')

    # public:

    def __init__(self, H, K=2):
        """Initialization

        Arguments:
            H (Netlist):  description

        Keyword Arguments:
            K (uint8_t):  number of partitions (default: {2})
        """
        self.H = H
        if isinstance(self.H.modules, range):
            self.vertex_list = [
                dllink(i) for i in self.H.modules
            ]
        elif isinstance(self.H.modules, list):
            self.vertex_list = {v: dllink(v) for v in self.H.modules}
        else:
            raise NotImplementedError

    def init(self, part: Part) -> int:
        """(re)initialization after creation

        Arguments:
            part ([type]): [description]

        Raises:
            NotImplementedError: [description]

        Returns:
            [type]: [description]
        """
        self.totalcost = 0
        if isinstance(self.H.modules, range):
            for vlink in self.vertex_list:
                vlink.key = 0
        elif isinstance(self.H.modules, list):
            for vlink in self.vertex_list.values():
                vlink.key = 0
        else:
            raise NotImplementedError

        for net in self.H.G.edges():
            # for net in self.H.net_list:
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

    def __modify_gain(self, w, weight):
        """Modify gain

        Arguments:
            v (node_t):  description
            weight (int):  description
        """
        self.vertex_list[w].key += weight

    def __init_gain_2pin_net(self, net, part: Part):
        """initialize gain for 2-pin net

        Arguments:
            net (node_t):  description
            part (list):  description
        """
        w, v = net
        weight = self.H.get_net_weight(net)
        if part[w] != part[v]:
            self.totalcost += weight
            self.__modify_gain(w, weight)
            self.__modify_gain(v, weight)
        else:
            self.__modify_gain(w, -weight)
            self.__modify_gain(v, -weight)

    def update_move_init(self):
        """update move init

           nothing to do in 2-way partitioning
        """
        pass

    def update_move_2pin_net(self, part, move_info):
        """Update move for 2-pin net

        Arguments:
            part (list):  description
            move_info (MoveInfoV):  description

        Returns:
            dtype:  description
        """
        net, fromPart, _, v = move_info
        u, t = net
        w = u if u != v else t
        weight = self.H.get_net_weight(net)
        delta = 2 if part[w] == fromPart else -2
        return w, delta * weight
