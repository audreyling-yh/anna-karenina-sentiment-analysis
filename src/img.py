import pandas as pd
from bokeh.plotting import figure, ColumnDataSource
from bokeh.palettes import Set2_8 as palette1
from bokeh.palettes import Set1_3 as palette2
from bokeh.io import output_file, save
from bokeh.layouts import column
import itertools

class Image:
    def __init__(self, calc_filepath, output_filepath):
        self.calc_filepath = calc_filepath
        self.output_filepath = output_filepath

        self.data = None

    def run(self):
        self.read_file()
        self.get_img()

    def read_file(self):
        self.data = pd.read_csv(calc_filepath, encoding = 'utf-8')

    def get_img(self):
        source = ColumnDataSource(self.data)

        TOOLTIPS = [
            ('part', '@part_int'),
            ('chapter', '@chapter_int'),
            ('topic_model', '@topic_1')
        ]

        output_file(self.output_filepath)
        colors_emotions = itertools.cycle(palette1)
        bk_emotions = figure(title = 'The narrative of Anna Karenina', plot_width = 1200, plot_height = 400,
                             tooltips = TOOLTIPS)
        for i in ['anger', 'trust', 'surprise', 'joy', 'sadness', 'disgust', 'anticipation', 'fear']:
            bk_emotions.line(x = 'idx', y = i, color = next(colors_emotions), legend_label = i, source = source)
        bk_emotions.xaxis.axis_label = 'Chapter number'
        bk_emotions.yaxis.axis_label = 'Emotion score'

        colors_sentiments = itertools.cycle(palette2)
        bk_sentiments = figure(plot_width = 1200, plot_height = 400, tooltips = TOOLTIPS)
        for i in ['positive', 'negative']:
            bk_sentiments.line(x = 'idx', y = i, color = next(colors_sentiments), legend_label = i, source = source)
        bk_sentiments.xaxis.axis_label = 'Chapter number'
        bk_sentiments.yaxis.axis_label = 'Sentiment score'

        p = column(bk_emotions, bk_sentiments)
        save(p)


if __name__ == '__main__':
    calc_filepath = '../data/calc/anna-karenina_scored_by-chapter.csv'
    output_filepath = '../data/img/anna-karenina_img_by-chapter.html'
    im = Image(calc_filepath, output_filepath)
    im.run()