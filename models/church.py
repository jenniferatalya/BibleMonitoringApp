from models import connection, text

class Church:
    def read(self):
        """ This method reads all the church information

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("SELECT * FROM church_table;")
            data = connection.execute(query)
            data = data.fetchall()
            returnData = []
            for row in data:
                returnData.append({
                    'id_church': row[0],
                    'church_name': row[1],
                    'phone': row[2],
                    'address': row[3],
                })
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'No data found!'
        return response
    
    def insert(self, church_name, phone, address):
        """ Insert a new church in the database

        Parameters:
        church_name (str): The name of the church
        phone (str): The phone number of the church
        address (str): The address of the church

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("INSERT INTO church_table (id_church, church_name, phone, address) VALUES (NULL, :church_name, :phone, :address);")
            params = {'church_name': church_name, 'phone': phone, 'address': address}
            connection.execute(query, params)
            # connection.commit()
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to insert church'
        return response
    
    def update(self, id_church, church_name, phone, address):
        """ Update a certain church information

        Parameters:
        id_church (int): The id of the church
        church_name (str): The name of the church
        phone (str): The phone number of the church
        address (str): The address of the church

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            if id_church == '1':
                response = {'status': False,'msg': 'You cannot update this church'}
            else:
                query = text("UPDATE church_table SET church_name = :church_name, phone = :phone, address = :address WHERE id_church = :id_church;")
                params = {'id_church': id_church, 'church_name': church_name, 'phone': phone, 'address': address}
                connection.execute(query, params)
                # connection.commit()
                response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to update church'
        return response
    
    def delete(self, id_church):
        """Delete a certain church from the database
        
        Parameters:
        id_church (int): The id of the church

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            if id_church == '1':
                response = {'status': False,'msg': 'You cannot delete this church'}
            else:
                query = text("DELETE FROM church_table WHERE id_church = :id_church;")
                
                params = {"id_church": id_church}
                connection.execute(query, params)
                # connection.commit()
                response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Cannot delete church'
        return response
    
    def get_all_names(self):
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT
                            church_name
                        FROM church_table;
                        """)
            data = connection.execute(query)
            returnData = []
            for row in data:
                returnData.append(row[0])
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'SELECT CHURCH | {str(e)}'
        return response
    
    def get_church_name_by_id(self, id_church):
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT
                            church_name
                        FROM church_table
                        WHERE id_church = :id_church;
                        """)
            params = {"id_church": id_church}
            data = connection.execute(query, params)
            returnData = []
            for row in data:
                returnData.append(row[0])
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'SELECT CHURCH | {str(e)}'
        return response