# anna-karenina-sentiment-analysis
A lexicon-based sentiment and emotion analysis of Anna Karenina by Leo Tolstoy using the NRC lexicon. The book contains 8 parts, of which each part contains an average of 25 chapters.

### About
There are four parts to this analysis:
- src/puller.py -- pulls raw html from https://www.gutenberg.org/files/1399/1399-h/1399-h.htm
- src/process.py -- cleans the html, aggregates text by chapter to csv
- src/calc.py -- calculate sentiment and emotion scores
- src/img.py -- visualise the scores using bokeh interactive plot

Final output: data/img/

### Resources
The lexicon used in this analysis is NRC Word-Emotion Association (EmoLex). It is available for download at http://sentiment.nrc.ca/lexicons-for-research/. The corpus of Anna Karenina is available at https://www.gutenberg.org/files/1399/1399-h/1399-h.htm.


