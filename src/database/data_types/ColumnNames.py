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
    proposal_description = "description"
    proposal_contact     = "contact"
    proposal_comment     = "comment"
    proposal_location    = "location"
    proposal_services    = "services"
    proposal_date_time   = "date_time"
    proposal_embedding   = "embedding"

    proposal_string_columns_names = [
        proposal_name, proposal_description, proposal_contact, proposal_comment, proposal_location,
        proposal_services, proposal_date_time
    ]

    length = {
        proposal_name: 300,
        proposal_description: 2000,
        proposal_contact: 300,
        proposal_comment: 2000,
        proposal_location: 300,
        proposal_services: 2000,
        proposal_date_time: 300,
    }
