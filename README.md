- [Haggle](#haggle)
- [Simple example](#simple-example)
  * [By the way...](#by-the-way)
- [Search results and dataset metadata](#search-results-and-dataset-metadata)
  * [.meta](#meta)
  * [Cached search info](#cached-search-info)
- [The boring stuff](#the-boring-stuff)
  * [Install](#install)
  * [API credentials](#api-credentials)
- [F.A.Q.](#faq)
  * [What if I don't want a zip file anymore?](#what-if-i-don-t-want-a-zip-file-anymore-)
  * [Do you have any jupyter notebooks demoing this.](#do-you-have-any-jupyter-notebooks-demoing-this)
  * [A little snippet of code to test?](#a-little-snippet-of-code-to-test-)


# Haggle

A simple facade to [Kaggle](https://www.kaggle.com/) data.

Essentially, instantiate a `KaggleDatasets` object, and from it...
- search for datasets from the python console (so much better than having pictures the [kaggle website](https://www.kaggle.com/) right?)
- download what you want and start using...
- ... oh, and it automatically caches the data zip and search results to local files
- ... oh, and all the while it pretends to be a humble dict with `owner/dataset` keys, and that's the coolest bit.

**Haggle:** /ˈhaɡəl/
- an instance of intense argument (as in bargaining) 
- wrangle (over a price, terms of an agreement, etc.) 
- rhymes with Kaggle and is not taken on pypi (well, now it is)

# Simple example


```python
from haggle import KaggleDatasets

rootdir = None  # define (or not) where you want the data to be cached/downloaded

s = KaggleDatasets(rootdir)  # make an instance

if 'rtatman/english-word-frequency' in s:
    del s['rtatman/english-word-frequency']  # just to prepare for the demo
```


```python
list(s)  # see what you have locally
```




    ['uciml/human-activity-recognition-with-smartphones',
     'sitsawek/phonetics-articles-on-plos']



Let's search something (you can also search on [kaggle](https://www.kaggle.com/), I was kidding about it being lame!)


```python
results = s.search('word frequency')
print(f"{len(results)=}")
list(results)[:10]
```

    len(results)=180




    ['rtatman/english-word-frequency',
     'yekenot/fasttext-crawl-300d-2m',
     'rtatman/japanese-lemma-frequency',
     'rtatman/glove-global-vectors-for-word-representation',
     'averkij/lingtrain-hungarian-word-frequency',
     'lukevanhaezebrouck/subtlex-word-frequency',
     'facebook/fatsttext-common-crawl',
     'facebook/fasttext-wikinews',
     'facebook/fasttext-english-word-vectors-including-subwords',
     'kushtej/kannada-word-frequency']



Chose what you want? Good, now do this:


```python
v = s['rtatman/english-word-frequency']
type(v)
```




    py2store.slib.s_zipfile.ZipReader



Okay, let's slow down a moment. What happened? What's this `ZipReader` thingy?

Well, what happened is that this downloaded the zip file of the data for you and saved it in `ROOTDIR/rtatman/english-word-frequency.zip`. Don't believe me? Go have a look. 

But then it also returns this object called `ZipReader` that points to it. 

If you don't like it, you don't have to use it. But I think you should like it.

Look at what it can do!

List the contents of file (that's in the zip... okay there's just one here, it's a bit boring)


```python
list(v)
```




    ['unigram_freq.csv']



Retrieve the data for any given file of the zip without ever having to unzip it!

Oh, and still pretending to be a dict. 


```python
b = v['unigram_freq.csv']
print(f"b is a {type(b)} and has {len(b)} bytes")
```

    b is a <class 'bytes'> and has 4956252 bytes


Now the data is given in bytes by default, since that's the basis of everything. 

From there you can go everywhere. Here for example, say we'd like to go to `pandas.DataFrame`...


```python
import pandas as pd
from io import BytesIO

df = pd.read_csv(BytesIO(b))
df.shape
```




    (333333, 2)




```python
print(df.head(7).to_string())
```

      word        count
    0  the  23135851162
    1   of  13151942776
    2  and  12997637966
    3   to  12136980858
    4    a   9081174698
    5   in   8469404971
    6  for   5933321709


And as mentioned, it caches the data to your local drive. You know, download, so that the next time you ask for `s['rtatman/english-word-frequency']`, it'll be faster to get those bytes.

See, let's list the contents of `s` again and see that we now have that `'rtatman/english-word-frequency'` key we didn't have before.


```python
list(s)
```




    ['uciml/human-activity-recognition-with-smartphones',
     'rtatman/english-word-frequency',
     'sitsawek/phonetics-articles-on-plos']




## By the way...

So a `KaggleDatasets` is a store with a dict-like interface. 

Listing happens locally. Remote listing is done through `.search(...)`.

Getting happens locally first, and if not, will get remotely (and cache locally).


Where are the zips stored? Ask `.zips_dir`:


```python
s.zips_dir
```




    '/D/Dropbox/_odata/kaggle/zips'



# Search results and dataset metadata

Let's have a closer look at those search results. All we did is a `len(results)` and a `list(results)`. What else can you do with that object?

Well, as is so happens, you can do whatever (read-only) operation you can do on a -- take a wild guess -- a dict. 

Namely, you can get a value for the keys we've listed


```python
from pprint import pprint
pprint(results['rtatman/english-word-frequency'])
```

    {'creatorName': 'Rachael Tatman',
     'creatorUrl': 'rtatman',
     'currentVersionNumber': 1,
     'description': None,
     'downloadCount': 3079,
     'files': [],
     'id': 2367,
     'isFeatured': False,
     'isPrivate': False,
     'isReviewed': True,
     'kernelCount': 12,
     'lastUpdated': '2017-09-06T18:21:27.18Z',
     'licenseName': 'Other (specified in description)',
     'ownerName': 'Rachael Tatman',
     'ownerRef': 'rtatman',
     'ref': 'rtatman/english-word-frequency',
     'subtitle': '⅓ Million Most Frequent English Words on the Web',
     'tags': [{'competitionCount': 3,
               'datasetCount': 231,
               'description': 'Language is a method of communication that consists '
                              'of using words arranged into meaningful patterns. '
                              'This is a good place to find natural language '
                              'processing datasets and kernels to study languages '
                              'and train your chat bots.',
               'fullPath': 'topic > culture and humanities > languages',
               'isAutomatic': False,
               'name': 'languages',
               'ref': 'languages',
               'scriptCount': 77,
               'totalCount': 311},
              {'competitionCount': 6,
               'datasetCount': 445,
               'description': 'The linguistics tag contains datasets and kernels '
                              'that you can use for text analytics, sentiment '
                              'analyses, and making clever jokes like this: Let me '
                              "tell you a little about myself. It's a reflexive "
                              'pronoun that means "me."',
               'fullPath': 'topic > people and society > social science > '
                           'linguistics',
               'isAutomatic': False,
               'name': 'linguistics',
               'ref': 'linguistics',
               'scriptCount': 122,
               'totalCount': 573},
              {'competitionCount': 18,
               'datasetCount': 4172,
               'description': 'An interconnected network of tubes that connects '
                              'the entire world together. This tag covers a broad '
                              'range of tags; anything from cryptocurrency to '
                              'website analytics.',
               'fullPath': 'topic > science and technology > internet',
               'isAutomatic': False,
               'name': 'internet',
               'ref': 'internet',
               'scriptCount': 198,
               'totalCount': 4388}],
     'title': 'English Word Frequency',
     'topicCount': 1,
     'totalBytes': 2236581,
     'url': 'https://www.kaggle.com/rtatman/english-word-frequency',
     'usabilityRating': 0.8235294,
     'versions': [],
     'viewCount': 21726,
     'voteCount': 105}


You get description, size, tags, download count... Useful stuff to make your choice. 

Personally, I like transform those results in a `DataFrame` that I can subsequently interrogate:


```python
import pandas as pd
df = pd.DataFrame(results.values())[['ref', 'title', 'subtitle', 'downloadCount', 'totalBytes']]
df = df.set_index('ref').sort_values('downloadCount', ascending=False)
# print(df.head(10).to_markdown())  # markdown for first 10 rows
```


| ref                                                  | title                                         | subtitle                                                                         |   downloadCount |       totalBytes |
|:-----------------------------------------------------|:----------------------------------------------|:---------------------------------------------------------------------------------|----------------:|-----------------:|
| jealousleopard/goodreadsbooks                        | Goodreads-books                               | comprehensive list of all books listed in goodreads                              |           23640 | 637338           |
| uciml/zoo-animal-classification                      | Zoo Animal Classification                     | Use Machine Learning Methods to Correctly Classify Animals Based Upon Attributes |           16597 |   1898           |
| yekenot/fasttext-crawl-300d-2m                       | FastText crawl 300d 2M                        | 2 million word vectors trained on Common Crawl (600B tokens)                     |            8275 |      1.54555e+09 |
| rtatman/sentiment-lexicons-for-81-languages          | Sentiment Lexicons for 81 Languages           | Sentiment Polarity Lexicons (Positive vs. Negative)                              |            7960 |      1.62176e+06 |
| rtatman/glove-global-vectors-for-word-representation | GloVe: Global Vectors for Word Representation | Pre-trained word vectors from Wikipedia 2014 + Gigaword 5                        |            7432 |      4.80173e+08 |
| mozillaorg/common-voice                              | Common Voice                                  | 500 hours of speech recordings, with speaker demographics                        |            6075 |      1.29315e+10 |
| arathee2/demonetization-in-india-twitter-data        | Demonetization in India Twitter Data          | Data extracted from Twitter regarding the recent currency demonetization         |            5761 | 919578           |
| eibriel/rdany-conversations                          | rDany Chat                                    | 157 chats & 6300+ messages with a (fake) virtual companion                       |            3983 | 916724           |
| mrisdal/2016-us-presidential-debates                 | 2016 US Presidential Debates                  | Full transcripts of the face-off between Clinton & Trump                         |            3920 | 123161           |
| nobelfoundation/nobel-laureates                      | Nobel Laureates, 1901-Present                 | Which country has won the most prizes in each category?                          |            3192 |  67763           |


## .meta

`.meta` is your access to metadata about datasets. 

It works the same way things work with the zips of datasets: It will:
- list: will list locally store dataset meta information (in location specified by `s.meta_dir`)
- get: when a value (metadata dict) is requested, (1) the key is searched locally first, and if not found, (2) will request it remotely (through the kaggle api), and (3) the value will be cached (stored) locally


## Cached search info

Wait, it's not all: `KaggleDatasets` will (by default) also cache these results locally in individual json files.

Where? Ask `meta_dir`:


```python
s.meta_dir
```




    '/D/Dropbox/_odata/kaggle/meta'



You can access these files with your favorite dict-like interface, through the `.meta` attribute


```python
len(s.meta)
```




    358




```python
list(s.meta)[:7]
```




    ['emmabel/word-occurrences-in-mr-robot',
     'bitsnpieces/covid19-country-data',
     'johnwdata/coronavirus-covid19-cases-by-us-state',
     'johnwdata/coronavirus-covid19-cases-by-us-county',
     'andradaolteanu/bing-nrc-afinn-lexicons',
     'rahulloha/covid19',
     'nltkdata/word2vec-sample']




```python
pprint(s.meta['emmabel/word-occurrences-in-mr-robot'])
```

    {'creatorName': 'Emma',
     'creatorUrl': 'emmabel',
     'currentVersionNumber': 1,
     'description': None,
     'downloadCount': 116,
     'files': [],
     'id': 4288,
     'isFeatured': False,
     'isPrivate': False,
     'isReviewed': False,
     'kernelCount': 1,
     'lastUpdated': '2017-11-09T18:30:15.733Z',
     'licenseName': 'CC0: Public Domain',
     'ownerName': 'Emma',
     'ownerRef': 'emmabel',
     'ref': 'emmabel/word-occurrences-in-mr-robot',
     'subtitle': "Find out F-Society's favorite lingo",
     'tags': [{'competitionCount': 0,
               'datasetCount': 7525,
               'description': 'Activities that holds the attention and interest of '
                              'an audience, or gives pleasure and delight. It can '
                              'be an idea or a task, but is more likely to be one '
                              'of the activities or events that have developed '
                              'over thousands of years specifically for the '
                              "purpose of keeping an audience's attention.",
               'fullPath': 'topic > arts and entertainment',
               'isAutomatic': False,
               'name': 'arts and entertainment',
               'ref': 'arts and entertainment',
               'scriptCount': 35,
               'totalCount': 7560},
              {'competitionCount': 0,
               'datasetCount': 1227,
               'description': 'One of the hallmarks of intelligence is the use of '
                              'games and toys to occupy free time and develop '
                              "intellectually. Often stored in Mom's basement.",
               'fullPath': 'topic > culture and humanities > games',
               'isAutomatic': False,
               'name': 'games',
               'ref': 'games',
               'scriptCount': 40,
               'totalCount': 1267}],
     'title': 'Word Occurrences in Mr. Robot',
     'topicCount': 0,
     'totalBytes': 119466,
     'url': 'https://www.kaggle.com/emmabel/word-occurrences-in-mr-robot',
     'usabilityRating': 0.7058824,
     'versions': [],
     'viewCount': 1028,
     'voteCount': 5}


So if you want to search locally for information (again, information about your searches, not your data zips!), you can get them in a `DataFrame` like so:


```python
>>> df = pd.DataFrame(s.meta.values())
>>> df.shape
(358, 36)
```

Markdown for the 10 first rows...
```python
t = df.head(10).dropna(axis=1)
del t['tags']
print(t.to_markdown())
```

|    |     id | ref                                                      | subtitle                                                                        | creatorName     | creatorUrl     |       totalBytes | url                                                                             | lastUpdated              |   downloadCount | isPrivate   | isReviewed   | isFeatured   | licenseName                                                | ownerName       | ownerRef       |   kernelCount | title                                              |   topicCount |   viewCount |   voteCount |   currentVersionNumber | files   | versions   |   usabilityRating |
|---:|-------:|:---------------------------------------------------------|:--------------------------------------------------------------------------------|:----------------|:---------------|-----------------:|:--------------------------------------------------------------------------------|:-------------------------|----------------:|:------------|:-------------|:-------------|:-----------------------------------------------------------|:----------------|:---------------|--------------:|:---------------------------------------------------|-------------:|------------:|------------:|-----------------------:|:--------|:-----------|------------------:|
|  0 |   4288 | emmabel/word-occurrences-in-mr-robot                     | Find out F-Society's favorite lingo                                             | Emma            | emmabel        | 119466           | https://www.kaggle.com/emmabel/word-occurrences-in-mr-robot                     | 2017-11-09T18:30:15.733Z |             116 | False       | False        | False        | CC0: Public Domain                                         | Emma            | emmabel        |             1 | Word Occurrences in Mr. Robot                      |            0 |        1028 |           5 |                      1 | []      | []         |          0.705882 |
|  1 | 576036 | bitsnpieces/covid19-country-data                         | Country level metadata that includes temperature, COVID-19 and H1N1 cases, etc. | Patrick         | bitsnpieces    | 190821           | https://www.kaggle.com/bitsnpieces/covid19-country-data                         | 2020-05-03T23:51:55.5Z   |             939 | False       | False        | False        | Database: Open Database, Contents: Database Contents       | Patrick         | bitsnpieces    |             3 | COVID-19 Country Data                              |            0 |        5419 |          26 |                     30 | []      | []         |          0.882353 |
|  2 | 575937 | johnwdata/coronavirus-covid19-cases-by-us-state          | NYTimes Coronavirus Dataset                                                     | John Wackerow   | johnwdata      |  82582           | https://www.kaggle.com/johnwdata/coronavirus-covid19-cases-by-us-state          | 2020-09-23T12:43:05.76Z  |              59 | False       | False        | False        | Other (specified in description)                           | John Wackerow   | johnwdata      |             2 | Coronavirus COVID-19 Cases By US State             |            0 |        1276 |           3 |                     83 | []      | []         |          1        |
|  3 | 575883 | johnwdata/coronavirus-covid19-cases-by-us-county         | NYTimes Coronavirus Dataset                                                     | John Wackerow   | johnwdata      |      3.50819e+06 | https://www.kaggle.com/johnwdata/coronavirus-covid19-cases-by-us-county         | 2020-07-23T18:47:16.543Z |              37 | False       | False        | False        | Unknown                                                    | John Wackerow   | johnwdata      |             2 | Coronavirus COVID-19 Cases By US County            |            0 |         610 |           3 |                      6 | []      | []         |          0.764706 |
|  4 | 507452 | andradaolteanu/bing-nrc-afinn-lexicons                   | the lexicons are in CSV format                                                  | Andrada Olteanu | andradaolteanu |  83965           | https://www.kaggle.com/andradaolteanu/bing-nrc-afinn-lexicons                   | 2020-02-09T18:39:13.343Z |             135 | False       | False        | False        | Unknown                                                    | Andrada Olteanu | andradaolteanu |            11 | Bing, NRC, Afinn Lexicons                          |            0 |         629 |          12 |                      1 | []      | []         |          0.882353 |
|  5 | 599303 | rahulloha/covid19                                        | Covid-19 dataset (updates daily at 10:00 pm pst)                                | Rahul Loha      | rahulloha      |      1.60678e+07 | https://www.kaggle.com/rahulloha/covid19                                        | 2020-04-12T22:50:26.857Z |              65 | False       | False        | False        | Unknown                                                    | Rahul Loha      | rahulloha      |             1 | Global Coronavirus (COVID-19) Data (Johns Hopkins) |            0 |         615 |           6 |                      1 | []      | []         |          0.647059 |
|  6 |   2045 | nltkdata/word2vec-sample                                 | Sample Word2Vec Model                                                           | Liling Tan      | alvations      |      1.01479e+08 | https://www.kaggle.com/nltkdata/word2vec-sample                                 | 2017-08-20T03:14:39.623Z |             772 | False       | True         | False        | Other (specified in description)                           | NLTK Data       | nltkdata       |             3 | Word2Vec Sample                                    |            0 |        8073 |          15 |                      1 | []      | []         |          0.75     |
|  7 | 585107 | nxpnsv/country-health-indicators                         | Health indicator relevant to covid19 death and infection risk                   | nxpnsv          | nxpnsv         |  40146           | https://www.kaggle.com/nxpnsv/country-health-indicators                         | 2020-04-07T11:12:41.91Z  |             185 | False       | False        | False        | CC BY-NC-SA 4.0                                            | nxpnsv          | nxpnsv         |             6 | country health indicators                          |            0 |        2126 |          11 |                      6 | []      | []         |          1        |
|  8 | 585591 | joelhanson/coronavirus-covid19-data-in-the-united-states | The New York Times data on coronavirus cases and deaths in the U.S              | Joel Hanson     | joelhanson     |      5.83676e+06 | https://www.kaggle.com/joelhanson/coronavirus-covid19-data-in-the-united-states | 2020-09-21T15:51:45.933Z |             164 | False       | False        | False        | Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) | Joel Hanson     | joelhanson     |             3 | Coronavirus (Covid-19) Data of United States (USA) |            0 |        1724 |           5 |                     29 | []      | []         |          0.882353 |
|  9 |   8352 | vsmolyakov/fasttext                                      | embeddings with sub-word information                                            | vsmolyakov      | vsmolyakov     |      1.1168e+08  | https://www.kaggle.com/vsmolyakov/fasttext                                      | 2017-12-31T17:32:30.94Z  |             947 | False       | False        | False        | CC0: Public Domain                                         | vsmolyakov      | vsmolyakov     |            14 | FastText                                           |            0 |        3809 |           5 |                      1 | []      | []         |          0.875    |


**Note: If you don't want all your search results to be cached you can just specify it.**

```python
s = KaggleDatasets(rootdir, cache_metas_on_search=False)  # make an instance
```

# The boring stuff

## Install

pip install haggle

**You'll need a kaggle api token to use this**

If you do, you probably can just start using. 

If you don't got get one! Go see [this](https://github.com/Kaggle/kaggle-api) for detailed instructions, it essentially says:



## API credentials

To use the Kaggle API, sign up for a Kaggle account at https://www.kaggle.com. 
Then go to the 'Account' tab of your user profile (`https://www.kaggle.com/<username>/account`) and select 'Create API Token'. 
This will trigger the download of `kaggle.json`, a file containing your API credentials. 
Place this file in the location `~/.kaggle/kaggle.json` (on Windows in the location `C:\Users\<Windows-username>\.kaggle\kaggle.json` - you can check the exact location, sans drive, with `echo %HOMEPATH%`). 
You can define a shell environment variable `KAGGLE_CONFIG_DIR` to change this location to `$KAGGLE_CONFIG_DIR/kaggle.json` (on Windows it will be `%KAGGLE_CONFIG_DIR%\kaggle.json`).

For your security, ensure that other users of your computer do not have read access to your credentials. On Unix-based systems you can do this with the following command: 

`chmod 600 ~/.kaggle/kaggle.json`

You can also choose to export your Kaggle username and token to the environment:

```bash
export KAGGLE_USERNAME=datadinosaur
export KAGGLE_KEY=xxxxxxxxxxxxxx
```
In addition, you can export any other configuration value that normally would be in
the `$HOME/.kaggle/kaggle.json` in the format 'KAGGLE_<VARIABLE>' (note uppercase).  
For example, if the file had the variable "proxy" you would export `KAGGLE_PROXY`
and it would be discovered by the client.


# F.A.Q.

## What if I don't want a zip file anymore?

Just delete it, like you do with any file you don't want anymore. You know the one.

Or... you can be cool and do `del s['owner/dataset']` for that key (note a key doesn't include the rootdir or the `.zip` extension), just like you would with a... `dict`, once again.

## Do you have any jupyter notebooks demoing this.

Sure, you can find some [here on github](https://github.com/otosense/haggle/tree/master/docs).

## A little snippet of code to test?

```python
from haggle import KaggleDatasets

s = KaggleDatasets()  # make an instance
# results = s.search('coronavirus')
# ref = next(iter(results))  # see that results iteration works
ref = 'sanchman/coronavirus-present-data'
if ref in s:  # delete if exists
    del s[ref]
assert ref not in s  # see, not there
v = s[ref]  # redownload
assert ref in s  # see, not there
assert 'PresentData.xlsx' in set(v)  # and it has stuff in v

import pandas as pd
import io
df = pd.read_excel(io.BytesIO(v['PresentData.xlsx']))
assert 'Total Confirmed' in df.columns
assert 'Country' in df.columns
assert 'France' in df['Country'].values
```
