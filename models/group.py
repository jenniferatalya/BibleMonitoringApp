from models import connection, text

class Group:
    def read(self):
        """ Read all the groups in the database

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                         SELECT 
                            g.id_group, 
                            g.group_name, 
                            g.id_church,
                            c.church_name,
                            g.start_date,
                            g.target_date,
                            g.num_of_chapter,
                            g.status
                        FROM group_table g
                        JOIN church_table c ON g.id_church = c.id_church;
                    """)
            data = connection.execute(query)
            returnData = []
            for row in data:
                returnData.append({
                    'id_group': row[0],
                    'group_name': row[1],
                    'id_church': row[2],
                    'church_name': row[3],
                    'start_date': row[4],
                    'target_date': row[5],
                    'num_of_chapter': row[6],
                    'status': row[7],
                })
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'No data found'
        return response
    
    def insert(self, group_name, id_church, start_date, target_date, num_of_chapter, status):
        """ Insert a new group

        Parameters:
        group_name (str): The name of the group
        id_church (int): The id of the church
        start_date (str): The start date of the group
        target_date (str): The target date of the group
        num_of_chapter (int): The number of chapters in the group
        status (int): The status of the group

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("INSERT INTO group_table (id_group, group_name, id_church, start_date, target_date, num_of_chapter, status) VALUES (NULL, :group_name, :id_church, :start_date, :target_date, :num_of_chapter, :status);")
            params = {'group_name': group_name, 'id_church': id_church, 'start_date': start_date, 'target_date': target_date, 'num_of_chapter': num_of_chapter, 'status': status}
            connection.execute(query, params)
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to insert new group'
        return response
    
    def update(self, id_group, group_name, id_church, status):
        """ Update a certain group information

        Parameters:
        id_group (int): The id of the group
        group_name (str): The name of the group
        id_church (int): The id of the church
        start_date (str): The start date of the group
        target_date (str): The target date of the group
        num_of_chapter (int): The number of chapters in the group
        status (int): The status of the group

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("UPDATE group_table SET group_name = :group_name, id_church = :id_church, status = :status WHERE id_group = :id_group;")
            params = {'id_group': id_group, 'group_name': group_name, 'id_church': id_church, 'status': status}
            connection.execute(query, params)
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to update group'
        return response
    
    def alter_fk(self):
        response = {'status': False, 'msg': 'Database error'}
        try:
            
            query = text("""
                        ALTER TABLE schedule_details_table
                            ADD CONSTRAINT fk_schedule_details_schedule
                            FOREIGN KEY (id_schedule)
                            REFERENCES schedule_table(id_schedule)
                            ON DELETE CASCADE;
                    """)
            
            connection.execute(query)

            query2 = text("""
                        ALTER TABLE schedule_table
                            ADD CONSTRAINT fk_schedule_group
                            FOREIGN KEY (id_group)
                            REFERENCES group_table(id_group)
                            ON DELETE CASCADE; 
                    """)
            
            connection.execute(query2)
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Cannot delete group!'
        return response
    
    def delete(self, id_group):
        """ Delete a group

        Parameters:
        id_group (int): The id of the group

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            if id_group == '1':
                response = {'status': False,'msg': 'You cannot delete this group'}
            else:
                self.alter_fk()
                query = text("""
                            DELETE FROM group_table
                            WHERE id_group = :id_group;
                        """)
                
                params = {"id_group": id_group}
                connection.execute(query, params)
                response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Cannot delete group!'
        return response
    
    def get_group_name(self, id_group):
        """ Get a certain group name by its id

        Parameters:
        id_group (int): The id of the group

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                         SELECT g.group_name 
                         FROM group_table g
                         WHERE g.id_group = :id_group;
                         """)
            
            params = {"id_group": id_group}
            data = connection.execute(query, params)
            returnData = ""
            for row in data:
                returnData = row[0]
            response = {'status': True, 'msg': 'Success', 'data': returnData}
        except Exception as e:
            response['msg'] = f'Cannot delete group!'
        return response
    
    def get_group_ids(self):
        """ Get all the group ids in the database

        Returns:
        response (list): A list of group ids
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                    SELECT
                        g.id_group
                    FROM group_table g;
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
    
    def get_group_last_id(self):
        """ Get the last id exist in the group_table

        Returns:
        response (int): the last id exist in the group_table
        
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT id_group
                        FROM group_table
                        ORDER BY id_group DESC
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
    
    def get_all_names(self):
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT
                            group_name
                        FROM group_table;
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
            response['msg'] = f'SELECT GROUP | {str(e)}'
        return response
    
    def get_group_name_by_id(self, id_group):
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT
                            group_name
                        FROM group_table
                        WHERE id_group = :id_group;
                        """)
            params = {"id_group": id_group}
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
            response['msg'] = f'SELECT GROUP | {str(e)}'
        return response