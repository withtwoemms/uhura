from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


#-- DRIVER METHODS ------------------------------------->>>
def click_button(elemental, element, elm_attr, value=None):
    attr = elm_attr[0]
    attr_val = elm_attr[1]

    if element == 'select':
        xpath = '//{}[@{}="{}"]/option[@value="{}"]'.format(element, attr, attr_val, value)
        elemental.wait.until(EC.element_to_be_clickable(
            (By.XPATH, xpath))).click()
    else:
        xpath = '//{}[@{}="{}"]'.format(element, attr, attr_val)
        elemental.wait.until(EC.element_to_be_clickable(
            (By.XPATH, xpath))).click()
        

def confirm_text(elemental, text):
    elemental.wait.until(EC.text_to_be_present_in_element(
        (By.TAG_NAME, 'html'), text))


def fill_out_form(elemental, form_id, field_text):
    '''
    Relies on receiving fields in order as presented in DOM
    '''
    text_fields = get_form_text_fields(elemental, form_id)
    field_ids = [field.get_attribute('id') for field in text_fields]
    form_dict = dict(zip(field_ids, field_text))
    for field_id, text in form_dict.iteritems():
        fill_field(elemental, field_id, text)


#-- DRIVER METHOD HELPERS ------------------------------>>>
def get_form_text_fields(elemental, form_id):
    form = elemental.wait.until(EC.element_to_be_clickable(
        (By.ID, '{}'.format(form_id))))
    form_fields = form.find_elements_by_xpath('.//input')
    displayed_fields = [field for field in form_fields if field.is_displayed()]

    hidden_fields = form.find_elements_by_xpath('.//input[@type="hidden"]')
    radio_buttons = get_form_radio_buttons(elemental, form_id)
    dropdowns = get_form_dropdowns(elemental, form_id)

    only_text_fields = [field for field in displayed_fields if field 
        not in hidden_fields + radio_buttons + dropdowns]
    return only_text_fields


def get_form_radio_buttons(elemental, form_id):
    form = elemental.wait.until(EC.element_to_be_clickable(
        (By.ID, '{}'.format(form_id))))
    return form.find_elements_by_xpath('.//input[@type="radio"]')


def get_form_dropdowns(elemental, form_id):
    form = elemental.wait.until(EC.element_to_be_clickable(
        (By.ID, '{}'.format(form_id))))
    return form.find_elements_by_xpath('.//select')


def fill_field(elemental, field_id, text, overwrite=True):
    if overwrite == True:
        elemental.driver.find_element_by_id(field_id).clear()
        elemental.wait.until(EC.presence_of_element_located(
            (By.ID, '{}'.format(field_id)))).send_keys('{}'.format(text))
    else:
        elemental.wait.until(EC.presence_of_element_located(
            (By.ID, '{}'.format(field_id)))).send_keys('{}'.format(text))