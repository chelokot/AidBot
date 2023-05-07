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


class ColumnNames:
    id                   = "id"

    proposal_name        = "name"
    description          = "description"
    proposal_contact     = "contact"
    proposal_comment     = "comment"
    proposal_location    = "location"
    proposal_services    = "services"
    proposal_date_time   = "date_time"
    proposal_embedding   = "embedding"

    bot_request_start    = "start"
    bot_request_amount   = "amount"
    bot_request_answer_message_id = "answer_message_id"

    all_proposal_string_columns_names = [
        proposal_name, description, proposal_contact, proposal_comment, proposal_location,
        proposal_services, proposal_date_time
    ]

    all_bot_request_string_columns_names = [
        description, bot_request_start, bot_request_amount, bot_request_answer_message_id
    ]

    types = {
        proposal_name:      "varchar(300)",
        description:        "varchar(2000)",
        proposal_contact:   "varchar(300)",
        proposal_comment:   "varchar(2000)",
        proposal_location:  "varchar(300)",
        proposal_services:  "varchar(2000)",
        proposal_date_time: "varchar(300)",

        bot_request_start:  "integer",
        bot_request_amount: "integer",
        bot_request_answer_message_id: "bigint",
    }
