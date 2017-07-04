from __future__ import absolute_import
from __future__ import print_function
import pytest
from aether.replica import *


class TestReplicaNetworking:
        def test_networking_function(self):
            assert (networking_function() == 1)

class TestReplicaMain:
        def test_main_function(self):
            assert (main_function() == 1)
