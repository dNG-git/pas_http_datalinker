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

from .abstract_row import AbstractRow

class DataLinkerRow(AbstractRow):
    """
"DataLinkerRow" provides properties mapped to DataLinker entry attributes.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: datalinker
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
    """

    def __init__(self, entry):
        """
Constructor __init__(DataLinkerRow)

:param entry: DataLinker entry

:since: v0.2.00
        """

        self.entry = entry
        """
DataLinker entry to iterate
        """
    #

    def __contains__(self, item):
        """
python.org: Called to implement membership test operators.

:param item: Item to be looked up

:return: (bool) True if "__getitem__()" call will be successfully
:since:  v0.2.00
        """

        return (type(item) is str)
    #

    def __getitem__(self, key):
        """
python.org: Called to implement evaluation of self[key].

:param name: Attribute name

:return: (mixed) Attribute value
:since:  v0.2.00
        """

        return self.entry.get_data_attributes(key)[key]
    #
#
