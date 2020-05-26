import ast
import pandas as pd
from pandas.io.json import json_normalize
import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import gensim
from gensim import corpora
import pickle

class Calc:
    def __init__(self, clean_filepath, lexicon_filepath, output_filepath_para, output_filepath_chapter):
        self.clean_filepath = clean_filepath
        self.lexicon_filepath = lexicon_filepath
        self.output_filepath_para = output_filepath_para
        self.output_filepath_chapter = output_filepath_chapter

        self.data = None
        self.lex = None
        self.data_chpt = None

    def run(self):
        self.read_files()
        self.clean_paragraphs()
        self.get_scores()
        self.group_by_chapter()
        self.topic_modeling()
        self.to_csv()

    def read_files(self):
        self.data = pd.read_csv(self.clean_filepath)
        self.lex = pd.read_csv(self.lexicon_filepath, names=['word', 'emotion', 'score'], sep='\t')

    def clean_paragraphs(self):
        self.data['paragraph_c'] = self.data['paragraph'].apply(self.cleaner)
        self.data['para_no'] = self.data.index + 1
        self.data['part_int'] = self.data['part'].apply(self.map_part)
        self.data['chapter_int'] = self.data['chapter'].apply(lambda x: int(x.replace('Chapter ', '')))

    def cleaner(self, val):
        para = val.strip().lower()
        para = ' '.join(re.findall('[a-zA-Z]+', para))
        para = para.split(' ')
        para = [x for x in para if x not in stopwords.words('english')]
        para = [WordNetLemmatizer().lemmatize(x) for x in para if x not in stopwords.words('english')]
        return para

    def get_scores(self):
        # get scores by paragraph
        emotions = self.lex['emotion'].unique()
        words = self.lex['word'].unique()
        zero_dict = {}
        for e in emotions:
            zero_dict[e] = 0

        for idx, val in self.data['paragraph_c'].iteritems():
            zero_dict_c = zero_dict.copy()
            for word in val:
                if word in words:
                    scores = self.lex[self.lex['word'] == word][['emotion', 'score']]
                    score_dict = scores.set_index('emotion').to_dict()

                    for k, v in score_dict['score'].items():
                        zero_dict_c[k] += v
            self.data.loc[idx, 'score'] = str(zero_dict_c)

    def group_by_chapter(self):
        data = self.data.copy(deep = True)
        data['score'] = data['score'].apply(lambda x: ast.literal_eval(x))
        emotion_df = json_normalize(data['score'])
        merged_df = data.merge(emotion_df, left_index=True, right_index=True)
        chpt_agg = merged_df.groupby(['part_int', 'chapter_int'])[emotion_df.columns].sum()

        agg_text = pd.DataFrame(merged_df.groupby(['part_int', 'chapter_int'])['paragraph_c'].apply(list)).reset_index()
        agg_text.rename(columns = {'paragraph_c': 'chapter_corpus_c'}, inplace=True)
        chpt_agg = chpt_agg.merge(agg_text, on = ['part_int', 'chapter_int'])
        chpt_agg.reset_index(inplace = True)
        chpt_agg['idx'] = chpt_agg.index
        self.data_chpt = chpt_agg

    def topic_modeling(self):
        self.dictionary = corpora.Dictionary()
        for idx, val in self.data_chpt.iterrows():
            chpt = val['chapter_corpus_c']
            self.dictionary.add_documents(chpt)
        self.data_chpt['topic_1'], self.data_chpt['topic_2'], self.data_chpt['topic_3'] = zip(*self.data_chpt['chapter_corpus_c'].map(self.lda))

    def lda(self, chpt):
        chpt_corpus = []
        for x in chpt:
            for i in x:
                chpt_corpus.append(i)
        corpus = [self.dictionary.doc2bow(chpt_corpus)]
        pickle.dump(corpus, open('../data/lda/corpus.pkl', 'wb'))
        self.dictionary.save('../data/lda/dictionary.gensim')

        NUM_TOPICS = 3
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word = self.dictionary)
        ldamodel.save('../data/lda/ldamodel_anna-karenina.gensim')
        topics = ldamodel.print_topics(num_words = 10)
        topic_1 = topics[0]
        topic_2 = topics[1]
        topic_3 = topics[2]
        return topic_1, topic_2, topic_3


    def map_part(self, string):
        num = 0
        if 'ONE' in string:
            num = 1
        elif 'TWO' in string:
            num = 2
        elif 'THREE' in string:
            num = 3
        elif 'FOUR' in string:
            num = 4
        elif 'FIVE' in string:
            num = 5
        elif 'SIX' in string:
            num = 6
        elif 'SEVEN' in string:
            num = 7
        elif 'EIGHT' in string:
            num = 8
        return num

    def to_csv(self):
        self.data.to_csv(self.output_filepath_para, index = False)
        self.data_chpt.to_csv(self.output_filepath_chapter, index = False)



if __name__ == '__main__':
    clean_filepath = '../data/clean/anna-karenina_by-paragraph.csv'
    lexicon_filepath = '../NRC-Emotion-Lexicon-Wordlevel-v0.92.txt'
    output_filepath_para = '../data/calc/anna-karenina_scored_by-paragraph.csv'
    output_filepath_chapter = '../data/calc/anna-karenina_scored_by-chapter.csv'
    c = Calc(clean_filepath, lexicon_filepath, output_filepath_para, output_filepath_chapter)
    c.run()

