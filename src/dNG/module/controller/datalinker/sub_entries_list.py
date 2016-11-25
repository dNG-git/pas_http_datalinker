# -*- coding: utf-8 -*-

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;http;datalinker

The following license agreement remains valid unless any additions or
changes are being made by direct Netware Group in a written form.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(pasHttpDataLinkerVersion)#
#echo(__FILEPATH__)#
"""

import re

from dNG.data.data_linker import DataLinker
from dNG.data.hookable_settings import HookableSettings
from dNG.data.http.translatable_error import TranslatableError
from dNG.data.ownable_mixin import OwnableMixin as OwnableInstance
from dNG.data.rfc.basics import Basics as RfcBasics
from dNG.data.settings import Settings
from dNG.data.text.date_time import DateTime
from dNG.data.text.input_filter import InputFilter
from dNG.data.text.l10n import L10n
from dNG.data.xhtml.link import Link
from dNG.data.xhtml.oset.file_parser import FileParser
from dNG.data.xhtml.table.data_linker import DataLinker as DataLinkerTable
from dNG.data.xml_parser import XmlParser
from dNG.module.controller.services.abstract_dom_editor import AbstractDomEditor
from dNG.runtime.value_exception import ValueException

from .abstract_sub_entries import AbstractSubEntries

class SubEntriesList(AbstractDomEditor, AbstractSubEntries):
    """
"SubEntriesList" provides a dynamic list of child entries.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: datalinker
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
    """

    def execute_index(self):
        """
Action for "index"

:since: v0.2.00
        """

        if (self.request.is_dsd_set("oid")): self.execute_view()
    #

    def execute_render(self):
        """
Action for "render"

:since: v0.2.00
        """

        if (self._is_primary_action()): raise TranslatableError("core_access_denied", 403)

        if ("id" not in self.context): raise ValueException("Required sub entries list ID is missing")

        L10n.init("pas_http_datalinker")
        Settings.read_file("{0}/settings/pas_http_datalinker.json".format(Settings.get("path_data")))

        hookable_settings = HookableSettings("dNG.pas.http.datalinker.SubEntriesList.getDynamicLimit",
                                             oid = self.context['id']
                                            )

        limit = hookable_settings.get("pas_http_datalinker_sub_entries_dynamic_list_limit", 5)

        ( datalinker_object, content ) = self._get_datalinker_object_and_content(self.context['id'], limit)
        datalinker_object_data = datalinker_object.get_data_attributes("sub_entries", "sub_entries_type")
        session = (self.request.get_session() if (self.request.is_supported("session")) else None)

        if (isinstance(datalinker_object, OwnableInstance)
            and (not datalinker_object.is_readable_for_session_user(session))
           ): raise TranslatableError("core_access_denied", 403)

        content['table']['page_limit'] = 1

        if (content['sub_entries_count'] > limit):
            content['view_link_content'] = self._get_sub_entries_link_content(datalinker_object_data['sub_entries'], datalinker_object_data['sub_entries_type'])

            link_attributes = { "m": "datalinker",
                                "s": "sub_entries_list",
                                "dsd": { "oid": self.context['id'],
                                         "source": Link().build_url(Link.TYPE_QUERY_STRING, { "__request__": True })
                                       }
                              }

            content['view_link_query'] = Link().build_url(Link.TYPE_QUERY_STRING, link_attributes)
            content['view_link_url'] = Link().build_url(Link.TYPE_RELATIVE_URL, link_attributes)
        #

        self.set_action_result(FileParser().render("datalinker.sub_entries_list", content))
    #

    def execute_view(self):
        """
Action for "view"

:since: v0.2.00
        """

        _id = InputFilter.filter_control_chars(self.request.get_dsd("oid", ""))
        page = InputFilter.filter_int(self.request.get_dsd("dpage", 1))
        sort_value = InputFilter.filter_control_chars(self.request.get_dsd("dsort", ""))

        source_iline = InputFilter.filter_control_chars(self.request.get_dsd("source", "")).strip()

        L10n.init("pas_http_datalinker")
        Settings.read_file("{0}/settings/pas_http_datalinker.json".format(Settings.get("path_data")))

        is_dom_editor_response_instance_supported = self._check_response_instance_supported()

        if (source_iline != "" and (not is_dom_editor_response_instance_supported)):
            if (self.response.is_supported("html_css_files")): self.response.add_theme_css_file("mini_default_sprite.min.css")

            Link.set_store("servicemenu",
                           Link.TYPE_RELATIVE_URL,
                           L10n.get("core_back"),
                           { "__query__": re.sub("\\_\\_\\w+\\_\\_", "", source_iline) },
                           icon = "mini-default-back",
                           priority = 7
                          )
        #

        hookable_settings = HookableSettings("dNG.pas.http.datalinker.SubEntriesList.getLimit",
                                             oid = _id
                                            )

        limit = hookable_settings.get("pas_http_datalinker_sub_entries_list_limit", 30)

        ( datalinker_object, content ) = self._get_datalinker_object_and_content(_id, limit)
        session = (self.request.get_session() if (self.request.is_supported("session")) else None)

        if (isinstance(datalinker_object, OwnableInstance)
            and (not datalinker_object.is_readable_for_session_user(session))
           ): raise TranslatableError("core_access_denied", 403)

        content['table']['dsd_page_key'] = "dpage"
        content['table']['page'] = page

        content['table']['dsd_sort_key'] = "dsort"
        content['table']['sort_value'] = sort_value

        if (is_dom_editor_response_instance_supported): self._set_append_overlay_dom_oset_result("datalinker.sub_entries_list_overlay", content)
        else:
            self.response.init(True)
            self.response.set_expires_relative(+15)
            self.response.set_title(content['title'])

            self.response.add_oset_content("datalinker.sub_entries_list", content)
        #
    #

    def _get_datalinker_object_and_content(self, _id, limit = -1):
        """
Returns a tuple containing the DataLinker object and a content dictionary
ready for output.

:param _id: DataLinker ID
:param limit: Maximum number of DataLinker sub entries

:return: (tuple) DataLinker object and content dictionary
:since:  v0.2.00
        """

        datalinker_object = DataLinker.load_id(_id)

        datalinker_object_data = datalinker_object.get_data_attributes("id", "title", "sub_entries", "sub_entries_type")

        title = self._get_sub_entries_title(datalinker_object_data['sub_entries_type'])
        if (title == ""): title = L10n.get("pas_http_datalinker_sub_entries")

        content = { "id": "pas_http_datalinker_{0:d}".format(id(self)),
                    "title": datalinker_object_data['title'],
                    "sub_entries_count": datalinker_object_data['sub_entries'],
                    "sub_entries_title": title
                  }

        title_renderer_attributes = { "type": DataLinkerTable.COLUMN_RENDERER_CALLBACK,
                                      "callback": self._get_title_cell_content
                                    }

        time_sortable_renderer_attributes = { "type": DataLinkerTable.COLUMN_RENDERER_CALLBACK,
                                              "callback": self._get_time_sortable_cell_content
                                            }

        table = DataLinkerTable(datalinker_object)
        table.add_column("title", title, 75, renderer = title_renderer_attributes)
        table.add_column("time_sortable", L10n.get("pas_http_datalinker_entry_updated"), 25, renderer = time_sortable_renderer_attributes)

        table.add_sort_definition("position", DataLinkerTable.SORT_DESCENDING)
        table.add_sort_definition("time_sortable", DataLinkerTable.SORT_DESCENDING)
        table.disable_sort("title", "time_sortable")

        table.set_limit(limit)

        content['table'] = { "id": datalinker_object_data['id'],
                             "object": table
                           }

        return ( datalinker_object, content )
    #

    def _get_time_sortable_cell_content(self, content, column_definition):
        """
Returns content used for "time_sortable" cell rendering.

:param content: Content already defined
:param column_definition: Column definition for the cell

:return: (dict) Content used for rendering
:since:  v0.2.00
        """

        time_attributes = { "tag": "time", "attributes": { "datetime": "{0}+00:00".format(RfcBasics.get_iso8601_datetime(content['time_sortable'])) } }

        return "{0}{1}</time>".format(XmlParser().dict_to_xml_item_encoder(time_attributes, False),
                                      DateTime.format_l10n(DateTime.TYPE_FUZZY_MONTH, content['time_sortable'])
                                     )
    #

    def _get_title_cell_content(self, content, column_definition):
        """
Returns content used for title cell rendering.

:param content: Content already defined
:param column_definition: Column definition for the cell

:return: (dict) Content used for rendering
:since:  v0.2.00
        """

        return self._render_link(content)
    #
#
