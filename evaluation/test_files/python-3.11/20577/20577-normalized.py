def _write_row_into_ods(ods, sheet_no, row_no, row):
    """
    Write row with translations to ods file into specified sheet and row_no.
    """
    ods.content.getSheet(sheet_no)
    for j, col in enumerate(row):
        cell = ods.content.getCell(j, row_no + 1)
        cell.stringValue(_escape_apostrophe(col))
        if j % 2 == 1:
            cell.setCellColor(settings.EVEN_COLUMN_BG_COLOR)
        else:
            cell.setCellColor(settings.ODD_COLUMN_BG_COLOR)