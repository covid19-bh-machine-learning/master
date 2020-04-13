
__author__ = 'Aneesh Panoli'

# written for global biohackathon https://github.com/covid19-bh-machine-learning

import pandas as pd
from collections import Counter

#bokeh
from bokeh.transform import linear_cmap
from bokeh.models import ColorBar, ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.models import HoverTool
from bokeh.core.properties import value
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from IPython.display import display, HTML
from bokeh.transform import factor_cmap, factor_mark

global DATA

import ipywidgets as widgets
import numpy as np
from bokeh.plotting import reset_output
from bokeh.io import push_notebook, show, output_notebook
from bokeh.plotting import figure


from ipywidgets import Button, HBox, VBox

#custom functions
from Bio import SeqIO
from Bio.Alphabet import generic_protein
from skbio import Protein
from pathlib import Path
import os
import logging
from collections import defaultdict
import numpy as np
import requests
import wget




class FastaMeta:
    '''
    object to hold fasta file and its corresponding meta file paths
    '''
    def __init__(self, fasta, meta):
        '''
        fasta: .fa file name
        meta: .csv file name
        '''
        self.data_path = 'https://raw.githubusercontent.com/covid19-bh-machine-learning/master/master/data/'
        self.fasta = os.path.join(self.data_path, fasta)
        self.meta = os.path.join(self.data_path, meta)

class DataProcessing(FastaMeta):
    def __init__(self, fasta, meta):
        super().__init__(fasta, meta)

    def get_amino_df(self, k):
        '''
        k = kmer length
        Generates all possible offsets of amino acid sequence and
        returns a pandas dataframe merged with given metadata
        meta_format ; csv tsv etc
        '''
        meta_df = pd.read_csv(self.meta, header=0)
        seq_seq = defaultdict(list)
        filename = wget.download(self.fasta)
        seq_list = list(SeqIO.parse(filename, 'fasta', alphabet=generic_protein))
        for s in seq_list:
            for i in range(k):
                seq_seq[f'seq_offset_{i}'].append(str(s.seq)[i:])
        for key in seq_seq:
            meta_df[key] = seq_seq[key]
        return meta_df

def get_dashboard():
    global amino_df
    orf1 = DataProcessing('coronavirus_orf1ab.fasta', 'coronavirus_orf1ab_meta.csv')
    # read for data folder and out put
    offset, kmer = 4, 4 # number of bases to offset
    amino_df = orf1.get_amino_df(offset)
    print(f"shape WITH duplicates: {amino_df.shape}")

    # remove duplicates
    amino_df.drop_duplicates(subset='Accession', keep=False, inplace=True)
    print(f"shape WITHOUT duplicates: {amino_df.shape}")
    amino_df['Collection_Date'] = pd.to_datetime(amino_df['Collection_Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    amino_df['Release_Date'] = pd.to_datetime(amino_df['Release_Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    amino_df['Length'] = amino_df['Length'].apply(str)



    output_notebook()

    def get_count_data(df, column, row=None):
        counts = Counter(df[column])
        if not counts:
            return ColumnDataSource(data={column: ['None Found'], 'Count':[counts['None Found']]})
        if counts.get(np.nan):
            counts.pop(np.nan)
        print(f"Total number of {column}s:{len(counts)}")
        if row:
            globals()['DATA'] = df[df[column] == row]
            return ColumnDataSource(data={column: [row], 'Count':[counts[row]]})
        return ColumnDataSource(data={column:list(counts.keys()), 'Count':list(counts.values())})

    def bokeh_plot_vbar(column, source):
    #     source = ColumnDataSource(data=get_count_data(column, row))
        mapper = linear_cmap(field_name='Count', palette=Spectral6 ,low=min(source.data['Count']) ,high=max(source.data['Count']))

        p = figure(x_range=list(map(str, source.data[column])), plot_height=400, plot_width=750, title=f"{column}".title(),
                   toolbar_location='right')
        pv = p.vbar(x=column, top='Count', width=0.9, source=source, color=mapper)
        p.add_tools(HoverTool(
        #     renderers=[pv],
            tooltips=[
                ( column,   '@'+column            ), #state
                ( 'Count',  '@'+'Count'            ), #count
            ],

            formatters={

            },

            # display a tooltip whenever the cursor is vertically in line with a glyph
            mode='vline'
                      ))

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.xaxis.visible = False
        p.yaxis.axis_label = 'Number of sequences'
        output_file("bars.html")
        save(p)
        display(HTML('bars.html'))

    ALL = 'ALL'
    def unique_sorted_values_plus_ALL(array):
        unique = array.unique().tolist()
        unique.sort()
        unique.insert(0, ALL)
        return unique

    align_kw = dict(
        _css = (('.widget-label', 'min-width', '20ex'),),
        margin = '0px 0px 5px 12px'
    )

    dropdown_values = widgets.Dropdown()
    df_columns = ['Release_Date', 'Species', 'Length', 'Geo_Location',
           'Host', 'Isolation_Source', 'Collection_Date', 'GenBank_Title']
    dropdown_columns = widgets.Dropdown(options = df_columns)
    dropdown_columns1 = widgets.Dropdown(options = df_columns)
    output_values= widgets.Output(wait=True)
    output_widget = widgets.Output(wait=True)
    output_columns1 = widgets.Output(wait=True)



    def dropdown_columns_eventhandler(change):
        output_columns1.clear_output()
        output_widget.clear_output()
        output_values.clear_output()
        with output_widget:
            dropdown_values = widgets.Dropdown(
                options = unique_sorted_values_plus_ALL(amino_df[change.new].dropna()))
            dropdown_values.observe(dropdown_values_eventhandler, names='value')
            display(dropdown_values)
        with output_values:
            source = get_count_data(amino_df, change.new)
            bokeh_plot_vbar(change.new, source)
            display(amino_df)

    def dropdown_colums1_eventhandler(change):
        output_values.clear_output()
        with output_values:

            source = get_count_data(DATA, change.new)
            bokeh_plot_vbar(change.new, source)
            display(DATA)

    def dropdown_values_eventhandler(change):
        output_values.clear_output()
        output_columns1.clear_output()
        with output_values:
            if (change.new == ALL):
                source = get_count_data(amino_df, dropdown_columns.value)
                bokeh_plot_vbar(dropdown_columns.value, source)
                display(amino_df)

            else:
                source = get_count_data(amino_df, dropdown_columns.value, change.new)
                bokeh_plot_vbar(dropdown_columns.value, source)
                display(amino_df[amino_df[dropdown_columns.value] == change.new])
        if (change.new != ALL):
            with output_columns1:
                dropdown_columns1 = widgets.Dropdown(
                    options = [i for i in df_columns if i!= dropdown_columns.value])
                dropdown_columns1.observe(dropdown_colums1_eventhandler, names='value')
                display(dropdown_columns1)

    dropdown_values.observe(dropdown_values_eventhandler, names='value')
    dropdown_columns.observe(dropdown_columns_eventhandler, names='value')

    box_layout = widgets.Layout(display='flex-grow',
                        flex_flow='row',
                        align_items='stretch',
                        border='None',
                        width='100%',
                        )
    box = widgets.Box(
        children=[dropdown_columns, output_widget, output_columns1], layout=box_layout)
    print('Eplore the dataset here')

    display(box)
    display(output_values)
