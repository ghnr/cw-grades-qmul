import cw_grades
import requests
import lxml.html
import re

s = requests.Session()


def startLogin():

    while True:
        s.cookies.clear()
        url = 'https://idcheck.qmul.ac.uk/idcheck'
        user = cw_grades.main_window().input_user()
        passw = cw_grades.main_window().input_pass()
        if len(user) <= 2 or len(passw) <= 3:
            return "Empty Fail"
        try:
            cw_url = 'https://admin.sems.qmul.ac.uk/studentweb/cwdiary/'
            s.get(cw_url)
            login_data = dict(username=user, password=passw)
            response = s.post(url, data=login_data)
            page = s.get(cw_url)
        except requests.exceptions.RequestException:
            return "Connection Fail"

        html = page.text

        if response.history:
            break
        else:
            return "Fail"

    tree = lxml.html.fromstring(html)
    table = [td.text_content().strip() for td in tree.xpath('//td[@class="tablehead"] | //td[@class="tablecell"]')]

    newDict = {}
    for i in range (8):
        newDict[table[i]] = table[i+8::8]
    return newDict


def format_data(data):
    from datetime import datetime
    import pandas as pd

    def string_to_date(item):
        date_string = datetime.strptime(item, '%a %d %b %y').strftime('%d/%m/%Y')
        return date_string

    for i,due_date in enumerate(data["Due Date"]):
        if due_date == "TODAY": # If the today's date is the due date, the website displays "TODAY"
            data["Due Date"][i] = datetime.today().strftime('%d/%m/%Y')
            data["Issue Date"][i] = datetime.today().strftime('%d/%m/%Y')
        else:
            data["Due Date"][i] = string_to_date(due_date)
            data["Issue Date"][i] = string_to_date(data["Issue Date"][i])

    df_semesters = pd.DataFrame(data, columns=['Issue Date','Module'])
    df_semesters['Issue Date'] = pd.to_datetime(df_semesters['Issue Date'], dayfirst = [True], format = "%d/%m/%Y")
    df_semesters.sort_values(['Issue Date'], ascending = [True], inplace = [True])
    unique_modules = pd.unique(df_semesters.Module.ravel())

    df = pd.DataFrame(data, columns=['Due Date','Module', 'Coursework Title', 'Weight', 'Mark‡', 'Final Mark‡'])
    # Don't have to convert to pd.datetime because we don't have to sort it

    formatted_data = {}

    for i,module in enumerate(unique_modules):
        df_dummy = df[df['Module'] == module]
        dict_dummy = pd.DataFrame.to_dict(df_dummy, 'list')
        formatted_data[i] = dict_dummy
    
    for module in formatted_data:
        formatted_data[module]['Mark'] = formatted_data[module].pop('Mark‡')
        formatted_data[module]['Final Mark'] = formatted_data[module].pop('Final Mark‡')

    return formatted_data


def get_weights(module):
    if not s.cookies.items():
        return "Session Error"
    try:
        page = s.get('https://admin.sems.qmul.ac.uk/courses/coursework.php?id=' + module)
    except requests.exception.RequestException:
        return "Connection Error"
    html = page.text
    tree = lxml.html.fromstring(html)
    try:
        weight_text = tree.xpath("//div[@class='content']/section/div[@id='main']/p[contains(text(), 'constitutes')]")[0].text_content().strip()
    except IndexError:
        return "Session Error"

    return re.search('(\d+)%', weight_text).group() #finds the string of a unicode digit object
