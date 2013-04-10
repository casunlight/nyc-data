import nose.tools as n
import addresses

def test_find_latlng():
    row = {'a': '229 PARKVILLE AVENUE\nBrooklyn, New York\n(40.63141555357741, -73.97038995525058)'}
    n.assert_equal(addresses.find_latlng_column(row), 'a')

