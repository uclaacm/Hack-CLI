import unittest
from Event import Event
from Showcase import Showcase
from Settings import Settings
import Global
import json

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.modules = {
    		"event" : Event,
    		"showcase" : Showcase,
    		"cli" : Settings
    	}
        self.event_module = self.modules["event"]("list", [])
        self.showcase_module = self.modules["showcase"]("list", [])

    def test_event_listing(self):
        li = self.event_module.list()
        if li is None:
            return
        event_data = li[0]
        # we should get back the date, id and title
        self.assertTrue("date" in event_data.keys())
        self.assertTrue("id" in event_data.keys())
        self.assertTrue("title" in event_data.keys())


    def test_event_details(self):
        pass

    def test_event_add(self):
        pass

    def test_event_update(self):
        pass

    def test_event_delete(self):
        pass

    def test_showcase_listing(self):
        pass

    def test_showcase_details(self):
        pass

    def test_showcase_add(self):
        pass

    def test_showcase_update(self):
        pass

    def test_showcase_delete(self):
        pass




if __name__ == '__main__':
    unittest.main()
