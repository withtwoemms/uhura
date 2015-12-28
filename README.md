# uhura.py
an automated, lightweight tool for browser testing your site by writing yaml... ONLY YAML!

![This is a picture of Uhura operating an instrument panel.](http://www.startrek.com/legacy_media/images/200303/tos-037-uhura-gets-a-signal-fr/320x240.jpg)

### Try it out:
---
_CLI interface pending, so some rigging is necessary..._
_In the meantime here are some notes:_

* make your own yaml file like so:
```yaml
destination: 'http://localhost:2020'
test_1_and_the_name_of_test:
  url: 'http://the-page-you-want-to-test.com'
  response: 200
  title: 'Title of the page'
  actions:
    - button:
      - html_element
      - ['attribute','attribute_value(s)']
    - form:
      - 'form_id'
      - ['first text field value', 'second text field value', ...]
test_2_for_testing_the_next_page:
  ...
```
> be sure to specify the endpoint to which you would like to send your test results under the top-level `destination` key in the scenario yaml.

> there is a test server included. To run it and see the Transponder in action, open a tty and issue `node test-server.js`. You will see a set of test results populate once a TestCase is complete. Output should look something like the following:

```
Server listening on: http://localhost:2020
{ failures: { test_3_basic_application_info_can_be_input: [ 'Traceback (most recent call last):\n  File "uhura.py", line 108, in _fail\n    raise failure\nAssertionError: (1)\n\t>>> Expected: \n\t    - Dev Bootcamp | Apply Now, to equal \n\t    - Dev Bootcamp Application - Step 1. \n' ] },
  errors: { test_3_basic_application_info_can_be_input: [ 'Traceback (most recent call last):\n  File "uhura.py", line 114, in _error\n    raise error\nAssertionError: <form id="application-step-1"> element NOT FOUND!\n' ] } }
```

> there are two actions the web_elemental can perform: _clicking a button_ and _filling out a form_. These actions are indicated in the yaml with the `button` and `form` headings. Will make them more expressive in the future.

* change the url and yaml_path in `uhura.py`
```python
class TestCaseMeta(type):
	def __new__(mcs, name, bases, dict):
		dict['elemental'] = WebElemental('http://landing-page-of-your-site', 'Firefox', delay=60, 
		yaml_path='path_to_your.yaml')
		
    ...
```
* run your test with `python uhura.py -v`
> you can run tests out-of-the-box using the included `devbootcamp.com.yaml` file. Use the above command where -v is optional and stands for 'verbose' output.

### Known Issues:
---
* ~~there will be `FAIL`s in the output cause the validators broke. Fixing it now...~~
* Error handling absent if `destination` invalid
* it only works with Firefox
* ...and probably many more. If your see something, report it.

### Coming soon:
---
* working on the "transponder" interface for sending test results elsewhere (working on this now...)
* CLI (or something) for specifying url and yaml_path
