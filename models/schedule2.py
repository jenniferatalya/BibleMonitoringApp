from models import connection, text

class Schedule:
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