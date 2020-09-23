<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#Haggle" data-toc-modified-id="Haggle-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Haggle</a></span></li><li><span><a href="#Install" data-toc-modified-id="Install-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Install</a></span><ul class="toc-item"><li><span><a href="#API-credentials" data-toc-modified-id="API-credentials-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>API credentials</a></span></li></ul></li><li><span><a href="#Simple-example" data-toc-modified-id="Simple-example-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Simple example</a></span><ul class="toc-item"><li><span><a href="#Conclusion" data-toc-modified-id="Conclusion-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>Conclusion</a></span></li></ul></li><li><span><a href="#F.A.Q." data-toc-modified-id="F.A.Q.-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>F.A.Q.</a></span><ul class="toc-item"><li><span><a href="#What-if-I-don't-want-a-zip-file-anymore?" data-toc-modified-id="What-if-I-don't-want-a-zip-file-anymore?-4.1"><span class="toc-item-num">4.1&nbsp;&nbsp;</span>What if I don't want a zip file anymore?</a></span></li></ul></li></ul></div>



# Haggle

A simple facade to [Kaggle](https://www.kaggle.com/) data.

**Haggle:** /ˈhaɡəl/
- an instance of intense argument (as in bargaining) 
- wrangle (over a price, terms of an agreement, etc.) 
- rhymes with Kaggle and is not taken on pypi (well, now it is)

Essentially, instantiate a `KaggleDatasets` object, and from it...
- search for datasets from the python console (so much better than having pictures the [kaggle website](https://www.kaggle.com/) right?)
- download what you want and start using...
- ... oh, and it automatically caches the data zip to a local directory
- ... oh, and all the while it pretends to be a humble dict with `owner/dataset` keys, and that's the coolest bit.

# Install

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


# Simple example


```python
from py2store.ext.kaggle import KaggleDatasets

rootdir = '/D/Dropbox/_odata/kaggle/zips'  # define where you want the data to be cached/downloaded

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



## Conclusion

This is awesome.

You get any dataset you want by just doing `s['owner/dataset']`, and start using it right away (or later), and the next time you ask for it, it'll be there at your fingertips.


```python

```

# F.A.Q.

## What if I don't want a zip file anymore?

Just delete it, like you do with any file you don't want anymore. You know the one.

Or... you can be cool and do `del s['owner/dataset']` for that key (note a key doesn't include the rootdir or the `.zip` extension), just like you would with a... `dict`, once again.

## Do you have any jupyter notebooks demoing this.

Sure, you can find some [here on github](https://github.com/otosense/haggle/tree/master/docs).