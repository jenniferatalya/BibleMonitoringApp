from datetime import datetime, timedelta
from utils import BIBLECHAPTERSIDX
from models import connection, text

class Schedule:
    def __init__(self):
        self.BIBLECHAPTERSIDX = BIBLECHAPTERSIDX

    def is_sunday(self, date):
        return date.weekday() == 6

    def generate_schedule(self, start_date, bible_chapters, chapters_per_day):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        schedule = []
        current_date = start_date
        chapter_index = 0
        while chapter_index < len(bible_chapters):
            if self.is_sunday(current_date):
                current_date += timedelta(days=1)
                continue
            chapters = [str(ch) for ch in bible_chapters[chapter_index:chapter_index+chapters_per_day]]
            reading = ', '.join(chapters)
            schedule.append({'tanggal': current_date.strftime('%Y-%m-%d'), 'bacaan': reading})
            current_date += timedelta(days=1)
            chapter_index += chapters_per_day
        return schedule
    
    def get_todays_schedule(self, id_group):
        """ Get today's schedule for the given group

        Parameters:
        id_group (int): The id of the group

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""SELECT s.date, GROUP_CONCAT(c.chapter_name SEPARATOR ', ') AS chapter_names
                            FROM schedule_details_table sd
                            JOIN schedule_table s ON sd.id_schedule = s.id_schedule
                            JOIN chapter_table c ON sd.id_chapter = c.id_chapter
                            WHERE s.date = CURDATE() AND s.id_group = :id_group
                            GROUP BY s.date;
                        """)
            params = {"id_group": id_group}
            data = connection.execute(query, params)
            returnData = []
            for row in data:
                returnData.append({
                    'date': row[0],
                    'readings': ' '.join(word.capitalize() for word in row[1].split(' ')),
                })
        
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'Error: {str(e)}'
        return response
    
    def get_certain_date_chapter(self, id_group, date):
        """ Get the certain date schedule for a given group

        Parameters:
        id_group (int): The id of the group
        date (str): The date of the schedule

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""SELECT 
                                c.book_name, 
                                MAX(c.number) AS number
                            FROM chapter_table c
                            JOIN (
                                SELECT sd.id_chapter, MAX(sd.id_schedule_details) AS latest_id_schedule_details
                                FROM schedule_details_table sd
                                JOIN schedule_table s ON sd.id_schedule = s.id_schedule
                                WHERE s.date = :date AND s.id_group = :id_group
                                GROUP BY sd.id_chapter
                            ) latest_sd ON c.id_chapter = latest_sd.id_chapter
                            JOIN schedule_details_table sd ON sd.id_chapter = latest_sd.id_chapter AND sd.id_schedule_details = latest_sd.latest_id_schedule_details
                            GROUP BY c.book_name;
                        """)
            params = {"id_group": id_group, "date": date}
            data = connection.execute(query, params)
            returnData = []
            for row in data:
                returnData.append({
                    'book_name': row[0],
                    'number': row[1],
                })
        
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'Error: {str(e)}'
        return response
    
    def insert(self, id_group, date):
        """ Insert a new schedule
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("INSERT INTO schedule_table (id_group, date) VALUES (:id_group, :date);")
            params = {'id_group': id_group, 'date': date}
            connection.execute(query, params)
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'INSERT SCHEDULE | {str(e)}'
        return response
    
    def insert_details(self, id_schedule, id_chapter):
        """ Insert a new schedule
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("INSERT INTO schedule_details_table (id_schedule, id_chapter) VALUES (:id_schedule, :id_chapter);")
            params = {'id_schedule': id_schedule, 'id_chapter': id_chapter}
            connection.execute(query, params)
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'INSERT SCHEDULE DETAILS | {str(e)}'
        return response
    
    # def delete(self, id_group):
    #     response = {'status': False, 'msg': 'Database error'}
    #     try:
    #         query = text("DELETE FROM schedule_table WHERE id_group = :id_group;")        
    #         params = {"id_group": id_group}
    #         connection.execute(query, params)
    #         response = {'status': True, 'msg': 'Success'}
    #     except Exception as e:
    #         response['msg'] = f'Failed to delete schedule'
    #     return response
    
    # def delete_details(self, id_schedule):
    #     response = {'status': False, 'msg': 'Database error'}
    #     try:
    #         query = text("DELETE FROM schedule_details_table WHERE id_schedule = :id_schedule;")        
    #         params = {"id_schedule": id_schedule}
    #         connection.execute(query, params)
    #         # connection.commit()
    #         response = {'status': True, 'msg': 'Success'}
    #     except Exception as e:
    #         response['msg'] = f'Failed to delete schedule details'
    #     return response

    def get_schedule_last_id(self):
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT id_schedule
                        FROM schedule_table
                        ORDER BY id_schedule DESC
                        LIMIT 1;
                    """)
            data = connection.execute(query)
            returnData = 0
            for row in data:
                returnData= row[0]
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'Error: {str(e)}'
        return response
