# AidBot - Telegram bot project for finding volunteer help using semantic search
# Copyright (C) 2023
# Anastasia Mayorova aka EternityRei  <anastasiamayorova2003@gmail.com>
#    Andrey Vlasenko aka    chelokot   <andrey.vlasenko.work@gmail.com>

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or any later version. This
# program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details. You should have received a copy of the GNU General Public License along with this program. If not,
# see <https://www.gnu.org/licenses/>.

from src.database.data_types.ColumnNames import ColumnNames
from src.database.data_types.ProposalRequest import ProposalRequest
from src.config.DatabaseConfig import site_table_name


class ProposalsTableUtils:
    @staticmethod
    def _format_column_names() -> str:
        """
        :return: string with all column names in format (column1, column2, ...)

        Used in INSERT INTO query
        """
        columns = [ColumnNames.id] + ColumnNames.proposal_string_columns_names + [ColumnNames.proposal_embedding]
        return "(" + ", ".join(columns) + ")"

    @staticmethod
    def _format_string_column_names() -> str:
        """
        :return: string with all string column names in format (column1, column2, ...)

        Used in INSERT INTO query
        """
        columns = ColumnNames.proposal_string_columns_names
        return "(" + ", ".join(columns) + ")"

    @staticmethod
    def _format_single_column_value(proposal: ProposalRequest, column_name: str) -> str:
        """
        Simple function to format column value in INSERT INTO query
        It adds quotes and cuts string if it is too long
        """
        return "'" + proposal.get_characteristic(column_name)[:ColumnNames.length[column_name]].replace("'", "") + "'"

    @staticmethod
    def _formal_column_values(proposal: ProposalRequest) -> str:
        """
        :return: string with column values in format (value1, value2, ...)

        Used in INSERT INTO query
        """
        values = ["default"] \
                 + [ProposalsTableUtils._format_single_column_value(proposal, column) for column in
                    ColumnNames.proposal_string_columns_names] \
                 + ["'" + str(proposal.embedding.get_list()) + "'"]
        return "(" + ", ".join(values) + ")"

    @staticmethod
    def _get_insert_query(proposal: ProposalRequest) -> str:
        """
        :return: string with INSERT INTO query in format
        INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...)
        """
        return f"""INSERT INTO {site_table_name} 
            {ProposalsTableUtils._format_column_names()} 
            VALUES {ProposalsTableUtils._formal_column_values(proposal)}"""