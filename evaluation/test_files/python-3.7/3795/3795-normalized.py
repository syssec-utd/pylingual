def iplot_histogram(data, figsize=None, number_to_keep=None, sort='asc', legend=None):
    """ Create a histogram representation.

        Graphical representation of the input array using a vertical bars
        style graph.

        Args:
            data (list or dict):  This is either a list of dicts or a single
                dict containing the values to represent (ex. {'001' : 130})
            figsize (tuple): Figure size in pixels.
            number_to_keep (int): The number of terms to plot and
                rest is made into a single bar called other values
            sort (string): Could be 'asc' or 'desc'
            legend (list): A list of strings to use for labels of the data.
                The number of entries must match the length of data.
        Raises:
            VisualizationError: When legend is provided and the length doesn't
                match the input data.
    """
    html_template = Template('\n    <p>\n        <div id="histogram_$divNumber"></div>\n    </p>\n    ')
    javascript_template = Template('\n    <script>\n        requirejs.config({\n            paths: {\n                qVisualization: "https://qvisualization.mybluemix.net/q-visualizations"\n            }\n        });\n\n        require(["qVisualization"], function(qVisualizations) {\n            qVisualizations.plotState("histogram_$divNumber",\n                                      "histogram",\n                                      $executions,\n                                      $options);\n        });\n    </script>\n    ')
    div_number = str(time.time())
    div_number = re.sub('[.]', '', div_number)
    if figsize is None:
        figsize = (7, 5)
    options = {'number_to_keep': 0 if number_to_keep is None else number_to_keep, 'sort': sort, 'show_legend': 0, 'width': int(figsize[0]), 'height': int(figsize[1])}
    if legend:
        options['show_legend'] = 1
    data_to_plot = []
    if isinstance(data, dict):
        data = [data]
    if legend and len(legend) != len(data):
        raise VisualizationError("Length of legendL (%s) doesn't match number of input executions: %s" % (len(legend), len(data)))
    for (item, execution) in enumerate(data):
        exec_data = process_data(execution, options['number_to_keep'])
        out_dict = {'data': exec_data}
        if legend:
            out_dict['name'] = legend[item]
        data_to_plot.append(out_dict)
    html = html_template.substitute({'divNumber': div_number})
    javascript = javascript_template.substitute({'divNumber': div_number, 'executions': data_to_plot, 'options': options})
    display(HTML(html + javascript))