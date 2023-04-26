import json
import os
from datetime import datetime
from typing import List

from common.user_team_linking import UserTeamLinkingBase

from .schema import UserRequest, UserListResponse, UserTeamResponse


class UserController:
    def __init__(self):
        self.user_file = os.path.join("db", 'users.json')
        self.users = []

    def _save_users(self):
        with open(self.user_file, 'w') as f:
            json.dump(self.users, f)

    def _load_users(self):
        self.users = []

        for line in open(self.user_file, 'r'):
            self.users.extend(json.loads(line))

    def create_user(self, user_data: UserRequest) -> int:
        """
        Create a user.

        :param request: A dictionary with the user details
        {
          "name" : "<user_name>",
          "display_name" : "<display name>"
        }
        :return: A dictionary with the response {"id" : "<user_id>"}

        Constraint:
            * user name must be unique
            * name can be max 64 characters
            * display name can be max 64 characters
        """
        self._load_users()

        # Check if the user name already exists
        if any(t['name'] == user_data.name for t in self.users):
            raise ValueError("User name already exists")

        user_id = len(self.users) + 1

        user_data = user_data.dict()
        user_data['creation_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_data['id'] = user_id
        self.users.append(user_data)
        self._save_users()
        return user_id

    def list_users(self) -> List[UserListResponse]:
        """
        List all users.

        :return: A list with the response
        [
          {
            "name" : "<user_name>",
            "display_name" : "<display name>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        self._load_users()

        if not self.users:
            return []

        user_list = []
        for user in self.users:
            user_list.append(UserListResponse(
                id=user['id'],
                name=user['name'],
                display_name=user['display_name'],
                description=user['description'],
                creation_time=datetime.strptime(user['creation_time'], '%Y-%m-%d %H:%M:%S')
            ))
        return user_list

    def describe_user(self, user_data: dict) -> UserListResponse:
        """
        Describe a user.

        :param request: A dictionary with the user details
        {
          "id" : "<user_id>"
        }

        :return: A dictionary with the response

        {
          "name" : "<user_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>"
        }

        """
        user = self._get_user_by_id(user_data['id'])
        return UserListResponse(
            id=user['id'],
            name=user['name'],
            display_name=user['display_name'],
            description=user['description'],
            creation_time=datetime.strptime(user['creation_time'], '%Y-%m-%d %H:%M:%S')
        )

    def update_user(self, user_data: dict) -> int:
        """
        Update an existing user.

        :param request: A Pydantic UserUpdateRequest object with the user id and updated user details.
        :return: A json string with the response {"id" : "<user_id>"}

        Constraint:
           * user name cannot be updated
           * name can be max 64 characters
           * display name can be max 128 characters
        """

        user_id = user_data['id']
        user = self._get_user_by_id(user_id)
        updated_user = user_data['user']
        if 'display_name' in updated_user:
            user['display_name'] = updated_user['display_name']
        if 'description' in updated_user:
            user['description'] = updated_user['description']
        self._save_users()
        return user_id

    def get_user_teams(self, user_id) -> List[UserTeamResponse]:
        """
            :param request:
            {
              "id" : "<user_id>"
            }

            :return: A json list with the response.
            [
              {
                "name" : "<team_name>",
                "description" : "<some description>",
                "creation_time" : "<some date:time format>"
              }
            ]
        """
        user_team_linking = UserTeamLinkingBase()
        return user_team_linking.get_teams_of_a_user(user_id)

    def _get_user_by_id(self, user_id: int) -> dict:
        self._load_users()

        for user in self.users:
            if user['id'] == user_id:
                return user
        raise ValueError('User not found')

    def get_all_user_data(self):
        self._load_users()
        return self.users

