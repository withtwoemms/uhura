import requests
import unittest
import sys
import types

from core import click_button, fill_out_form
from requests.exceptions import ConnectionError
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
from utils import ordered_load, retry
from web_elemental import WebElemental


class TestCaseMeta(type):
	def __new__(mcs, name, bases, dict):
		dict['elemental'] = WebElemental('http://devbootcamp.com/', 'Firefox', delay=60, yaml_path='devbootcamp.com.yaml')

		# Methods and functions for asserting & driving
		#-------------------------------------------------->>>
		asserts = { # page properties
			'title': dict['elemental'].get_page_title,
			'response': dict['elemental'].page_status
		}
		drive = { # driver actions
			'form': fill_out_form,
			'button': click_button
		}
		#-------------------------------------------------->>>

		def drive_browser(self, actions):
			for action in actions:
				key = action.iterkeys().next()
				args = action.itervalues().next()
				if len(args) > 2:
					drive[key](dict['elemental'], args[0], args[1], args[2])
				else:
					drive[key](dict['elemental'], args[0], args[1])
		dict['drive_browser'] = drive_browser

		def gen_test(assertions, actions):
			this = asserts[assertion](dict['elemental'].current_url())
			that = config[assertion]
			def test(self):
				self.expect_equal(this, that)
				self.drive_browser(actions)
			return test
			
		# Populate namespace of new class with test methods
		#-------------------------------------------------->>>
		for tname, config in dict['elemental'].scenario.items():
			assertions = [assertion for assertion in config.keys() if assertion in asserts.keys()]
			for assertion in assertions:
				dict[tname] = gen_test(assertions, config['actions'])

		print('-' * 70 + '\n')
		try:
			return type.__new__(mcs, name, bases, dict)
		except NoSuchWindowException as e:
			print(e)
			return type.__new__(type, 'TestCaseMeta', (), {})


class TestCase(unittest.TestCase):
	__metaclass__ = TestCaseMeta


	@classmethod
	def tearDownClass(cls):
		cls.elemental.driver.close()
		# pass

	def run(self, result=None):
		self._result = result
		self._num_expectations = 0
		super(TestCase, self).run(result)

	def _fail(self, failure):
		try:
			raise failure
		except failure.__class__:
			self._result.addFailure(self, sys.exc_info())

	def expect_equal(self, this, that, msg=''):
		if this != that:
			msg = '({})\n\t>>> Expected: \n\t    - {}, to equal \n\t    - {}. '.format(self._num_expectations, this, that) #+ msg
			self._fail(self.failureException(msg))
		self._num_expectations += 1

	

if __name__ == "__main__":
    unittest.main() # actually an instance of the unittest.TestProgram