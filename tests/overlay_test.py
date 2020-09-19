from overlay_all_stats import OverlayAllStats
from overlay_blank import OverlayBlank
from overlay_new import OverlayNew
from overlay_top_strip import OverlayTopStrip


def test_overlay_all_stats_instantiation():
    """ Check that OverlayAllStats can be instantiated """
    OverlayAllStats("V3")


def test_overlay_blank_instantiation():
    """ Check that OverlayBlank can be instantiated """
    OverlayBlank("V3")


def test_overlay_new_instantiation():
    """ Check that OverlayNew can be instantiated """
    OverlayNew("V3")


def test_overlay_top_strip_instantiation():
    """ Check that OverlayTopStrip can be instantiated """
    OverlayTopStrip("V3")

