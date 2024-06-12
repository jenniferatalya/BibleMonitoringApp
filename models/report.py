from models import connection, text
from models.chapter import Chapter
import sqlalchemy

class Report:
    def insert(self, date, id_member, report):
        """ Insert a new report

        Parameters:
        date (str): The date of the report
        id_member (int): The id of the member
        report (str): The report

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("INSERT INTO report_table (id_report, date, id_member, report) VALUES (NULL, :date, :id_member, :report);")
            params = {'date': date, 'id_member': id_member, 'report': report}
            connection.execute(query, params)
            # connection.commit()
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to insert new report'
        return response

    def insert_details(self, id_report, id_chapter):
        """ Insert a new report details

        Parameters:
        id_report (int): The id of the report
        id_chapter (int): The id of the chapter

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("INSERT INTO report_details_table (id_report, id_chapter) VALUES (:id_report, :id_chapter);")
            params = {'id_report': id_report, 'id_chapter': id_chapter}
            connection.execute(query, params)

            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to insert report details'
        return response
    
    def read(self):
        """ Get all the records of reports in the database

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                    SELECT
                        r.id_report,
                        r.date,
                        r.id_member,
                        m.member_name,
                        r.report,
                        GROUP_CONCAT(rd.id_report_details SEPARATOR ',') AS id_report_details,
                        GROUP_CONCAT(c.chapter_name SEPARATOR ',') AS chapter_name
                    FROM report_table r
                    JOIN member_table m ON r.id_member = m.id_member
                    JOIN report_details_table rd ON r.id_report = rd.id_report
                    JOIN chapter_table c ON rd.id_chapter = c.id_chapter
                    GROUP BY r.id_report, m.member_name;
                    """)
            data = connection.execute(query)
            returnData = []
            for row in data:
                returnData.append({
                    'id_report': row[0],
                    'date': row[1],
                    'id_member': row[2],
                    'member_name': row[3],
                    'report': row[4],
                    'id_report_details': row[5].split(','),
                    'chapter_name': row[6].split(','),
                })
            response = {
                'status': True,
                'msg': 'Success',
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'No data found'
        return response

    def update(self, id_report, date, id_member, report):
        """ Update a certain report in the report_table

        Parameters:
        id_report (int): The id of the report
        date (str): The date of the report
        id_member (int): The id of the member
        report (str): The report

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                         UPDATE report_table 
                         SET date = :date, id_member = :id_member, report = :report 
                         WHERE id_report = :id_report;
                         """)
            
            params = {'id_report': id_report, 'date': date, 'id_member': id_member, 'report': report}
            connection.execute(query, params)
            
            # query2 = text("""UPDATE report""")
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to update report data'
        return response
    
    def update_details(self, id_report_details, id_chapter):
        """ Updates the details of a report in the report_details_table

        Parameters:
        id_report_details (int): The id of the report details
        id_chapter (int): The id of the chapter

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                         UPDATE report_details_table 
                         SET id_chapter = :id_chapter
                         WHERE id_report_details = :id_report_details;
                         """)
            
            params = {'id_report_details': id_report_details, 'id_chapter': id_chapter}
            connection.execute(query, params)
            
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to update report details'
        return response

    def delete(self, id_report):
        """ Delete a certain report from the report_table and report_details_table

        Parameters:
        id_report (int): The id of the report

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("DELETE FROM report_details_table WHERE id_report = :id_report;")
            params = {"id_report": id_report}
            connection.execute(query, params)

            query2 = text("DELETE FROM report_table WHERE id_report = :id_report;")
            params2 = {"id_report": id_report}
            connection.execute(query2, params2)
            # connection.commit()
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Cannot delete report!'
        return response
    
    def delete_details(self, id_report_details):
        """ Delete a report details from the database

        Parameters:
        id_report_details (int): The id of the report details

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("DELETE FROM report_details_table WHERE id_report_details = :id_report_details;")
            params = {"id_report_details": id_report_details}
            connection.execute(query, params)

            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Cannot delete report'
        return response
    
    def insert_many(self, data_to_db):
        """ Insert a list of report into the database

        Parameters:
        data_to_db (dict): A dictionary that contains the data to be inserted

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                    INSERT INTO report_table (id_member, date, report)
                    VALUES (:id_member, :date, :report);
                    """)
            
            result:sqlalchemy.engine.cursor.LegacyCursorResult = connection.execute(query, data_to_db)
            inserted_data = self.get_last_index().get('data')
            parsed_data = data_to_db['parsed']
           
            for data in parsed_data:
                self.insert_details(inserted_data, data)
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'INSERT MANY REPORT | {str(e)}'
        return response
    
    def get_last_index(self):
        """ Get the last index in the report_table

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                    SELECT (max(id_report))
                    FROM report_table;
                    """)
            
            data = connection.execute(query)
            result = data.fetchone()
            response = {'status': True, 'msg': 'Success', 'data': result[0]}
        except Exception as e:
            response['msg'] = f'SELECT REPORT | {str(e)}'
        return response
    
    def get_data_graph1(self, id_group):
        """ Get the data to create a graph for a given group

        Parameters:
        id_group (int): The id of the group

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT 
                            rt.date, 
                            COUNT(DISTINCT rt.id_member) as number_of_member
                        FROM report_table rt 
                        JOIN member_table m ON rt.id_member = m.id_member
                        WHERE rt.date BETWEEN CURDATE() - INTERVAL 6 DAY AND CURDATE() AND m.id_group = :id_group
                        GROUP BY rt.date
                        ORDER BY rt.date;
            """)
            params = {'id_group': id_group}
            data = connection.execute(query, params)
            returnData = []
            for row in data:
                returnData.append({
                    'report_date': row[0],
                    'num_members': int(row[1]),
                })
            response = {
                'status': True,
                'msg': 'Success',
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'Error: {str(e)}'
        return response
    
    def get_data_monthly(self, id_group):
        """ Get the data to create a graph for a given group

        Parameters:
        id_group (int): The id of the group

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT 
                            rt.date, 
                            COUNT(DISTINCT rt.id_member) as number_of_member
                        FROM report_table rt 
                        JOIN member_table m ON rt.id_member = m.id_member
                        WHERE rt.date BETWEEN CURDATE() - INTERVAL 30 DAY AND CURDATE() AND m.id_group = :id_group
                        GROUP BY rt.date
                        ORDER BY rt.date;
            """)
            params = {'id_group': id_group}
            data = connection.execute(query, params)
            returnData = []
            for row in data:
                returnData.append({
                    'report_date': row[0],
                    'num_members': int(row[1]),
                })
            response = {
                'status': True,
                'msg': 'Success',
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'Error: {str(e)}'
        return response

    def get_data_lifetime(self, id_group):
        """ Get the data to create a graph for a given group

        Parameters:
        id_group (int): The id of the group

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT 
                            rt.date, 
                            COUNT(DISTINCT rt.id_member) as number_of_member
                        FROM report_table rt 
                        JOIN member_table m ON rt.id_member = m.id_member
                        WHERE rt.date BETWEEN CURDATE() - INTERVAL 60 DAY AND CURDATE() AND m.id_group = :id_group
                        GROUP BY rt.date
                        ORDER BY rt.date;
            """)
            params = {'id_group': id_group}
            data = connection.execute(query, params)
            returnData = []
            for row in data:
                returnData.append({
                    'report_date': row[0],
                    'num_members': int(row[1]),
                })
            response = {
                'status': True,
                'msg': 'Success',
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'Error: {str(e)}'
        return response
    
    def get_members_by_report(self, id_group, date, book_name, number):
        """ Get member name based on a report

        Parameters:
        id_group (int): The id of the group
        date (str): The date of the report
        book_name (str): The name of the book
        number (int): The number of the chapter

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT m.member_name
                        FROM member_table m
                        JOIN report_table r ON r.id_member = m.id_member
                        JOIN report_details_table rd ON r.id_report = rd.id_report
                        JOIN chapter_table c ON rd.id_chapter = c.id_chapter
                        WHERE r.date = :date AND c.book_name = :book_name AND c.number = :number AND m.id_group = :id_group
                        """)
            params = {'id_group': id_group, 'date': date, 'book_name': book_name, 'number': number}
            data = connection.execute(query, params)
        
            returnData = []
            for row in data:
                returnData.append({
                    'member_name': row[0],
                })
            response = {'status': True, 'msg': 'Success', 'data': returnData}
        except Exception as e:
            response['msg'] = f'SELECT REPORT | {str(e)}'
        return response
    
    def get_members_not_reporting_more_than_7days(self, id_group):
        """ Get list of members who have not reporting for more than 7 days

        Parameters:
        id_group (int): The id of the group

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT m.member_name, c.chapter_name AS last_read_chapter 
                        FROM member_table m 
                        JOIN ( 
                            SELECT r.id_member, MAX(r.date) AS last_report_date, MAX(rd.id_chapter) AS last_read_chapter_id 
                            FROM report_table r 
                            JOIN report_details_table rd ON r.id_report = rd.id_report 
                            GROUP BY r.id_member 
                            HAVING last_report_date <= CURDATE() - INTERVAL 7 DAY
                        ) last_read ON m.id_member = last_read.id_member 
                        JOIN chapter_table c ON last_read.last_read_chapter_id = c.id_chapter
                        WHERE m.id_group=:id_group
                        ORDER BY last_read.last_read_chapter_id;
                        """)
            params = {'id_group': id_group}
            data = connection.execute(query, params)
            returnData = []
            for row in data:
                if row[1] == 'null':
                    continue
                else:
                    returnData.append({
                        'member_name': row[0],
                        'chapter_name': row[1],
                    })
            response = {'status': True, 'msg': 'Success', 'data': returnData}
        except Exception as e:
            response['msg'] = f'SELECT REPORT | {str(e)}'
        return response

    def get_reading_percentage(self, id_group):
        """ Get a certain group reading percentage

        Parameters:
        id_group (int): The id of the group

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT 
                            (MAX(rd.id_chapter)/1189)*100 AS group_reading_percentage
                        FROM report_details_table rd
                        JOIN report_table r ON rd.id_report = r.id_report
                        JOIN member_table m ON r.id_member = m.id_member
                        JOIN group_table g ON m.id_group = g.id_group
                        WHERE g.id_group = :id_group;
                        """)
            params = {'id_group': id_group}
            data = connection.execute(query, params)
            returnData = 0
            for row in data:
                returnData = row[0]
            response = {'status': True, 'msg': 'Success', 'data': returnData}
        except Exception as e:
            response['msg'] = f'SELECT REPORT | {str(e)}'
        return response
    
    def get_members_segmentation(self, id_group):
        """ Get the number of members based on the segmentation

        Params:
        id_group (int): The id of the group

        Response:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            params = {'id_group': id_group}
            returnData = {}

            query_ontime = text("""
                                WITH LatestReport AS (
                                    SELECT id_member, MAX(date) AS latest_date
                                    FROM report_table
                                    GROUP BY id_member
                                ),
                                MemberLatestReport AS (
                                    SELECT r.id_report, r.id_member, r.date
                                    FROM report_table r
                                    JOIN LatestReport lr ON r.id_member = lr.id_member AND r.date = lr.latest_date
                                ),
                                MaxChapterPerMember AS (
                                    SELECT mlr.id_member, MAX(rd.id_chapter) AS latest_id_chapter
                                    FROM MemberLatestReport mlr
                                    JOIN report_details_table rd ON mlr.id_report = rd.id_report
                                    GROUP BY mlr.id_member
                                )
                                SELECT COUNT(m.member_name)
                                FROM MaxChapterPerMember mcpm
                                JOIN member_table m ON mcpm.id_member = m.id_member
                                JOIN schedule_details_table sd ON mcpm.latest_id_chapter = sd.id_chapter
                                JOIN schedule_table s ON sd.id_schedule = s.id_schedule
                                WHERE s.date >= CURDATE() - INTERVAL 1 DAY
                                AND s.id_group=:id_group
                                AND m.id_group=:id_group;
                                """)
            
            data_ontime = connection.execute(query_ontime, params)

            for row in data_ontime:
                returnData['ontime'] = row[0]

            query_7dayslate = text("""
                                WITH LatestReport AS (
                                    SELECT id_member, MAX(date) AS latest_date
                                    FROM report_table
                                    GROUP BY id_member
                                ),
                                MemberLatestReport AS (
                                    SELECT r.id_report, r.id_member, r.date
                                    FROM report_table r
                                    JOIN LatestReport lr ON r.id_member = lr.id_member AND r.date = lr.latest_date
                                ),
                                MaxChapterPerMember AS (
                                    SELECT mlr.id_member, MAX(rd.id_chapter) AS latest_id_chapter
                                    FROM MemberLatestReport mlr
                                    JOIN report_details_table rd ON mlr.id_report = rd.id_report
                                    GROUP BY mlr.id_member
                                )
                                SELECT COUNT(m.member_name)
                                FROM MaxChapterPerMember mcpm
                                JOIN member_table m ON mcpm.id_member = m.id_member
                                JOIN schedule_details_table sd ON mcpm.latest_id_chapter = sd.id_chapter
                                JOIN schedule_table s ON sd.id_schedule = s.id_schedule
                                WHERE s.date < CURDATE() - INTERVAL 1 DAY
                                AND s.date >= CURDATE() - INTERVAL 7 DAY
                                AND s.id_group=:id_group
                                AND m.id_group=:id_group;
                                """)
            data_7dayslate = connection.execute(query_7dayslate, params)

            for row in data_7dayslate:
                returnData['7_days'] = row[0]

            query_1monthlate = text("""
                                WITH LatestReport AS (
                                    SELECT id_member, MAX(date) AS latest_date
                                    FROM report_table
                                    GROUP BY id_member
                                ),
                                MemberLatestReport AS (
                                    SELECT r.id_report, r.id_member, r.date
                                    FROM report_table r
                                    JOIN LatestReport lr ON r.id_member = lr.id_member AND r.date = lr.latest_date
                                ),
                                MaxChapterPerMember AS (
                                    SELECT mlr.id_member, MAX(rd.id_chapter) AS latest_id_chapter
                                    FROM MemberLatestReport mlr
                                    JOIN report_details_table rd ON mlr.id_report = rd.id_report
                                    GROUP BY mlr.id_member
                                )
                                SELECT COUNT(m.member_name)
                                FROM MaxChapterPerMember mcpm
                                JOIN member_table m ON mcpm.id_member = m.id_member
                                JOIN schedule_details_table sd ON mcpm.latest_id_chapter = sd.id_chapter
                                JOIN schedule_table s ON sd.id_schedule = s.id_schedule
                                WHERE s.date < CURDATE() - INTERVAL 7 DAY
                                AND s.date >= CURDATE() - INTERVAL 30 DAY
                                AND s.id_group=:id_group
                                AND m.id_group=:id_group;
                                """)
            data_1monthlate = connection.execute(query_1monthlate, params)

            for row in data_1monthlate:
                returnData['1_month'] = row[0]

            query_more_than_1month = text("""
                                        WITH LatestReport AS (
                                            SELECT id_member, MAX(date) AS latest_date
                                            FROM report_table
                                            GROUP BY id_member
                                        ),
                                        MemberLatestReport AS (
                                            SELECT r.id_report, r.id_member, r.date
                                            FROM report_table r
                                            JOIN LatestReport lr ON r.id_member = lr.id_member AND r.date = lr.latest_date
                                        ),
                                        MaxChapterPerMember AS (
                                            SELECT mlr.id_member, MAX(rd.id_chapter) AS latest_id_chapter
                                            FROM MemberLatestReport mlr
                                            JOIN report_details_table rd ON mlr.id_report = rd.id_report
                                            GROUP BY mlr.id_member
                                        )
                                        SELECT COUNT(m.member_name)
                                        FROM MaxChapterPerMember mcpm
                                        JOIN member_table m ON mcpm.id_member = m.id_member
                                        JOIN schedule_details_table sd ON mcpm.latest_id_chapter = sd.id_chapter
                                        JOIN schedule_table s ON sd.id_schedule = s.id_schedule
                                        WHERE s.date < CURDATE() - INTERVAL 30 DAY
                                        AND s.id_group=:id_group
                                        AND m.id_group=:id_group;
                                        """)
            data_more_than_1month = connection.execute(query_more_than_1month, params)

            for row in data_more_than_1month:
                returnData['more_than_1month'] = row[0]

            response = {'status': True, 'msg': 'Success', 'data': returnData}
        except Exception as e:
            response['msg'] = f'SELECT REPORT | {str(e)}'
        return response

    def get_report_dates(self, id_group):
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT 
                            DISTINCT r.date
                        FROM report_table r
                        JOIN member_table m ON r.id_member = m.id_member
                        WHERE m.id_group = :id_group
                        """)
            params = {'id_group': id_group}
            data = connection.execute(query, params)
            returnData = []
            for row in data:
                returnData.append(row[0])
            response = {'status': True, 'msg': 'Success', 'data': returnData}
        except Exception as e:
            response['msg'] = f'SELECT REPORT | {str(e)}'
        return response
    
    def get_member_last_chapter(self, id_member, date):
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT 
                            c.id_chapter,
                            c.chapter_name
                        FROM chapter_table c
                        JOIN report_details_table rd ON rd.id_chapter = c.id_chapter
                        JOIN report_table r ON r.id_report = rd.id_report
                        WHERE r.id_member = :id_member
                        AND r.date <= :date
                        ORDER BY c.id_chapter DESC
                        LIMIT 1;
                        """)
            params = {'id_member': id_member, 'date': date}
            data = connection.execute(query, params)
            returnData = {}
            for row in data:
                returnData['id_chapter'] = row[0]
                returnData['chapter_name'] = row[1]
            response = {'status': True, 'msg': 'Success', 'data': returnData}
        except Exception as e:
            response['msg'] = f'SELECT REPORT | {str(e)}'
        return response