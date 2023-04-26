import json
import os
from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel
from pydantic import PositiveInt


class UserTeamLinking(BaseModel):
    user_id: PositiveInt
    team_id: PositiveInt


class UserTeamLinkingBase:
    def __init__(self):
        self.user_file_path = os.path.join("db", 'users.json')
        self.team_file_path = os.path.join("db", 'team.json')
        self.linking_file_path = os.path.join("db", 'user_team_linking.json')

    def read_file(self, file_path: str):
        data = []

        for line in open(file_path, 'r'):
            data.extend(json.loads(line))

        return data

    def write_file(self, file_path: str, data: List[Dict]):
        with open(file_path, 'w') as f:
            json.dump(data, f)

    def add_users_to_team(self, team_id, users):
        linking_data = self.read_file(self.linking_file_path)
        user_data = self.read_file(self.user_file_path)

        user_list = {}
        for item in user_data:
            user_list[item["id"]] = item["id"]

        for user in users:
            if user not in user_list:
                raise ValueError(f"User with id = {user} not found")

            user_team_linking = UserTeamLinking(user_id=user, team_id=team_id)
            if user_team_linking.dict() not in linking_data:
                linking_data.append(user_team_linking.dict())

        self.write_file(self.linking_file_path, linking_data)

    def remove_users_from_team(self, team_id, users_to_remove):
        linking_data = self.read_file(self.linking_file_path)
        for user in users_to_remove:
            user_team_linking = UserTeamLinking(user_id=user, team_id=team_id)
            if user_team_linking.dict() in linking_data:
                linking_data.remove(user_team_linking.dict())
        self.write_file(self.linking_file_path, linking_data)

    def list_users_in_a_team(self, team_id):
        user_data = self.read_file(self.user_file_path)
        linking_data = self.read_file(self.linking_file_path)

        user_list = {
            item["id"]: {"user_id": item["id"], "user_name": item["name"], "display_name": item["display_name"]}
            for item in user_data
        }

        response = [user_list[item["user_id"]] for item in linking_data if item["team_id"] == team_id]

        return response

    def get_teams_of_a_user(self, user_id):
        team_data = self.read_file(self.team_file_path)
        linking_data = self.read_file(self.linking_file_path)

        team_list = {
            item["id"]: {"name": item["name"], "description": item["description"],
                         "creation_time": datetime.fromisoformat(item["creation_time"])}
            for item in team_data
        }

        response = [team_list[item["team_id"]] for item in linking_data if item["user_id"] == user_id]

        return response

    def check_if_user_and_team_linking_exists(self, team_id, user_id):
        linking_data = self.read_file(self.linking_file_path)
        user_team_linking = UserTeamLinking(user_id=user_id, team_id=team_id)

        if user_team_linking.dict() in linking_data:
            return True
        else:
            return False
