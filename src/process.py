import codecs
from bs4 import BeautifulSoup
import pandas as pd

class Process:
    def __init__(self, raw_filepath, output_filename):
        self.raw_filepath = raw_filepath
        self.output_filename = output_filename

        self.content = None
        self.df = None

    def run(self):
        self.read()
        self.to_df()
        self.to_csv()

    def read(self):
        file = codecs.open(self.raw_filepath, 'r')
        soup = BeautifulSoup(file, 'html.parser')
        html = list(soup.children)[2]
        body = list(html.children)[3]
        self.content = body.find_all('div', class_= 'chapter')

    def to_df(self):
        df = pd.DataFrame(columns = ['part', 'chapter', 'paragraph'])
        for i in self.content:
            part = i.find_all('h2')
            for p in part:
                part_label = p.get_text()

            for txt in i.find_all(['h3', 'p'])[1:]:
                if 'Chapter ' in txt.get_text():
                    chpt_label = txt.get_text()
                else:
                    para = txt.get_text()

                    row = {'part': part_label,
                           'chapter': chpt_label,
                           'paragraph': para}
                    df = df.append(row, ignore_index=True)
        self.df = df

    def to_csv(self):
        filepath = '../data/clean/{}.csv'.format(self.output_filename)
        self.df.to_csv(filepath, index = False)

if __name__ == '__main__':
    raw_filepath = '../data/raw/anna-karenina.html'
    output_filename = 'anna-karenina_by-paragraph'
    pr = Process(raw_filepath, output_filename)
    pr.run()