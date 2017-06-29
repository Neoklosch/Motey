import unittest

from motey.models.capability import Capability


class TestCapabilityModel(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.test_dict = {'capability': 'test capability', 'capability_type': 'test capability type'}
        self.expecting_capability = Capability(capability='test capability', capability_type='test capability type')

    def test_capability_construction(self):
        resulting_capability = Capability(capability='test capability', capability_type='test capability type')
        self.assertTrue(resulting_capability.capability == 'test capability' and
                        resulting_capability.capability_type == 'test capability type')

    def test_dict_to_capability(self):
        resulting_capability = Capability.transform(data=self.test_dict)
        self.assertTrue(resulting_capability.capability == self.expecting_capability.capability and
                        resulting_capability.capability_type == self.expecting_capability.capability_type)

    def test_dict_to_none(self):
        resulting_capability = Capability.transform(data={'capability': 'test capability'})
        self.assertEqual(resulting_capability, None)

        resulting_capability = Capability.transform(data={'capability_type': 'test capability type'})
        self.assertEqual(resulting_capability, None)

    def test_capability_to_dict(self):
        resulting_dict = dict(self.expecting_capability)
        self.assertTrue(resulting_dict['capability'] == self.test_dict['capability'] and
                        resulting_dict['capability_type'] == self.test_dict['capability_type'])
