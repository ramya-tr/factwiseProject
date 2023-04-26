import json
import os
from datetime import datetime
from typing import List

from common.user_team_linking import UserTeamLinkingBase
from teams.controller import TeamBase
from users.controller import UserController

from .schema import BoardBase, BoardList, TaskBase, TaskStatusUpdate, TaskList


class ProjectBoardBase:
    """
        A project board is a unit of delivery for a project.
        Each board will have a set of tasks assigned to a user.
        """

    def __init__(self):
        self.board_file_path = os.path.join("db", 'board.json')
        self.task_file_path = os.path.join("db", 'task.json')

    def _load_board_data(self):
        self.boards = []
        for line in open(self.board_file_path, 'r'):
            self.boards.extend(json.loads(line))

    def _save_board_data(self):
        with open(self.board_file_path, "w") as f:
            json.dump(self.boards, f)

    def _load_task_data(self):
        self.tasks = []
        for line in open(self.task_file_path, 'r'):
            self.tasks.extend(json.loads(line))

    def _save_task_data(self):
        with open(self.task_file_path, "w") as f:
            json.dump(self.tasks, f)

    def create_board(self, board_request: BoardBase) -> int:
        """
        :param board_request: A json string with the board details.
        {
            "name" : "<board_name>",
            "description" : "<description>",
            "team_id" : "<team id>"
            "creation_time" : "<date:time when board was created>"
        }
        :return: A json string with the response {"id" : "<board_id>"}

        Constraint:
         * board name must be unique for a team
         * board name can be max 64 characters
         * description can be max 128 characters
        """

        # validate that a team with that id exists
        team = TeamBase().get_team_by_id(board_request.team_id)

        self._load_board_data()

        # Check if the board title name already exists for the team
        if any(t['name'] == board_request.name and t['team_id'] == board_request.team_id for t in self.boards):
            raise ValueError("Board already exists for this team")

        # Generate new team id
        new_id = len(self.boards) + 1

        new_board = {"id": new_id,
                     'creation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                     "board_status": 'Open',
                     **board_request.dict()}
        self.boards.append(new_board)
        self._save_board_data()
        return new_board["id"]

    def close_board(self, board_id: int):
        """
        :param request: A json string with the user details
        {
          "board_id" : "<board_id>"
        }

        :return:

        Constraint:
          * Set the board status to CLOSED and record the end_time date:time
          * You can only close boards with all tasks marked as COMPLETE
        """

        board = self.get_board(board_id)
        board["board_status"] = 'Closed'
        self._save_board_data()

    def add_task(self, task: TaskBase) -> int:
        """
        :param request: A json string with the task details. Task is assigned to a user_id who works on the task
        {
            "board_id" : "<board_id>",
            "title" : "<task_name>",
            "description" : "<description>",
            "user_id" : "<team id>"
        }
        :return: A json string with the response {"id" : "<task_id>"}

        Constraint:
         * task title must be unique for a board
         * title name can be max 64 characters
         * description can be max 128 characters

        Constraints:
        * Can only add task to an OPEN board
        """

        # check if board exists and is Open
        board = self.get_board(task.board_id)

        if board["board_status"] == 'Closed':
            raise ValueError("Board is closed")

        # check if user in task belongs to team in board

        user_team_linking = UserTeamLinkingBase()
        if not user_team_linking.check_if_user_and_team_linking_exists(board["team_id"], task.user_id):
            raise ValueError("The user the task is assigned to does not belong to the team that the board is for")

        self._load_task_data()

        # Check if the task title name already exists
        if any(t['title'] == task.title and t['board_id'] == task.board_id for t in self.tasks):
            raise ValueError("Task title already exists in this board")

        new_task = {"id": len(self.tasks) + 1,
                    'creation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'task_status': "Open",
                    **task.dict()}

        self.tasks.append(new_task)
        self._save_task_data()
        return new_task["id"]

    def update_task_status(self, task_id, update: TaskStatusUpdate):
        """
        :param request: A json string with the user details
        {
            "id" : "<task_id>",
            "status" : "OPEN | IN_PROGRESS | COMPLETE"
        }
        """
        task = self.get_task_by_id(task_id)

        task["task_status"] = update.status
        self._save_task_data()

    def list_boards(self) -> List[BoardList]:
        """
        :param

        :return:
        [
          {
            "id" : "<board_id>",
            "name" : "<board_name>"
          }
        ]
        """
        self._load_board_data()
        return [
            BoardList(**board)
            for board in self.boards
            if board["board_status"] != 'Closed'
        ]

    def list_boards_of_a_team(self, team_id: int) -> List[BoardList]:
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<board_id>",
            "name" : "<board_name>"
          }
        ]
        """
        self._load_board_data()
        return [
            BoardList(**board)
            for board in self.boards
            if board["board_status"] != 'Closed' and board["team_id"] == team_id
        ]

    def list_tasks_in_board(self, board_id: int) -> List[TaskList]:
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:

        """
        self._load_task_data()
        return [
            TaskList(**task)
            for task in self.tasks
            if task["task_status"] != 'Closed' and task["board_id"] == board_id
        ]

    def get_board(self, board_id: int) -> dict:
        self._load_board_data()

        for board in self.boards:
            if board["id"] == board_id:
                return board
        raise ValueError("Board not found")

    def get_task_by_id(self, task_id: int) -> dict:
        self._load_task_data()

        for task in self.tasks:
            if task["id"] == task_id:
                return task
        raise ValueError("Task not found")

    def get_board_by_task_id(self, task_id: int) -> dict:
        for board in self.boards:
            for task in board["tasks"]:
                if task["id"] == task_id:
                    return board
        raise ValueError("Task not found")

    def export_board(self) -> str:
        """
        Export a board in the out folder. The output will be a txt file.
        We want you to be creative. Output a presentable view of the board and its tasks with the available data.
        :param request:
        {
          "id" : "<board_id>"
        }
        :return:
        {
          "out_file" : "<name of the file created>"
        }
        """
        # Open the JSON file
        self._load_board_data()
        self._load_task_data()

        team_data = TeamBase().get_all_team_data()
        user_data = UserController().get_all_user_data()

        user_list = {
            item["id"]: {"user_id": item["id"], "user_name": item["name"], "display_name": item["display_name"]}
            for item in user_data
        }

        team_list = {
            item["id"]: {"name": item["name"], "description": item["description"],
                         "creation_time": datetime.fromisoformat(item["creation_time"])}
            for item in team_data
        }

        task_list_by_board = {}
        for task in self.tasks:
            board = task_list_by_board.get(task["board_id"], [])
            board.append({
                "task_id": task["id"],
                "task_title": task["title"],
                "description": task["description"],
                "user_id": task["user_id"],
                "user_name": user_list[task["user_id"]]["user_name"],
                "user_display_name": user_list[task["user_id"]]["user_name"],
                "task_status": task["task_status"],
                "creation_time": task["creation_time"],
            })
            task_list_by_board[task["board_id"]] = board

        response = []

        for board in self.boards:
            response.append({
                "board_id": board["id"],
                "board_name": board["name"],
                "description": board["description"],
                "team_id": board["team_id"],
                "team_name": team_list[board["team_id"]]["name"],
                "team_description": team_list[board["team_id"]]["description"],
                "tasks": task_list_by_board.get(board["id"], []),
                "board_creation_time": board["creation_time"],
                "board_status": board["board_status"],
            })

        export_file_path = os.path.join("output", 'output.txt')

        # Export the data to a TXT file
        with open(export_file_path, "w") as f:
            f.write(str(response))

        # Return a success message
        return export_file_path
