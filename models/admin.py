from models import connection, text

class Admin:
    def check_credential(self, username, password):
        """ Check the admin login information

        Parameters: 
        username (str): The username of the admin
        password (str): The password of the admin

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.  
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("SELECT * FROM admin_table WHERE username = :username and password = :password;")
            params = {"username": username, "password": password}
            data = connection.execute(query, params)
            rows = data.fetchone()
            if rows:
                returnData = {
                    'id_admin': rows[0],
                    'admin_name': rows[1],
                    'username': rows[2],
                    'phone': rows[4],
                    # 'id_group': rows[5],
                }
                response = {
                    'status': True, 
                    'msg': 'Success', 
                    'data': returnData
                }
            else:
                response = {
                    'status': False, 
                    'msg': 'Wrong Username or Password!', 
                    'data': None
                }
        except Exception as e:
            response['msg'] = f'Error: {str(e)}'
        return response

    def insert(self, admin_name, username, password, phone):
        """ Insert a new admin into the database

        Parameters:
        admin_name (str): The name of the admin
        username (str): The username of the admin
        password (str): The password of the admin in MD5 hash
        phone (str): The phone number of the admin

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.   
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            masterAdminUsername = self.get_all_usernames()['data']

            if username in masterAdminUsername:
                response = {
                   'status': False, 
                   'msg': 'Username already exists!'
                }
            else:
                query = text("INSERT INTO admin_table (id_admin, admin_name, username, password, phone) VALUES (NULL, :admin_name, :username, :password, :phone);")
                params = {'admin_name': admin_name, 'username': username, 'password': password, 'phone':phone}
                connection.execute(query, params)
                response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to insert admin'
        return response
    
    def insert_details(self, id_admin, id_group):
        """ Insert a new admin details

        Parameters:
        id_admin (int): The id of the admin
        id_group (int): The id of the group

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("INSERT INTO admin_details_table (id_admin, id_group) VALUES (:id_admin, :id_group);")
            params = {'id_admin': id_admin, 'id_group': id_group}
            connection.execute(query, params)

            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to insert admin details'
        return response
    
    def read(self):
        """ Read all the admins from the database

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                    SELECT
                        a.id_admin,
                        a.admin_name,
                        a.username,
                        a.password,
                        a.phone,
                        GROUP_CONCAT(ad.id_admin_details SEPARATOR ',') AS id_admin_details,
                        GROUP_CONCAT(ad.id_group SEPARATOR ',') AS admin_groups,
                        GROUP_CONCAT(g.group_name SEPARATOR ',') AS group_name
                    FROM admin_table a
                    JOIN admin_details_table ad ON a.id_admin = ad.id_admin
                    JOIN group_table g ON ad.id_group = g.id_group
                    GROUP BY a.id_admin, a.admin_name;
                    """)
            data = connection.execute(query)
            returnData = []
            for row in data:
                returnData.append({
                    'id_admin': row[0],
                    'admin_name': row[1],
                    'username': row[2],
                    'password': row[3],
                    'phone': row[4],
                    'id_admin_details': row[5].split(','),
                    'id_group': row[6].split(','),
                    'group_name': row[7].split(','),
                })
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'No data found'
        return response
    
    def update(self, id_admin, admin_name, username, phone):
        """ Updates an existing admin

        Parameters:
        id_admin (int): The id of the admin
        admin_name (str): The name of the admin
        username (str): The username of the admin
        phone (str): The phone number of the admin

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("UPDATE admin_table SET admin_name = :admin_name, username = :username, phone = :phone WHERE id_admin = :id_admin;")
            params = {'id_admin': id_admin, 'admin_name': admin_name, 'username': username, 'phone': phone}
            connection.execute(query, params)
            # connection.commit()
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to update admin'
        return response

    def update_details(self, id_admin_details, id_group):
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("UPDATE admin_details_table SET id_group = :id_group WHERE id_admin_details = :id_admin_details;")
            params = {'id_admin_details': id_admin_details, 'id_group': id_group}
            connection.execute(query, params)
            # connection.commit()
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to update admin'
        return response
    
    def reset_password(self, id_admin, password):
        """ Reset a certain admin's password

        Parameters:
        id_admin (int): The id of the admin
        password (str): The password of the admin in MD5 hash

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("UPDATE admin_table SET password = :password WHERE id_admin = :id_admin;")
            params = {'id_admin': id_admin, 'password': password}
            connection.execute(query, params)
            # connection.commit()
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to reset password'
        return response

    def delete(self, id_admin):
        """ Deletes a certain admin

        Parameters:
        id_admin (int): The id of the admin

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            if id_admin == '1':
                response = {'status': False,'msg': 'You cannot delete this admin'}
            else:
                query2 = text("DELETE FROM admin_details_table WHERE id_admin = :id_admin;")        
                params2 = {"id_admin": id_admin}
                connection.execute(query2, params2)

                query = text("DELETE FROM admin_table WHERE id_admin = :id_admin;")
                params = {"id_admin": id_admin}
                connection.execute(query, params)

                # connection.commit()
                response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Cannot delete admin'
        return response
    
    def delete_details(self, id_admin_details):
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("DELETE FROM admin_details_table WHERE id_admin_details = :id_admin_details;")        
            params = {"id_admin_details": id_admin_details}
            connection.execute(query, params)
            # connection.commit()
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to delete admin details'
        return response
    
    def count_current_admin(self):
        """ Count the number of admins in the database

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT COUNT(*)
                        FROM admin_table
                        """)
            data = connection.execute(query)
            returnData = 0
            for row in data:
                returnData = row[0]
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'Error: {str(e)}'
        return response
    
    def get_last_index(self):
        """ Get the last index exist in the admin_table

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                    SELECT (max(id_admin))
                    FROM admin_table;
                    """)
            
            data = connection.execute(query)
            result = data.fetchone()
            response = {'status': True, 'msg': 'Success', 'data': result[0]}
        except Exception as e:
            response['msg'] = f'SELECT ADmin | {str(e)}'
        return response
    
    def get_master_admin_details(self):
        """ Get all id_admin and its id_group

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                    SELECT
                        ad.id_admin
                        ad.id_group
                    FROM admin_details_table ad;
                    """)
            data = connection.execute(query)
            returnData = []
            for row in data:
                returnData.append([row[0], row[1]])
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'Error: {str(e)}'
        return response
    
    def get_all_usernames(self):
        """ Get all admins' usernames

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                    SELECT
                        a.username
                    FROM admin_table a;
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
            response['msg'] = f'Error: {str(e)}'
        return response
    
    def get_all_usernames(self):
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT
                            username
                        FROM admin_table;
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
            response['msg'] = f'SELECT ADMIN | {str(e)}'
        return response
    
    def get_username_by_id(self, id_admin):
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT
                            username
                        FROM admin_table
                        WHERE id_admin = :id_admin;
                        """)
            params = {"id_admin": id_admin}
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
            response['msg'] = f'SELECT ADMIN | {str(e)}'
        return response