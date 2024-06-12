from models import connection, text

class Member:
    def read(self):
        """ Read all the members' information from the database

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""SELECT
                            member_table.id_member,
                            member_table.member_name,
                            member_table.phone,
                            group_table.id_group,
                            group_table.group_name,
                            member_table.status
                        FROM member_table
                        JOIN group_table ON member_table.id_group = group_table.id_group;""")
            data = connection.execute(query)
            returnData = []
            for row in data:
                returnData.append({
                    'id_member': row[0],
                    'member_name': row[1],
                    'phone': row[2],
                    'id_group': row[3],
                    'group_name': row[4],
                    'status': row[5],
                })
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'No data found'
        return response
    
    def insert(self, member_name, phone, id_group, status):
        """ Insert a new member into the database

        Parameters:
        member_name (str): The name of the member
        phone (str): The phone number of the member
        id_group (int): The id of the group
        status (int): The status of the member

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("INSERT INTO member_table (id_member, member_name, phone, id_group, status) VALUES (NULL, :member_name, :phone, :id_group, :status);")
            params = {'member_name': member_name, 'phone': phone, 'id_group': id_group, 'status': status}
            connection.execute(query, params)
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to insert new member'
        return response
    
    def update(self, id_member, member_name, phone, id_group, status):
        """ Updates a certain member information
        
        Parameters:
        id_member (int): The id of the member
        member_name (str): The name of the member
        phone (str): The phone number of the member
        id_group (int): The id of the group
        status (int): The status of the member

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            if id_member == '1':
                response = {'status': False,'msg': 'You cannot update this member'}
            else:
                query = text("UPDATE member_table SET member_name = :member_name, phone = :phone, id_group = :id_group, status = :status WHERE id_member = :id_member;")
                params = {'id_member': id_member, 'member_name': member_name, 'phone': phone, 'id_group': id_group, 'status': status}
                connection.execute(query, params)
                # connection.commit()
                response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to update member'
        return response
    
    def alter_fk(self):
        response = {'status': False, 'msg': 'Database error'}
        try:
            
            query = text("""
                        ALTER TABLE report_details_table
                            ADD CONSTRAINT fk_report_details_report
                            FOREIGN KEY (id_report)
                            REFERENCES report_table(id_report)
                            ON DELETE CASCADE;
                    """)
            
            connection.execute(query)
            
            query2 = text("""
                        ALTER TABLE report_table
                            ADD CONSTRAINT fk_report_member
                            FOREIGN KEY (id_member)
                            REFERENCES member_table(id_member)
                            ON DELETE CASCADE; 
                    """)
            
            connection.execute(query2)
            response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Cannot delete group!'
        return response

    def delete(self, id_member):
        """ Delete a member from the database

        Parameters:
        id_member (int): The id of the member

        Returns:
        response (dict): A dictionary that contains the status of the query and the message of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            if id_member == '1':
                response = {'status': False,'msg': 'You cannot delete this member'}
            else:
                self.alter_fk()
                query = text("DELETE FROM member_table WHERE id_member = :id_member;")
                
                params = {"id_member": id_member}
                connection.execute(query, params)
                # connection.commit()
                response = {'status': True, 'msg': 'Success'}
        except Exception as e:
            response['msg'] = f'Failed to delete member'
        return response
    
    def get_members_by_group(self, id_group):
        """ Get list of members of a given group

        Parameters:
        id_group (int): The id of the group

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT 
                            m.id_member,
                            m.member_name
                        FROM member_table m
                        WHERE m.id_group = :id_group
                        ORDER BY m.member_name ASC;
                        """)
            params = {"id_group": id_group}
            data = connection.execute(query, params)
            returnData = []
            for row in data:
                returnData.append({
                    'id_member': row[0],
                    'member_name': row[1],
                })
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'SELECT MEMBERS | {str(e)}'
        return response

    def count_group_members(self, id_group):
        """ Counts the number of members of a given group

        Parameters:
        id_group (int): The id of the group

        Returns:
        response (dict): A dictionary that contains the status of the query, the message of the query, and the data of the query.
        """
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("SELECT COUNT(*) AS number_of_members FROM member_table WHERE id_group = :id_group;")
            params = {"id_group": id_group}
            data = connection.execute(query, params)
            returnData = []
            for row in data:
                returnData.append({
                    'number_of_members': row[0],
                })
            response = {
                'status': True, 
                'msg': 'Success', 
                'data': returnData
            }
        except Exception as e:
            response['msg'] = f'SELECT MEMBERS | {str(e)}'
        return response
    
    def get_all_names(self):
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT
                            m.member_name
                        FROM member_table m
                        ORDER BY m.member_name ASC;
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
            response['msg'] = f'SELECT MEMBERS | {str(e)}'
        return response
    
    def get_member_name_by_id(self, id_member):
        response = {'status': False, 'msg': 'Database error'}
        try:
            query = text("""
                        SELECT
                            member_name
                        FROM member_table
                        WHERE id_member = :id_member;
                        """)
            params = {"id_member": id_member}
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
            response['msg'] = f'SELECT MEMBER | {str(e)}'
        return response