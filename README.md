# uhura
an automated, lightweight tool for browser testing your site by writing yaml... ONLY YAML!

![This is a picture of Uhura operating an instrument panel.](http://www.startrek.com/legacy_media/images/200303/tos-037-uhura-gets-a-signal-fr/320x240.jpg)

### Try it out:
---
_CLI interface pending, so some rigging is necessary..._
_In the meantime here are some notes:_

* make your own yaml file like so:
```yaml
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

### Known Issues:
---
* there will be `FAIL`s in the output cause the validators broke. Fixing it now...
* it only works with Firefox
* ...and probably many more. If your see something, report it.

### Coming soon:
---
* CLI (or something) for specifying url and yaml_path
* working on the "transponder" interface for sending test results elsewhere
