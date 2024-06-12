
from apps import app, auth, render_template, request, redirect, jsonify
from models.admin import Admin
from models.chapter import Chapter
from models.church import Church
from models.devotion import Devotion
from models.group import Group
from models.member import Member
from models.report import Report
# from models.schedule import Schedule
from schedule import Schedule
from parsing import Parser
from utils import BOOKNAMES_FIX_TYPO
from datetime import datetime
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import hashlib
import joblib
import base64
import emoji
import re

# DASHBOARD
@app.route('/weekly-graph', methods=['GET'])
@auth
def get_weekly_data(*args, **kwargs):
    id_group = request.args.get('id_group', None)
    report = Report()
    result_graph = report.get_data_graph1(id_group).get('data')

    # dates = []
    # values = []

    # for data in result_graph:
    #     dates.append(data.get('report_date'))
    #     values.append(data.get('num_members'))

    # # Convert dates to datetime objects and then to ordinal format
    # date_objects = [datetime.strptime(date, "%Y-%m-%d") for date in dates]
    # date_ordinal = [mdates.date2num(date) for date in date_objects]

    # # Fit a linear trendline
    # coefficients = np.polyfit(date_ordinal, values, 1)
    # trendline = np.poly1d(coefficients)

    # # Generate trendline values at each date point
    # trendline_values = list(trendline(date_ordinal))

    response = {'status': True, 
                'msg': 'Success', 
                'data': result_graph, 
                # 'trendline_values': trendline_values
                }

    return response

@app.route('/monthly-graph', methods=['GET'])
@auth
def get_monthly_data(*args, **kwargs):
    id_group = request.args.get('id_group', None)
    report = Report()
    result_graph = report.get_data_monthly(id_group).get('data')

    # dates = []
    # values = []

    # for data in result_graph:
    #     dates.append(data.get('report_date'))
    #     values.append(data.get('num_members'))

    # # Convert dates to datetime objects and then to ordinal format
    # date_objects = [datetime.strptime(date, "%Y-%m-%d") for date in dates]
    # date_ordinal = [mdates.date2num(date) for date in date_objects]

    # # Fit a linear trendline
    # coefficients = np.polyfit(date_ordinal, values, 1)
    # trendline = np.poly1d(coefficients)

    # # Generate trendline values at each date point
    # trendline_values = list(trendline(date_ordinal))

    response = {'status': True, 
                'msg': 'Success', 
                'data': result_graph, 
                # 'trendline_values': trendline_values
                }
    
    return response

@app.route('/lifetime-graph', methods=['GET'])
@auth
def get_lifetime_data(*args, **kwargs):
    id_group = request.args.get('id_group', None)
    report = Report()
    result_graph = report.get_data_lifetime(id_group).get('data')

    # dates = []
    # values = []

    # for data in result_graph:
    #     dates.append(data.get('report_date'))
    #     values.append(data.get('num_members'))

    # # Convert dates to datetime objects and then to ordinal format
    # date_objects = [datetime.strptime(date, "%Y-%m-%d") for date in dates]
    # date_ordinal = [mdates.date2num(date) for date in date_objects]

    # # Fit a linear trendline
    # coefficients = np.polyfit(date_ordinal, values, 1)
    # trendline = np.poly1d(coefficients)

    # # Generate trendline values at each date point
    # trendline_values = list(trendline(date_ordinal))

    response = {'status': True, 
                'msg': 'Success', 
                'data': result_graph, 
                # 'trendline_values': trendline_values
                }
    
    return response

@app.route('/graphs', methods=['GET'])
@auth
def get_graphs_data(*args, **kwargs):
    id_group = request.args.get('id_group', None)
    report = Report()

    ## TODAY'S SCHEDULE ##
    schedule = Schedule()
    result_schedule = schedule.get_todays_schedule(id_group).get('data')
    ## TODAY'S SCHEDULE ##

    ## NUMBER OF MEMBERS IN A CERTAIN GROUP ##
    member = Member()
    result_number_of_members = member.count_group_members(id_group).get('data')
    ## NUMBER OF MEMBERS IN A CERTAIN GROUP ##

    ## GROUP READING PERCENTAGE ##
    result_percentage = report.get_reading_percentage(id_group).get('data')
    ## GROUP READING PERCENTAGE ##

    ## LINE-GRAPH: NUMBER OF MEMBERS IN A CERTAIN GROUP WHO HAS REPORTESD IN THE LAST 7 DAYS ##
    result_graph = report.get_data_graph1(id_group).get('data')
    # dates = []
    # values = []

    # for data in result_graph:
    #     dates.append(data.get('report_date'))
    #     values.append(data.get('num_members'))

    # # Convert dates to datetime objects and then to ordinal format
    # date_objects = [datetime.strptime(date, "%Y-%m-%d") for date in dates]
    # date_ordinal = [mdates.date2num(date) for date in date_objects]

    # # Fit a linear trendline
    # coefficients = np.polyfit(date_ordinal, values, 1)
    # trendline = np.poly1d(coefficients)

    # # Generate trendline values at each date point
    # trendline_values = list(trendline(date_ordinal))
    ## LINE-GRAPH: NUMBER OF MEMBERS IN A CERTAIN GROUP WHO HAS REPORTESD IN THE LAST 7 DAYS ##

    ## MEMBER SEGMENTATION ##
    result_segmentation = report.get_members_segmentation(id_group).get('data')
    ## MEMBER SEGMENTATION ##

    ## LIST OF MEMBERS WHO HAS NOT REPORTED FOR MORE THAN 7 DAYS ##
    result_member_list = report.get_members_not_reporting_more_than_7days(id_group).get('data')
    ## LIST OF MEMBERS WHO HAS NOT REPORTED FOR MORE THAN 7 DAYS ##

    
    
    response = {'status': True, 'msg': 'Success', 'data': 
                {
                    'today_schedule': result_schedule, 
                    'number_of_members': result_number_of_members,
                    'reading_percentage': result_percentage,
                    'graph': result_graph, 
                    'segmentation': result_segmentation,
                    'list_of_members': result_member_list,
                    # 'trendline_values': trendline_values
                    }
                }
    return response

# AUTORECAP
@app.route('/auto-recap', methods=['GET'])
@auth
def auto_recap(*args, **kwargs):
    report = Report()
    id_group = request.args.get('id_group', None)
    date = request.args.get('input_date')
    book_name = request.args.get('book_name')
    number = int(request.args.get('chapter_number'))
    emoji_opt = request.args.get('emoji_option')

    group = Group()
    group_name = group.get_group_name(id_group)['data']

    report_dates = report.get_report_dates(id_group)
    if date not in report_dates['data']:
        return {'status': False,'msg': 'There is no report with this date'}

    chapter = Chapter()
    id_chapter = chapter.get_chapter_id(book_name, number).get('data')[0]['id_chapter']

    member = Member()
    all_members = member.get_members_by_group(id_group)
    formatted_report = []
    formatted_report.append(f"*Update {group_name}*")
    formatted_report.append(f"{book_name.title()} {number}")
    formatted_report.append("")
    for index, temp_member in enumerate(all_members['data'], start=1):
        member_report = report.get_member_last_chapter(temp_member['id_member'], date).get('data')
        if member_report:
            if int(member_report['id_chapter']) == int(id_chapter):
                formatted_report.append(f"{index}. {temp_member['member_name']}: {emoji.emojize(str(emoji_opt))}")
            else:
                formatted_report.append(f"{index}. {temp_member['member_name']}: {member_report['chapter_name'].title()}")
        else:
            formatted_report.append(f"{index}. {temp_member['member_name']}")

    response = {'status': True, 'msg': 'Success', 'data': {'recap': formatted_report}}
    return response

@app.route('/set-chapter-recap', methods=['POST'])
@auth
def set_chapter_recap(*args, **kwargs):
    id_group = request.form.get('id_group', None)
    date = request.form.get('input_date')
    formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
    schedule = Schedule()
    recap_schedule = schedule.get_certain_date_chapter(id_group, formatted_date).get('data')
    if recap_schedule:
        response = {'status': True, 'msg': 'Success', 'data': {'schedule': recap_schedule}}
    else:
        yesterday_date = formatted_date[:-1]+str(int(formatted_date[-1])-1)
        temp_sch = schedule.get_certain_date_chapter(id_group, yesterday_date).get('data')
        if temp_sch:
            response = {'status': True, 'msg': 'Success', 'data': {'schedule': temp_sch}}
        else:
            response = {'status': False,'msg': 'There is no schedule'}
    return response

# UPLOAD FILE
def replace_invisible_chars(string):
    pattern = r'[\u200B-\u200F\u2028-\u202F\u205F-\u2064\uFEFF]'
    new_string = re.sub(pattern, ' ', string)
    return new_string

def parsing_text(string):
    parser = Parser()
    output = parser.run(string)
    return output

# ADMIN
@app.route('/add-data-admin', methods=['POST'])
@auth
def add_data_admin(*args, **kwargs):
    admin = Admin()
    group = Group()

    masterAdmin = admin.get_all_usernames().get('data')

    ajaxData = request.json

    admin_name = ajaxData.get('admin_name')
    username = ajaxData.get('username')
    password = ajaxData.get('password')
    phone = ajaxData.get('phone')
    groups = ajaxData.get('groupData')

    filtered_groups = []
    for group in groups:
        if group.get('group_id') != '1' and group.get('group_id') != '' and group.get('group_id') != 'Choose Group':
            filtered_groups.append(group)

    if filtered_groups:
        if username not in masterAdmin:
            response = admin.insert(admin_name, username, password, phone)
            if response.get('status'):
                id_admin = admin.get_last_index().get('data')
                for row in filtered_groups:
                    response = admin.insert_details(id_admin, int(row['group_id']))
            else:
                response = {'status': False,'msg': 'Failed to add admin'}
        else:
            response = {'status': False,'msg': 'Username is already taken!'}
    else:
        response = {'status': False,'msg': 'Please choose at least one group'}

    return response

@app.route('/load-data-admin', methods=['GET'])
@auth
def load_data_admin(*args, **kwargs):
    admin = Admin()
    response = admin.read()
    return response

@app.route('/update-data-admin', methods=['POST'])
@auth
def update_data_admin(*args, **kwargs):
    admin = Admin()
    masterAdmin = admin.get_all_usernames().get('data')

    ajaxData = request.json

    id_admin = ajaxData.get('id_admin_edit')
    admin_name = ajaxData.get('admin_name_edit')
    username = ajaxData.get('username_edit')
    phone = ajaxData.get('phone_edit')
    groups = ajaxData.get('groupData_edit')
    old_data = ajaxData.get('old_details_data')

    current_username = admin.get_username_by_id(id_admin).get('data')[0]
    masterAdmin.remove(current_username)
    
    new_id_details = []
    for row in groups:
        if row['col0'] == 'new':
            if row['col1'] == 'Choose Group':
                continue
            else:
                # insert new admin details
                admin.insert_details(id_admin, int(row['col1']))
        else:
            new_id_details.append(row['col0'])

    for id_detail in old_data:
        if id_detail in new_id_details:
            # update admin details
            for row in groups:
                if row['col0'] == id_detail:
                    admin.update_details(id_detail, int(row['col1']))
        else:
            # delete admin details
            admin.delete_details(id_detail)

    # id_group = int(request.form['id_group_edit'])
    admin = Admin()
    if username not in masterAdmin:
        response = admin.update(id_admin, admin_name, username, phone)
    else:
        response = {'status': False,'msg': 'Username is already taken!'}
    return response

@app.route('/reset-password-admin', methods=['POST'])
@auth
def reset_password_admin(*args, **kwargs):
    id_admin = request.form['id_admin_reset']
    password = hashlib.md5(request.form['password_reset'].encode()).hexdigest()
    admin = Admin()
    response = admin.reset_password(id_admin, password)
    if response.get('status'):
        return redirect('/admin')
    return response

@app.route('/delete-data-admin', methods=['GET'])
@auth
def delete_data_admin(*args, **kwargs):
    id_admin = request.args.get('id_admin')
    admin = Admin()

    num_of_current_admin = admin.count_current_admin().get('data')
    if num_of_current_admin == 1:
        response = {'status': False,'msg': 'Cannot delete the last admin'}
    else:
        response = admin.delete(id_admin)
    return response

#CHAPTER
@app.route('/load-data-booknames', methods=['GET'])
@auth
def load_data_booknames(*args, **kwargs):
    chapter = Chapter()
    response = chapter.get_booknames()
    return response

@app.route('/load-data-chapters', methods=['GET'])
@auth
def load_data_chapters(*args, **kwargs):
    book_name = request.args.get('book_name')
    chapter = Chapter()
    response = chapter.get_chapters(book_name)
    return response

@app.route('/get-master-chapter', methods=['GET'])
@auth
def get_master_chapter(*args, **kwargs):
    chapter = Chapter()
    response = chapter.get_master_chapter()
    return jsonify(response)

# CHURCH
@app.route('/add-data-church', methods=['POST'])
@auth
def add_data_church(*args, **kwargs):
    church = Church()
    masterChurch = church.get_all_names().get('data')

    ajaxData = request.json
    church_name = ajaxData.get('church_name')
    phone = ajaxData.get('phone') 
    address = ajaxData.get('address')
    
    if church_name not in masterChurch:
        response = church.insert(church_name, phone, address)
    else:
        response = {'status': False,'msg': 'Church name is already taken!'}

    return response

@app.route('/load-data-church', methods=['GET'])
@auth
def load_data_church(*args, **kwargs):
    church = Church()
    response = church.read()
    return response

@app.route('/update-data-church', methods=['POST'])
@auth
def update_data_church(*args, **kwargs):
    church = Church()
    masterChurch = church.get_all_names().get('data')
    
    ajaxData = request.json

    id_church = ajaxData.get('id_church_edit')
    church_name = ajaxData.get('church_name_edit')
    phone = ajaxData.get('phone_edit')
    address = ajaxData.get('address_edit')

    current_name = church.get_church_name_by_id(id_church).get('data')[0]
    masterChurch.remove(current_name)
    
    if church_name not in masterChurch:
        response = church.update(id_church, church_name, phone, address)
    else:
        response = {'status': False,'msg': 'Church name is already taken!'}

    return response

@app.route('/delete-data-church', methods=['GET'])
@auth
def delete_data_church(*args, **kwargs):
    id_church = request.args.get('id_church')
    church = Church()
    response = church.delete(id_church)
    return response

# DEVOTION
@app.route('/add-data-devotion', methods=['POST'])
@auth
def add_data_devotion(*args, **kwargs):
    title = request.form['title']
    content = request.form['content']
    book_name = request.form['book_name']
    number = request.form['chapter_number']
   
    chapter = Chapter()
    id_chapter = chapter.get_chapter_id(book_name, number).get('data')[0]['id_chapter']

    devotion = Devotion() 
    response = devotion.insert(title, content, id_chapter)
    if response.get('status'):
        return redirect('/devotion')
    return response

@app.route('/load-data-devotion', methods=['GET'])
@auth
def load_data_devotion(*args, **kwargs):
    devotion = Devotion()
    response = devotion.read()
    return response

@app.route('/update-data-devotion', methods=['POST'])
@auth
def update_data_devotion(*args, **kwargs):
    id_devotion = request.form['id_devotion_edit']
    title = request.form['title_edit']
    content = request.form['content_edit']
    book_name = request.form['book_name_edit']
    number = request.form['chapter_number_edit']
    
    chapter = Chapter()
    id_chapter = chapter.get_chapter_id(book_name, number).get('data')[0]['id_chapter']
    
    devotion = Devotion()
    response = devotion.update(id_devotion, title, content, int(id_chapter))
    if response.get('status'):
        return redirect('/devotion')
    return response

@app.route('/delete-data-devotion', methods=['GET'])
@auth
def delete_data_devotion(*args, **kwargs):
    id_devotion = request.args.get('id_devotion')
    devotion = Devotion()
    response = devotion.delete(id_devotion)

    return response

@app.route('/copy-data-devotion', methods=['GET'])
@auth
def copy_data_devotion(*args, **kwargs):
    id_devotion = request.args.get('id_devotion')
    devotion = Devotion()
    response_data = []

    devotion_data = devotion.get_devotion_by_id(id_devotion).get('data')[0]
    response_data = f"{devotion_data['title']}\n{devotion_data['chapter_name'].title()}\n\n{devotion_data['content']}"
    # response_data.append(devotion_data['title'])
    # response_data.append(devotion_data['chapter_name'])
    # response_data.append('')
    # response_data.append(devotion_data['content'])
    response = {'status': True, 'data': response_data}
    return response

# GROUP
@app.route('/add-data-group', methods=['POST'])
@auth
def add_data_group(*args, **kwargs):
    group = Group()
    masterGroup = group.get_all_names().get('data')

    ajaxData = request.json
    group_name = ajaxData.get('group_name')
    id_church = ajaxData.get('id_church')
    start_date = ajaxData.get('start_date')
    num_of_chapter = int(ajaxData.get('num_of_chapter'))
    status = int(ajaxData.get('status'))

    schedule = Schedule()
    generate_schedule = schedule.generate_schedule(start_date, schedule.BIBLECHAPTERSIDX, num_of_chapter)
    target_date =  generate_schedule[-1]['tanggal']

    if group_name not in masterGroup:
        response = group.insert(group_name, id_church, start_date, target_date, num_of_chapter, status)

        id_group = group.get_group_last_id().get('data')

        for data in generate_schedule:
            schedule.insert(id_group, data['tanggal'])
            
            id_schedule = schedule.get_schedule_last_id().get('data')
            chapters_schedule = data['bacaan'].split(', ')
            for chapter in chapters_schedule:
                schedule.insert_details(id_schedule, chapter)
    else:
        response = {'status': False,'msg': 'Group name is already taken!'}
    return response

@app.route('/load-data-group', methods=['GET'])
@auth
def load_data_group(*args, **kwargs):
    group = Group()
    response = group.read()
    return response

@app.route('/update-data-group', methods=['POST'])
@auth
def update_data_group(*args, **kwargs):
    group = Group()
    masterGroup = group.get_all_names().get('data')

    ajaxData = request.json

    id_group = ajaxData.get('id_group_edit')
    group_name = ajaxData.get('group_name_edit')
    id_church = ajaxData.get('id_church_edit')
    status = int(ajaxData.get('status_edit'))

    current_name = group.get_group_name_by_id(id_group).get('data')[0]
    masterGroup.remove(current_name)

    if group_name not in masterGroup:
        response = group.update(id_group, group_name, id_church, status)
    else:
        response = {'status': False,'msg': 'Group name is already taken!'}
    
    return response

@app.route('/delete-data-group', methods=['GET'])
@auth
def delete_data_group(*args, **kwargs):
    id_group = request.args.get('id_group')
   
    group = Group()
    response = group.delete(id_group)
    return response

@app.route('/get-master-group', methods=['GET'])
@auth
def get_master_group(*args, **kwargs):
    group = Group()
    response = group.get_master_group()
    return jsonify(response)

# MEMBER
@app.route('/upload-member', methods=['POST'])
@auth
def upload_member(*args, **kwargs):
    encoded_string = request.form.get("base64_data")

    id_group = request.form.get("id_group")
    id_group = int(id_group)

    if id_group != 0:
        header, base64_data = encoded_string.split(',', 1)
        decoded_data = base64.b64decode(base64_data)
        decoded_text = decoded_data.decode('utf-8')
        decoded_text = replace_invisible_chars(decoded_text)
        returnData = []
        response = {
                    'status': True,
                    'msg': 'Success',
                    'data': returnData
                }
        
        for line in decoded_text.split('\n'):
            if line.startswith('['):
                pattern = re.compile(r'\[\d{2}/\d{2}/\d{2} \d{2}\.\d{2}\.\d{2}\]\s*([^:]+):')
                match = pattern.search(line)
                if match:
                    name = match.group(1).strip()
                    if name not in returnData and not name.startswith('+62'):
                        returnData.append(name)
    else:
        response = {
                    'status': False,
                    'msg': 'Please Input Group!',
                    'data': []
                }
    return response

@app.route('/upload-member-to-db', methods=['POST'])
@auth
def upload_member_to_db(*args, **kwargs):
    member = Member()
    
    masterMember = member.get_all_names().get('data')

    ajax_data = request.json.get('data')
    id_group = request.json.get('id_group')

    for row in ajax_data:
        name = row.get('column1')
        if name in masterMember:
            continue
        else:
            member.insert(name, '', int(id_group), 1)
    
    response = {'status': True, 'msg': 'Success'}
    return response

@app.route('/add-data-member', methods=['POST'])
@auth
def add_data_member(*args, **kwargs):
    member = Member()

    masterMember = member.get_all_names().get('data')

    ajaxData = request.json

    member_name = ajaxData.get('member_name')
    phone = ''
    id_group = int(ajaxData.get('id_group'))
    status = ajaxData.get('status')
    
    if member_name in masterMember:
        response = {
                   'status': False,
                   'msg': 'Member Name is Taken!',
                }
    else:
        response = member.insert(member_name, phone, id_group, status)

    return response

@app.route('/load-data-member', methods=['GET'])
@auth
def load_data_member(*args, **kwargs):
    member = Member()
    response = member.read()
    return response

@app.route('/load-member-by-group', methods=['GET'])
@auth
def load_member_by_group(*args, **kwargs):
    member = Member()
    id_group = request.args.get('id_group', None)
    response = member.get_members_by_group(id_group)
    return response

@app.route('/update-data-member', methods=['POST'])
@auth
def update_data_member(*args, **kwargs):
    member = Member()
    masterMember = member.get_all_names().get('data')

    ajaxData = request.json

    id_member = ajaxData.get('id_member_edit')
    member_name = ajaxData.get('member_name_edit')
    # phone = request.form['phone_edit']
    phone = ''
    id_group = int(ajaxData.get('id_group_edit'))
    status = int(ajaxData.get('status_edit'))

    current_name = member.get_member_name_by_id(id_member).get('data')[0]
    masterMember.remove(current_name)

    if member_name in masterMember:
        response = {
                   'status': False,
                   'msg': 'Member Name is Taken!',
                }
    else:
        response = member.update(id_member, member_name, phone, id_group, status)
    return response

@app.route('/delete-data-member', methods=['GET'])
@auth
def delete_data_member(*args, **kwargs):
    id_member = request.args.get('id_member')
    member = Member()
    response = member.delete(id_member)
    return response

# REPORT
@app.route('/upload-file', methods=['POST'])
@auth
def upload_file(*args, **kwargs):
    encoded_string = request.form.get("base64_data")
    date = request.form.get("date")

    if date:
        # Parse the original date string
        original_date = datetime.strptime(date, "%Y-%m-%d")
        # Format the date as "DD/MM/YY"
        converted_date_string = original_date.strftime("%d/%m/%y")
        date = converted_date_string
        header, base64_data = encoded_string.split(',', 1)
        decoded_data = base64.b64decode(base64_data)
        decoded_text = decoded_data.decode('utf-8')
        decoded_text = replace_invisible_chars(decoded_text)
        result = []
        returnData = []
        response = {
                    'status': True,
                    'msg': 'Success',
                    'data': returnData
                }
        
        for line in decoded_text.split('\n'):
            if line.startswith('['):
                result.append(line)
            else:
                previous = result.pop(-1)
                result.append(previous + ' ' + line)
        parser = Parser()

        for line in result:
            _line = line.replace('\r', '')
            if date in _line:
                tmp = _line.split(':')
                report_chat = tmp[1].lstrip().rstrip()
                tmp2 = tmp[0].split(']')
                name = tmp2[1].lstrip().rstrip()

                loaded_model = joblib.load('ML_model/random_forest_model.joblib')
                loaded_vectorizer = joblib.load('ML_model/vectorizer.joblib')
                loaded_label_encoder = joblib.load('ML_model/label_encoder.joblib')

                X_test_transformed = loaded_vectorizer.transform(pd.Series([report_chat]))
                predictions_encoded = loaded_model.predict(X_test_transformed)
                predictions = loaded_label_encoder.inverse_transform(predictions_encoded)

                if predictions == ['report']:
                    parsed_data = parser.run(report_chat)
                    returnData.append({'name': name, 'report_chat': report_chat, 'parsed':parsed_data})
    else:
        response = {
                    'status': False,
                    'msg': 'Please Input Date!',
                    'data': []
                }
    return response

@app.route('/upload-to-db', methods=['POST'])
@auth
def upload_to_db(*args, **kwargs):
    member = Member()
    masterName = dict()
    
    report = Report()
    masterMember = member.read().get('data')
    for row in masterMember:
        masterName[row.get('id_member')] = row.get('member_name')

    chapter = Chapter()
    masterChapter = chapter.get_all_chapters().get('data')

    """{'status': True, 'msg': 'Success', 
    'data': [{'id_member': 4, 'member_name': 'Cath', 'phone': '0812345', 'id_church': 1, 'church_name': 'GRII Pusat', 'id_group': 3, 'group_name': 'Kelompok 3', 'status': 0}, 
    {'id_member': 7, 'member_name': 'anonymous', 'phone': '-', 'id_church': 7, 'church_name': 'anonymous', 'id_group': 8, 'group_name': 'anonymous', 'status': 1}]}"""

    """'data': [{'column1': '~ Tejo Jayadi', 'column2': 'Wahyu 19-20 done Wahyu 21-22 done', 'column3': 'wahyu 19, wahyu 21'}, 
    {'column1': 'Lenny Pandjidharma', 'column2': 'Lenny Pandjidharma keluar', 'column3': 'aa'}, 
    {'column1': 'Dicky Andrian', 'column2': 'Dicky Andrian keluar', 'column3': ''}, 
    {'column1': '~ Jeffry', 'column2': '~ Jeffry keluar', 'column3': ''}]}"""
    
    ajax_data = request.json.get('data')
    date = request.json.get('date')

    parser = Parser()

    for row in ajax_data:
        name = row.get('column1')
        id_member = 1
        report_chat = row.get('column2')
        parsed = row.get('column3').split(', ')

        for i, parsed_data in enumerate(parsed):
            tmp_list = parsed_data.split(' ')
            tmp_bookname = ' '.join(tmp_list[:-1])
            fixed_bookname = parser.jaro_function(tmp_bookname, BOOKNAMES_FIX_TYPO)
            tmp_chapter = tmp_list[-1]

            fixed_parsed_data = fixed_bookname + ' ' + tmp_chapter
            fixed_parsed_data.replace('  ', ' ')
            parsed[i] = int(masterChapter[fixed_parsed_data])

        for key, val in masterName.items():
            if val == name:
                id_member = key
        report.insert_many({'id_member': id_member, 'date': date,'report': report_chat, 'parsed': parsed})
    
    response = {'status': True, 'msg': 'Success'}
    return response

@app.route('/add-data-report', methods=['POST'])
@auth
def add_data_report(*args, **kwargs):
    report = Report()
    chapter = Chapter()

    ajaxData = request.json

    date = ajaxData.get('date')
    id_member = ajaxData.get('id_member')
    # report_chat = ajaxData.get('report')
    report_chat = ''
    chapters = ajaxData.get('chapterData')

    response = report.insert(date, id_member, report_chat)

    if response.get('status'):
        id_report = report.get_last_index().get('data')
        for row in chapters:
            if row['col1'] == 'Book' or row['col2'] == 'Number':
                continue
            else:
                ## add report details
                id_chapter = chapter.get_chapter_id(row['col1'], int(row['col2'])).get('data')[0]['id_chapter']
                response2 = report.insert_details(id_report, id_chapter)

    if response2.get('status'):
        return redirect('/report')
    return response2



@app.route('/load-data-report', methods=['GET'])
@auth
def load_data_report(*args, **kwargs):
    report = Report()
    response = report.read()
    return response

@app.route('/update-data-report', methods=['POST'])
@auth
def update_data_report(*args, **kwargs):
    report = Report()
    chapter = Chapter()

    ajaxData = request.json

    id_report = int(ajaxData.get('id_report'))
    date = ajaxData.get('date')
    id_member = ajaxData.get('id_member')
    report_chat = ajaxData.get('report')
    chapters = ajaxData.get('chapterData')
    old_data = ajaxData.get('old_details_data')

    new_id_details = []
    for row in chapters:
        if row['col0'] == 'new':
            if row['col1'] == 'Book' or row['col2'] == 'Number':
                continue
            else:
                ## add report details
                id_chapter = chapter.get_chapter_id(row['col1'], int(row['col2'])).get('data')[0]['id_chapter']
                report.insert_details(id_report, id_chapter)
        else:
            new_id_details.append(row['col0'])

    for id_detail in old_data:
        if id_detail in new_id_details:
            ## update report details
            for row in chapters:
                if row['col0'] == id_detail:
                    id_chapter = chapter.get_chapter_id(row['col1'], int(row['col2'])).get('data')[0]['id_chapter']
                    report.update_details(id_detail, id_chapter)
        else:
            ## delete report details
            report.delete_details(id_detail)
        
    report = Report()
    response = report.update(id_report, date, id_member, report_chat)
    if response.get('status'):
        return redirect('/report')
    return response

@app.route('/delete-data-report', methods=['GET'])
@auth
def delete_data_report(*args, **kwargs):
    id_report = request.args.get('id_report')
    report = Report()
    response = report.delete(id_report)
    return response