def make_reports(self, stats, old_stats):
    """render registered reports"""
    sect = Section('Report', '%s statements analysed.' % self.stats['statement'])
    for checker in self.report_order():
        for (reportid, r_title, r_cb) in self._reports[checker]:
            if not self.report_is_enabled(reportid):
                continue
            report_sect = Section(r_title)
            try:
                r_cb(report_sect, stats, old_stats)
            except EmptyReportError:
                continue
            report_sect.report_id = reportid
            sect.append(report_sect)
    return sect