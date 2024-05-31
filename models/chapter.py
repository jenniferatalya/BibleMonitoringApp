from models import connection, text

class Chapter:
    def get_all_chapters(self):
        """ Get all chapters id and name

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""SELECT 
                                c.id_chapter,
                                c.chapter_name
                            FROM 
                                chapter_table c
                        """)
            data = connection.execute(query)
            returnData = {}
            for row in data:
                returnData[row[1]] = row[0]
        
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'Error: {str(e)}'
        return response
    
    def get_master_chapter(self):
        """ Get all the chapter booknames and its max and min chapter numbers.

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""WITH example AS (
                                SELECT 
                                    c.book_name,
                                    min(c.number) as minimum,
                                    max(c.number) as maximum
                                from chapter_table c
                                group by c.book_name
                                order by min(c.id_chapter)
                            )
                            SELECT 
                                *
                                from example;
                        """)
            data = connection.execute(query)
            returnData = []
            for row in data:
                returnData.append({row[0]: {'min': row[1], 'max': row[2]}})
                # returnData[row[0]] = {'min': row[1], 'max': row[2]}
        
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'Error: {str(e)}'
        return response

    def get_booknames(self):
        """ Get book names and all of the book names' chapter numbers.

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""SELECT 
                                c.book_name,
                                GROUP_CONCAT(c.number ORDER BY c.id_chapter ASC SEPARATOR ', ') AS all_numbers
                            FROM 
                                chapter_table c
                            GROUP BY 
                                c.book_name
                            ORDER BY
                                MIN(c.id_chapter);
                        """)
            data = connection.execute(query)
            returnData = []
            for row in data:
                returnData.append({
                    'book_name': row[0],
                    'num_of_chapters': row[1]
                })
        
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'Error: {str(e)}'
        return response
    
    def get_chapters(self, book_name):
        """ Get all the chapter numbers of a given book

        Parameters:
        book_name (str): The name of the book

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""SELECT 
                                c.number 
                            FROM chapter_table c
                            WHERE c.book_name = :book_name
                            ORDER BY c.number;
                        """)
            params = {"book_name": book_name}
            data = connection.execute(query, params)
            returnData = []
            for row in data:
                returnData.append({
                    'chapter_number': row[0]
                })
        
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'Error: {str(e)}'
        return response
    
    def get_chapter_id(self, book_name, number):
        """ Get the chapter id of a certain chapter

        Parameters:
        book_name (str): The name of the book
        number (int): The number of the chapter

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""SELECT 
                                c.id_chapter
                            FROM chapter_table c
                            WHERE c.book_name = :book_name AND c.number = :number
                            ORDER BY c.number;
                        """)
            params = {"book_name": book_name, "number": number}
            data = connection.execute(query, params)
            returnData = []
            for row in data:
                returnData.append({
                    'id_chapter': row[0]
                })
        
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'Error: {str(e)}'
        return response
