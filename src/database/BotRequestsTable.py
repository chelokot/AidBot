# AidBot - Telegram bot project for finding volunteer help using semantic search
# Copyright (C) 2023
# Anastasia Mayorova aka EternityRei  <anastasiamayorova2003@gmail.com>
#    Andrey Vlasenko aka    chelokot   <andrey.vlasenko.work@gmail.com>
import psycopg

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or any later version. This
# program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details. You should have received a copy of the GNU General Public License along with this program. If not,
# see <https://www.gnu.org/licenses/>.

from src.database.DatabaseConnection import DatabaseConnection
from src.database.ProposalsRequestsTable import ProposalsRequestsTable
from src.database.data_types.BotRequest import BotRequest
from src.config.DatabaseConfig import user_table_name
from src.database.data_types.ColumnNames import ColumnNames
from pgvector.psycopg import register_vector


class BotRequestsTable(ProposalsRequestsTable):
    __conn = DatabaseConnection()

    def __init__(self):
        super().__init__()
        self.connection = self.__conn.get_instance().conn   # type: psycopg.connection.Connection
        self.all_string_columns_names = ColumnNames.all_bot_request_string_columns_names


