import logging
import requests
import unittest
import sys
import types

from collections import defaultdict
from core import click_button, fill_out_form
from requests.exceptions import ConnectionError
from selenium.common.exceptions import TimeoutException
from transponder import Transponder
from utils import ordered_load, retry
from web_elemental import WebElemental


class MetaTestCase(type):
	def __new__(mcs, name, bases, dict):
		dict['elemental'] = WebElemental('http://devbootcamp.com/', 'Firefox', delay=30, yaml_path='devbootcamp.com.yaml')

		# Methods and functions for asserting & driving
		#-------------------------------------------------->>>
		asserts = { # page properties
			'title': dict['elemental'].title,
			'response': dict['elemental'].page_status
		}
		drive = { # driver actions
			'form': fill_out_form,
			'button': click_button
		}
		#-------------------------------------------------->>>

		def drive_browser(self, actions):
			try:
				for action in actions:
					key = action.iterkeys().next()
					args = action.itervalues().next()
					if len(args) > 2:
						drive[key](dict['elemental'], args[0], args[1], args[2])
					else:
						drive[key](dict['elemental'], args[0], args[1])
			except TimeoutException as e:
				if key == 'button':
					msg = '<{} {}="{}"> element NOT FOUND!'.format(args[0], args[1])
				elif key == 'form':
					msg = '<form id="{}"> element NOT FOUND!'.format(args[0])
				else:
					msg = '*** Something strange has occurred ***'
				self._error(unittest.TestCase.failureException(msg))
				self._num_expectations += 1
		dict['drive_browser'] = drive_browser

		def make_assertions(self, assertions, config):
			for assertion in assertions:
				this = asserts[assertion](dict['elemental'].current_url())
				that = config[assertion]
				self.expect_equal(this, that)
		dict['make_assertions'] = make_assertions

		def gen_test(assertions, actions, config):
			def test(self):
				self.make_assertions(assertions, config)
				self.drive_browser(actions)
			return test

		# Populate namespace of new class with test methods
		#-------------------------------------------------->>>
		for tname, config in dict['elemental'].scenario.iteritems():
			if 'test' in tname:
				assertions = [assertion for assertion in config.keys() if assertion in asserts.keys()]
				actions = config['actions']
				dict[tname] = gen_test(assertions, actions, config)
		dict['_results'] = []
		dict['destination'] = dict['elemental'].scenario['destination']
		#-------------------------------------------------->>>

		print('-' * 70 + '\n')
		return type.__new__(mcs, name, bases, dict)


class TestCase(unittest.TestCase):
	__metaclass__ = MetaTestCase

	@classmethod
	def tearDownClass(cls):
		results = TestCase._results.pop()

		report = {}
		report['errors'] = defaultdict(list)
		report['failures'] = defaultdict(list)

		for test, error in results.errors:
			report['errors'][test._testMethodName].append(error)
		for test, failure in results.failures:
			report['failures'][test._testMethodName].append(failure)

		cls.elemental.driver.close()
		return Transponder(report, TestCase.destination)
		# return Transponder(report, 'http://localhost:2020')

	def run(self, result=None):
		self._results.append(result)
		self._result = result
		self._num_expectations = 0
		super(TestCase, self).run(result)

	def _fail(self, failure):
		try:
			raise failure
		except failure.__class__:
			self._result.addFailure(self, sys.exc_info())

	def _error(self, error):
		try:
			raise error
		except error.__class__:
			self._result.addError(self, sys.exc_info())

	def expect_equal(self, this, that, msg=''):
		if this != that:
			msg = '({})\n\t>>> Expected: \n\t    - {}, to equal \n\t    - {}. '.format(self._num_expectations, this, that) #+ msg
			self._fail(self.failureException(msg))
		self._num_expectations += 1



if __name__ == "__main__":
    unittest.main(catchbreak=True) # actually an instance of the unittest.TestProgram
