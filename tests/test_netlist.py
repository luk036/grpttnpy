
from grpttnpy.netlist import create_drawf, create_test_netlist


def test_netlist():
    H = create_test_netlist()
    assert H.number_of_modules() == 6
    assert H.number_of_nodes() == 6
    assert H.number_of_pins() == 6
    assert H.get_max_degree() == 3
    # assert not H.has_fixed_modules
    # assert H.get_module_weight_by_id(0) == 533
    assert isinstance(H.module_weight, dict)


def test_drawf():
    H = create_drawf()
    assert H.number_of_modules() == 13
    assert H.number_of_pins() == 14
    assert H.get_max_degree() == 3
    # assert not H.has_fixed_modules
    # assert H.get_module_weight_by_id(1) == 3

