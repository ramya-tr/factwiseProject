import json
import os
from datetime import datetime
from typing import List

from common.user_team_linking import UserTeamLinkingBase
from users.controller import UserController

from .schema import (
    TeamCreateRequest,
    TeamListResponse,
    TeamAddRemoveUsersRequest,
)



class TeamBase:
    def __init__(self):
        self.team_file_path = os.path.join("db", 'team.json')

    def _load_teams(self):
        self.teams = []
        for line in open(self.team_file_path, 'r'):
            self.teams.extend(json.loads(line))

    def _save_teams(self):
        with open(self.team_file_path, 'w') as f:
            json.dump(self.teams, f)

    def create_team(self, team: TeamCreateRequest) -> int:
        """
        :param request: A json string with the team details
        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "admin": "<id of a user>"
        }
        :return: A json string with the response {"id" : "<team_id>"}

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """

        # check if the admin user exists
        user_controller = UserController()
        user = user_controller._get_user_by_id(team.admin)

        self._load_teams()

        # Check if the team name already exists
        if any(t['name'] == team.name for t in self.teams):
            raise ValueError("Team name already exists")

        # Generate new team id
        if self.teams:
            new_id = max(t['id'] for t in self.teams) + 1
        else:
            new_id = 1

        # Create new team
        new_team = {
            "id": new_id,
            "name": team.name,
            "description": team.description,
            "creation_time": str(datetime.now()),
            "admin": team.admin,
            "users": []
        }

        self.teams.append(new_team)
        self._save_teams()

        return new_id

    def list_teams(self) -> List[TeamListResponse]:
        """
        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>",
            "admin": "<id of a user>"
          }
        ]
        """
        self._load_teams()

        team_list = []
        for t in self.teams:
            team_list.append(TeamListResponse(
                id=t['id'],
                name=t['name'],
                description=t['description'],
                creation_time=datetime.fromisoformat(t['creation_time']),
                admin=t['admin']
            ))

        return team_list

    def describe_team(self, data) -> TeamListResponse:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>"
        }

        :return: A json string with the response

        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>",
          "admin": "<id of a user>"
        }

        """
        team_id = data['id']
        self._load_teams()

        for t in self.teams:
            if t['id'] == team_id:
                return TeamListResponse(
                    id=t['id'],
                    name=t['name'],
                    description=t['description'],
                    creation_time=datetime.fromisoformat(t['creation_time']),
                    admin=t['admin']
                )

        return None

    def update_team(self, data):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "team" : {
            "name" : "<team_name>",
            "description" : "<team_description>",
            "admin": "<id of a user>"
          }
        }

        :return:

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """

        team_id = data['id']
        new_team = data['team']

        # check if the admin user exists
        user_controller = UserController()
        user = user_controller._get_user_by_id(new_team.admin)

        self._load_teams()

        for i, t in enumerate(self.teams):
            if t['id'] == team_id:
                # Check if the new team name already exists
                if any(tt['name'] == new_team.name for tt in self.teams if tt != t):
                    raise ValueError("Team name already exists")

                # Update team
                self.teams[i]['name'] = new_team.name
                self.teams[i]['description'] = new_team.description
                self.teams[i]['admin'] = new_team.admin

                self._save_teams()
                return

        raise ValueError("Team not found")

    def add_users_to_team(self, team_id: int, users: TeamAddRemoveUsersRequest):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        team = self.get_team_by_id(team_id)

        user_team_linking = UserTeamLinkingBase()
        user_team_linking.add_users_to_team(team_id, users.users)

    # add users to team
    def remove_users_from_team(self, team_id, users):
        """
        :param

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        team = self.get_team_by_id(team_id)

        user_team_linking = UserTeamLinkingBase()
        user_team_linking.remove_users_from_team(team_id, users.users)

    # list users of a team
    def list_team_users(self, team_id):
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<user_id>",
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        ]
        """
        team = self.get_team_by_id(team_id)

        user_team_linking = UserTeamLinkingBase()
        return user_team_linking.list_users_in_a_team(team_id)


    def get_team_by_id(self, team_id: int) -> dict:
        self._load_teams()

        for team in self.teams:
            if team['id'] == team_id:
                return team
        raise ValueError('Team not found')

    def get_all_team_data(self):
        self._load_teams()
        return self.teams
