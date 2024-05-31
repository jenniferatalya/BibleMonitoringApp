from models import connection, text

class Devotion:
    def read(self):
        """ Read all the devotion data from the database

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""SELECT 
                            d.id_devotion, 
                            d.title, 
                            d.content, 
                            d.id_chapter, 
                            c.chapter_name 
                         FROM devotion_table d
                         JOIN chapter_table c ON d.id_chapter = c.id_chapter;""")
            data = connection.execute(query)
            returnData = []
            for row in data:
                returnData.append({
                    'id_devotion': row[0],
                    'title': row[1],
                    'content': row[2],
                    'id_chapter': row[3],
                    'chapter_name': row[4]
                })
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'No data found'
        return response
    
    def insert(self, title, content, id_chapter):
        """ Insert a new devotion

        Parameters:
        title (str): The title of the devotion
        content (str): The content of the devotion
        id_chapter (int): The id of the chapter

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("INSERT INTO devotion_table (id_devotion, title, content, id_chapter) VALUES (NULL, :title, :content, :id_chapter);")
            params = {'title': title, 'content': content, 'id_chapter': id_chapter}
            connection.execute(query, params)
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to insert new devotion'
        return response
    
    def update(self, id_devotion, title, content, id_chapter):
        """ Update a certain devotion

        Parameters:
        id_devotion (int): The id of the devotion
        title (str): The title of the devotion
        content (str): The content of the devotion
        id_chapter (int): The id of the chapter

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("UPDATE devotion_table SET title = :title, content = :content, id_chapter = :id_chapter WHERE id_devotion = :id_devotion;")
            params = {'id_devotion': id_devotion, 'title': title, 'content': content, 'id_chapter': id_chapter}
            connection.execute(query, params)
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to update devotion'
        return response
    
    def delete(self, id_devotion):
        """ Delete a certain devotion

        Parameters:
        id_devotion (int): The id of the devotion

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("DELETE FROM devotion_table WHERE id_devotion = :id_devotion;")
            
            params = {"id_devotion": id_devotion}
            connection.execute(query, params)
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Cannot delete devotion!'
        return response
    
    def get_devotion_by_id(self, id_devotion):
        """
        Get devotion content by given id_devotion
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""SELECT 
                            d.title, 
                            d.content, 
                            d.id_chapter, 
                            c.chapter_name 
                         FROM devotion_table d
                         JOIN chapter_table c ON d.id_chapter = c.id_chapter
                         WHERE d.id_devotion = :id_devotion;""")
            params = {'id_devotion': id_devotion}
            data = connection.execute(query, params)
            returnData = []
            for row in data:
                returnData.append({
                    'title': row[0],
                    'content': row[1],
                    'id_chapter': row[2],
                    'chapter_name': row[3]
                })
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'No data found'
        return response