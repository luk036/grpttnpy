from typing import Any, Dict, List, Union

from grpttnpy.FMBiConstrMgr import FMBiConstrMgr
from grpttnpy.FMBiGainCalc import FMBiGainCalc
from grpttnpy.FMBiGainMgr import FMBiGainMgr
from grpttnpy.FMPartMgr import FMPartMgr
from grpttnpy.netlist import Netlist, create_drawf, create_p1, create_test_netlist

Part = Union[Dict[Any, int], List[int]]


def run_FMBiPartMgr(H: Netlist, part: Part):
    gainMgr = FMBiGainMgr(FMBiGainCalc, H)
    constrMgr = FMBiConstrMgr(H, 0.3)
    partMgr = FMPartMgr(H, gainMgr, constrMgr)
    partMgr.legalize(part)
    totalcostbefore = partMgr.totalcost
    partMgr.init(part)
    assert partMgr.totalcost == totalcostbefore
    partMgr.optimize(part)
    assert partMgr.totalcost <= totalcostbefore


def test_FMBiPartMgr():
    H = create_test_netlist()
    part = {v: 0 for v in H.modules}
    run_FMBiPartMgr(H, part)


def test_FMBiPartMgr2():
    H = create_drawf()
    part = {v: 0 for v in H.modules}
    H.module_fixed = {'p1'}
    run_FMBiPartMgr(H, part)


def test_FMBiPartMgr3():
    H = create_p1()
    part = [0 for _ in H.modules]
    run_FMBiPartMgr(H, part)
