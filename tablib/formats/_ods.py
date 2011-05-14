# -*- coding: utf-8 -*-

""" Tablib - ODF Support.
"""

import sys


if sys.version_info[0] > 2:
    from io import BytesIO
else:
    from cStringIO import StringIO as BytesIO

from tablib.compat import opendocument, style, table, text, unicode

title = 'ods'
extentions = ('ods',)

bold = style.Style(name='Bold', family="text")
bold.addElement(style.TextProperties(fontweight="bold"))

def export_set(dataset):
    """Returns ODF representation of Dataset."""

    wb = opendocument.OpenDocumentSpreadsheet()
    wb.automaticstyles.addElement(bold)

    ws = table.Table(name=dataset.title if dataset.title else 'Tablib Dataset')
    wb.spreadsheet.addElement(ws)
    dset_sheet(dataset, ws)

    stream = BytesIO()
    wb.save(stream)
    return stream.getvalue()


def export_book(databook):
    """Returns ODF representation of DataBook."""

    wb = opendocument.OpenDocumentSpreadsheet()
    wb.automaticstyles.addElement(bold)

    for i, dset in enumerate(databook._datasets):
        ws = table.Table(name=dset.title if dset.title else 'Sheet%s' % (i))
        wb.spreadsheet.addElement(ws)
        dset_sheet(dset, ws)


    stream = BytesIO()
    wb.save(stream)
    return stream.getvalue()


def dset_sheet(dataset, ws):
    """Completes given worksheet from given Dataset."""
    _package = dataset._package(dicts=False)

    for i, sep in enumerate(dataset._separators):
        _offset = i
        _package.insert((sep[0] + _offset), (sep[1],))

    for i, row in enumerate(_package):
        row_number = i + 1
        odf_row = table.TableRow(stylename=bold)
        for j, col in enumerate(row):
            ws.addElement(table.TableColumn())

            # bold headers
            if (row_number == 1) and dataset.headers:
                odf_row.setAttribute('stylename', bold)
                ws.addElement(odf_row)
                cell = table.TableCell()
                cell.addElement(text.P(stylename="Bold", text=unicode(col, errors='ignore')))
                odf_row.addElement(cell)

            # bold separators
            elif len(row) < dataset.width:
                ws.addElement(odf_row)
                cell = table.TableCell()
                cell.addElement(text.P(text=unicode(col, errors='ignore')))
                odf_row.addElement(cell)

            # wrap the rest
            else:
                try:
                    if '\n' in col:
                        ws.addElement(odf_row)
                        cell = table.TableCell()
                        cell.addElement(text.P(text=unicode(col, errors='ignore')))
                        odf_row.addElement(cell)
                    else:
                        ws.addElement(odf_row)
                        cell = table.TableCell()
                        cell.addElement(text.P(text=unicode(col, errors='ignore')))
                        odf_row.addElement(cell)
                except TypeError:
                    ws.addElement(odf_row)
                    cell = table.TableCell()
                    cell.addElement(text.P(text=unicode(col, errors='ignore')))
                    odf_row.addElement(cell)


