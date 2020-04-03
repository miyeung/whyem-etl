from whyemetl.location import Position

#
# UT for contains() method
#


def test_position_in_continent(rectangular_europe):
    paris = Position(48.866683, 2.342687)
    assert rectangular_europe.contains(paris)


def test_position_not_in_continent(rectangular_europe):
    beijing = Position(39.880066, 116.388496)
    assert not rectangular_europe.contains(beijing)


def test_position_in_continent_upperleft(rectangular_europe):
    europe_upperleft = Position(58.950306, -17.455528)  # north-west of UK
    assert rectangular_europe.contains(europe_upperleft)


def test_position_in_continent_bottomright(rectangular_europe):
    europe_bottomright = Position(42.324367, 27.273977)  # South-East of Bulgaria
    assert rectangular_europe.contains(europe_bottomright)
