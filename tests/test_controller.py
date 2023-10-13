
# import os
# import unittest
# import uuid
# from settings import REQUESTS_IN_DAY
# from shedule_manager.number_request_controller import NumberRequestControler, api_request_permission, reset_number_of_trying


# class TestController(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls) -> None:
#         cls.controller = NumberRequestControler()
#         cls.temp_fixture_dir = os.path.join(".", str(uuid.uuid1()))
#         os.mkdir(cls.temp_fixture_dir)

#     def tearDown(self) -> None:
#         reset_number_of_trying()

#     @classmethod
#     def tearDownClass(cls) -> None:
#         # cls.controller.reset_number_of_trying()
#         os.rmdir(cls.temp_fixture_dir)

#     def test_controller(self):
#         for index in range(REQUESTS_IN_DAY):
#             true_result = self.controller.get_request_permission()
#             self.assertTrue(true_result)
#         false_result = self.controller.get_request_permission()
#         self.assertFalse(false_result)

#     @api_request_permission
#     def decorating_func(self):
#         return True

#     def test_request_decorator(self):
#         for index in range(REQUESTS_IN_DAY):
#             true_result = self.decorating_func()
#             self.assertTrue(true_result)
#         none_result = self.decorating_func()
#         self.assertIsNone(none_result)