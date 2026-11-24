# haggle.dacc

Data access

### Module Attributes

| [`KaggleApi`](#haggle.dacc.KaggleApi)   | The `kaggle` package authenticates *when it is imported*, so it is imported (and the API authenticated) on first use, never at `import haggle`.   |
|--------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|

### Functions

| `clog`(condition, \*args)                                                               |                                                   |
|-----------------------------------------------------------------------------------------|---------------------------------------------------|
| [`get_kaggle_dataset`](#haggle.dacc.get_kaggle_dataset)(dataset[, rootdir]) | Get a Kaggle dataset.                             |
| `handle_missing_dir`(dirpath[, prefix_msg, ...])                                        |                                                   |
| [`owner_and_dataset_slugs`](#haggle.dacc.owner_and_dataset_slugs)(ref)           | try to get the owner and dataset slugs from a ref |

### Classes

| `DataInfoPaggedItems`()                                                                             |                                                                                       |
|-----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| [`KaggleBytesDatasetReader`](#haggle.dacc.KaggleBytesDatasetReader)(\*[, group, ...])         | Downloads the dataset as a zip file to a temporary location and then reads its bytes. |
| [`KaggleDatasetInfoReader`](#haggle.dacc.KaggleDatasetInfoReader)(\*[, group, sort_by, ...]) | A KvReader to access Kaggle resources.                                                |
| [`KaggleDatasetReader`](#haggle.dacc.KaggleDatasetReader)(\*[, group, sort_by, ...])     |                                                                                       |
| [`KaggleDatasets`](#haggle.dacc.KaggleDatasets)(rootdir)                            |                                                                                       |
| [`KaggleMeta`](#haggle.dacc.KaggleMeta)(rootdir)                                | By store we mean key-value store.                                                     |
| [`KaggleMetadataReader`](#haggle.dacc.KaggleMetadataReader)(\*[, group, sort_by, ...])    |                                                                                       |
| [`LocalKaggleMeta`](#haggle.dacc.LocalKaggleMeta)(rootdir)                           | By store we mean key-value store.                                                     |
| [`LocalKaggleZips`](#haggle.dacc.LocalKaggleZips)(rootdir)                           | By store we mean key-value store.                                                     |
| [`RelZipFiles`](#haggle.dacc.RelZipFiles)(rootdir[, subpath, ...])               |                                                                                       |

### haggle.dacc.KaggleApi *= None*

The `kaggle` package authenticates *when it is imported*, so it is imported (and the
API authenticated) on first use, never at `import haggle`. Assign a class here to
inject another implementation (tests do).

### *class* haggle.dacc.KaggleBytesDatasetReader(, group=None, sort_by=None, filetype=None, license=None, tagids=None, search=None, user=None, start_page=1, max_n_pages=10, warn_if_there_are_more_items=False, \*\*kwargs)

Bases: [`KaggleDatasetInfoReader`](#haggle.dacc.KaggleDatasetInfoReader)

Downloads the dataset as a zip file to a temporary location and then reads its bytes.
This is necessary because the `dataset_download_files` method in the current
Kaggle API handles saving files directly to disk, rather than returning bytes.

### *class* haggle.dacc.KaggleDatasetInfoReader(, group=None, sort_by=None, filetype=None, license=None, tagids=None, search=None, user=None, start_page=1, max_n_pages=10, warn_if_there_are_more_items=False, \*\*kwargs)

Bases: `KvReader`

A KvReader to access Kaggle resources.

Prerequisites:
: pip install kaggle
  Having a kaggle api token where the kaggle library will be looking for it
  <br/>
  > (see [https://github.com/Kaggle/kaggle-api#api-credentials](https://github.com/Kaggle/kaggle-api#api-credentials))

You seed a Reader by specifying any combination of things like search terms, groups,
filetypes etc.
See `kaggle.api` for more information.
Additional (and specific to py2store reader) arguments are

> start_page (default 0, but useful for paging),
> max_n_pages (to not hit the API too hard if your query is large), and
> warn_if_there_are_more_items if you want to be warned if there’s more items than
> what you see
```pycon
>>> ka = KaggleDatasetInfoReader(search='coronavirus covid')
>>> ka = KaggleDatasetInfoReader(
...         user='sudalairajkumar', start_page=1, max_n_pages=2)
```

### *class* haggle.dacc.KaggleDatasetReader(, group=None, sort_by=None, filetype=None, license=None, tagids=None, search=None, user=None, start_page=1, max_n_pages=10, warn_if_there_are_more_items=False, \*\*kwargs)

Bases: [`KaggleBytesDatasetReader`](#haggle.dacc.KaggleBytesDatasetReader)

### *class* haggle.dacc.KaggleDatasets(rootdir)

Bases: [`LocalKaggleZips`](#haggle.dacc.LocalKaggleZips)

### *class* haggle.dacc.KaggleMeta(rootdir)

Bases: [`LocalKaggleMeta`](#haggle.dacc.LocalKaggleMeta)

By store we mean key-value store. This could be files in a filesystem, objects in s3, or a database. Where and
how the content is stored should be specified, but StoreInterface offers a dict-like interface to this.

```default
__getitem__ calls: _id_of_key                                       _obj_of_data
__setitem__ calls: _id_of_key                   _data_of_obj
__delitem__ calls: _id_of_key
__iter__    calls:                  _key_of_id
```

```pycon
>>> # Default store: no key or value conversion #####################################
>>> from dol import Store
>>> s = Store()
>>> s['foo'] = 33
>>> s['bar'] = 65
>>> assert list(s.items()) == [('foo', 33), ('bar', 65)]
>>> assert list(s.store.items()) == [('foo', 33), ('bar', 65)]  # see that the store contains the same thing
>>>
>>> #################################################################################
>>> # Now let's make stores that have a key and value conversion layer ##############
>>> # input keys will be upper cased, and output keys lower cased ###################
>>> # input values (assumed int) will be converted to ascii string, and visa versa ##
>>> #################################################################################
>>>
>>> def test_store(s):
...     s['foo'] = 33  # write 33 to 'foo'
...     assert 'foo' in s  # __contains__ works
...     assert 'no_such_key' not in s  # __nin__ works
...     s['bar'] = 65  # write 65 to 'bar'
...     assert len(s) == 2  # there are indeed two elements
...     assert list(s) == ['foo', 'bar']  # these are the keys
...     assert list(s.keys()) == ['foo', 'bar']  # the keys() method works!
...     assert list(s.values()) == [33, 65]  # the values() method works!
...     assert list(s.items()) == [('foo', 33), ('bar', 65)]  # these are the items
...     assert list(s.store.items()) == [('FOO', '!'), ('BAR', 'A')]  # but note the internal representation
...     assert s.get('foo') == 33  # the get method works
...     assert s.get('no_such_key', 'something') == 'something'  # return a default value
...     del(s['foo'])  # you can delete an item given its key
...     assert len(s) == 1  # see, only one item left!
...     assert list(s.items()) == [('bar', 65)]  # here it is
>>>
>>> # We can introduce this conversion layer in several ways. Here's a few... ######################
>>> # by subclassing ###############################################################################
>>> class MyStore(Store):
...     def _id_of_key(self, k):
...         return k.upper()
...     def _key_of_id(self, _id):
...         return _id.lower()
...     def _data_of_obj(self, obj):
...         return chr(obj)
...     def _obj_of_data(self, data):
...         return ord(data)
>>> s = MyStore(store=dict())  # note that you don't need to specify dict(), since it's the default
>>> test_store(s)
>>>
>>> # by assigning functions to converters ##########################################################
>>> class MyStore(Store):
...     def __init__(self, store, _id_of_key, _key_of_id, _data_of_obj, _obj_of_data):
...         super().__init__(store)
...         self._id_of_key = _id_of_key
...         self._key_of_id = _key_of_id
...         self._data_of_obj = _data_of_obj
...         self._obj_of_data = _obj_of_data
...
>>> s = MyStore(dict(),
...             _id_of_key=lambda k: k.upper(),
...             _key_of_id=lambda _id: _id.lower(),
...             _data_of_obj=lambda obj: chr(obj),
...             _obj_of_data=lambda data: ord(data))
>>> test_store(s)
>>>
>>> # using a Mixin class #############################################################################
>>> class Mixin:
...     def _id_of_key(self, k):
...         return k.upper()
...     def _key_of_id(self, _id):
...         return _id.lower()
...     def _data_of_obj(self, obj):
...         return chr(obj)
...     def _obj_of_data(self, data):
...         return ord(data)
...
>>> class MyStore(Mixin, Store):  # note that the Mixin must come before Store in the mro
...     pass
...
>>> s = MyStore()  # no dict()? No, because default anyway
>>> test_store(s)
>>>
>>> # adding wrapper methods to an already made Store instance #########################################
>>> s = Store(dict())
>>> s._id_of_key=lambda k: k.upper()
>>> s._key_of_id=lambda _id: _id.lower()
>>> s._data_of_obj=lambda obj: chr(obj)
>>> s._obj_of_data=lambda data: ord(data)
>>> test_store(s)
```

Note on defining your own “Mapping Views”.

When you do a `.keys()`, a `.values()` or `.items()` you’re getting a `MappingView`
instance; an iterable and sized container that provides some methods to access
particular aspects of the wrapped mapping.

If you need to customize the behavior of these instances, you should avoid
overriding the `keys`, `values` or `items` methods directly, but instead
override the `KeysView`, `ValuesView` or `ItemsView` classes that they use.

For more, see: [https://github.com/i2mint/dol/wiki/Mapping-Views](https://github.com/i2mint/dol/wiki/Mapping-Views)

### *class* haggle.dacc.KaggleMetadataReader(, group=None, sort_by=None, filetype=None, license=None, tagids=None, search=None, user=None, start_page=1, max_n_pages=10, warn_if_there_are_more_items=False, \*\*kwargs)

Bases: [`KaggleDatasetInfoReader`](#haggle.dacc.KaggleDatasetInfoReader)

### *class* haggle.dacc.LocalKaggleMeta(rootdir)

Bases: [`LocalKaggleMeta`](#haggle.dacc.LocalKaggleMeta)

By store we mean key-value store. This could be files in a filesystem, objects in s3, or a database. Where and
how the content is stored should be specified, but StoreInterface offers a dict-like interface to this.

```default
__getitem__ calls: _id_of_key                                       _obj_of_data
__setitem__ calls: _id_of_key                   _data_of_obj
__delitem__ calls: _id_of_key
__iter__    calls:                  _key_of_id
```

```pycon
>>> # Default store: no key or value conversion #####################################
>>> from dol import Store
>>> s = Store()
>>> s['foo'] = 33
>>> s['bar'] = 65
>>> assert list(s.items()) == [('foo', 33), ('bar', 65)]
>>> assert list(s.store.items()) == [('foo', 33), ('bar', 65)]  # see that the store contains the same thing
>>>
>>> #################################################################################
>>> # Now let's make stores that have a key and value conversion layer ##############
>>> # input keys will be upper cased, and output keys lower cased ###################
>>> # input values (assumed int) will be converted to ascii string, and visa versa ##
>>> #################################################################################
>>>
>>> def test_store(s):
...     s['foo'] = 33  # write 33 to 'foo'
...     assert 'foo' in s  # __contains__ works
...     assert 'no_such_key' not in s  # __nin__ works
...     s['bar'] = 65  # write 65 to 'bar'
...     assert len(s) == 2  # there are indeed two elements
...     assert list(s) == ['foo', 'bar']  # these are the keys
...     assert list(s.keys()) == ['foo', 'bar']  # the keys() method works!
...     assert list(s.values()) == [33, 65]  # the values() method works!
...     assert list(s.items()) == [('foo', 33), ('bar', 65)]  # these are the items
...     assert list(s.store.items()) == [('FOO', '!'), ('BAR', 'A')]  # but note the internal representation
...     assert s.get('foo') == 33  # the get method works
...     assert s.get('no_such_key', 'something') == 'something'  # return a default value
...     del(s['foo'])  # you can delete an item given its key
...     assert len(s) == 1  # see, only one item left!
...     assert list(s.items()) == [('bar', 65)]  # here it is
>>>
>>> # We can introduce this conversion layer in several ways. Here's a few... ######################
>>> # by subclassing ###############################################################################
>>> class MyStore(Store):
...     def _id_of_key(self, k):
...         return k.upper()
...     def _key_of_id(self, _id):
...         return _id.lower()
...     def _data_of_obj(self, obj):
...         return chr(obj)
...     def _obj_of_data(self, data):
...         return ord(data)
>>> s = MyStore(store=dict())  # note that you don't need to specify dict(), since it's the default
>>> test_store(s)
>>>
>>> # by assigning functions to converters ##########################################################
>>> class MyStore(Store):
...     def __init__(self, store, _id_of_key, _key_of_id, _data_of_obj, _obj_of_data):
...         super().__init__(store)
...         self._id_of_key = _id_of_key
...         self._key_of_id = _key_of_id
...         self._data_of_obj = _data_of_obj
...         self._obj_of_data = _obj_of_data
...
>>> s = MyStore(dict(),
...             _id_of_key=lambda k: k.upper(),
...             _key_of_id=lambda _id: _id.lower(),
...             _data_of_obj=lambda obj: chr(obj),
...             _obj_of_data=lambda data: ord(data))
>>> test_store(s)
>>>
>>> # using a Mixin class #############################################################################
>>> class Mixin:
...     def _id_of_key(self, k):
...         return k.upper()
...     def _key_of_id(self, _id):
...         return _id.lower()
...     def _data_of_obj(self, obj):
...         return chr(obj)
...     def _obj_of_data(self, data):
...         return ord(data)
...
>>> class MyStore(Mixin, Store):  # note that the Mixin must come before Store in the mro
...     pass
...
>>> s = MyStore()  # no dict()? No, because default anyway
>>> test_store(s)
>>>
>>> # adding wrapper methods to an already made Store instance #########################################
>>> s = Store(dict())
>>> s._id_of_key=lambda k: k.upper()
>>> s._key_of_id=lambda _id: _id.lower()
>>> s._data_of_obj=lambda obj: chr(obj)
>>> s._obj_of_data=lambda data: ord(data)
>>> test_store(s)
```

Note on defining your own “Mapping Views”.

When you do a `.keys()`, a `.values()` or `.items()` you’re getting a `MappingView`
instance; an iterable and sized container that provides some methods to access
particular aspects of the wrapped mapping.

If you need to customize the behavior of these instances, you should avoid
overriding the `keys`, `values` or `items` methods directly, but instead
override the `KeysView`, `ValuesView` or `ItemsView` classes that they use.

For more, see: [https://github.com/i2mint/dol/wiki/Mapping-Views](https://github.com/i2mint/dol/wiki/Mapping-Views)

### *class* haggle.dacc.LocalKaggleZips(rootdir)

Bases: `Store`

By store we mean key-value store. This could be files in a filesystem, objects in s3, or a database. Where and
how the content is stored should be specified, but StoreInterface offers a dict-like interface to this.

```default
__getitem__ calls: _id_of_key                                       _obj_of_data
__setitem__ calls: _id_of_key                   _data_of_obj
__delitem__ calls: _id_of_key
__iter__    calls:                  _key_of_id
```

```pycon
>>> # Default store: no key or value conversion #####################################
>>> from dol import Store
>>> s = Store()
>>> s['foo'] = 33
>>> s['bar'] = 65
>>> assert list(s.items()) == [('foo', 33), ('bar', 65)]
>>> assert list(s.store.items()) == [('foo', 33), ('bar', 65)]  # see that the store contains the same thing
>>>
>>> #################################################################################
>>> # Now let's make stores that have a key and value conversion layer ##############
>>> # input keys will be upper cased, and output keys lower cased ###################
>>> # input values (assumed int) will be converted to ascii string, and visa versa ##
>>> #################################################################################
>>>
>>> def test_store(s):
...     s['foo'] = 33  # write 33 to 'foo'
...     assert 'foo' in s  # __contains__ works
...     assert 'no_such_key' not in s  # __nin__ works
...     s['bar'] = 65  # write 65 to 'bar'
...     assert len(s) == 2  # there are indeed two elements
...     assert list(s) == ['foo', 'bar']  # these are the keys
...     assert list(s.keys()) == ['foo', 'bar']  # the keys() method works!
...     assert list(s.values()) == [33, 65]  # the values() method works!
...     assert list(s.items()) == [('foo', 33), ('bar', 65)]  # these are the items
...     assert list(s.store.items()) == [('FOO', '!'), ('BAR', 'A')]  # but note the internal representation
...     assert s.get('foo') == 33  # the get method works
...     assert s.get('no_such_key', 'something') == 'something'  # return a default value
...     del(s['foo'])  # you can delete an item given its key
...     assert len(s) == 1  # see, only one item left!
...     assert list(s.items()) == [('bar', 65)]  # here it is
>>>
>>> # We can introduce this conversion layer in several ways. Here's a few... ######################
>>> # by subclassing ###############################################################################
>>> class MyStore(Store):
...     def _id_of_key(self, k):
...         return k.upper()
...     def _key_of_id(self, _id):
...         return _id.lower()
...     def _data_of_obj(self, obj):
...         return chr(obj)
...     def _obj_of_data(self, data):
...         return ord(data)
>>> s = MyStore(store=dict())  # note that you don't need to specify dict(), since it's the default
>>> test_store(s)
>>>
>>> # by assigning functions to converters ##########################################################
>>> class MyStore(Store):
...     def __init__(self, store, _id_of_key, _key_of_id, _data_of_obj, _obj_of_data):
...         super().__init__(store)
...         self._id_of_key = _id_of_key
...         self._key_of_id = _key_of_id
...         self._data_of_obj = _data_of_obj
...         self._obj_of_data = _obj_of_data
...
>>> s = MyStore(dict(),
...             _id_of_key=lambda k: k.upper(),
...             _key_of_id=lambda _id: _id.lower(),
...             _data_of_obj=lambda obj: chr(obj),
...             _obj_of_data=lambda data: ord(data))
>>> test_store(s)
>>>
>>> # using a Mixin class #############################################################################
>>> class Mixin:
...     def _id_of_key(self, k):
...         return k.upper()
...     def _key_of_id(self, _id):
...         return _id.lower()
...     def _data_of_obj(self, obj):
...         return chr(obj)
...     def _obj_of_data(self, data):
...         return ord(data)
...
>>> class MyStore(Mixin, Store):  # note that the Mixin must come before Store in the mro
...     pass
...
>>> s = MyStore()  # no dict()? No, because default anyway
>>> test_store(s)
>>>
>>> # adding wrapper methods to an already made Store instance #########################################
>>> s = Store(dict())
>>> s._id_of_key=lambda k: k.upper()
>>> s._key_of_id=lambda _id: _id.lower()
>>> s._data_of_obj=lambda obj: chr(obj)
>>> s._obj_of_data=lambda data: ord(data)
>>> test_store(s)
```

Note on defining your own “Mapping Views”.

When you do a `.keys()`, a `.values()` or `.items()` you’re getting a `MappingView`
instance; an iterable and sized container that provides some methods to access
particular aspects of the wrapped mapping.

If you need to customize the behavior of these instances, you should avoid
overriding the `keys`, `values` or `items` methods directly, but instead
override the `KeysView`, `ValuesView` or `ItemsView` classes that they use.

For more, see: [https://github.com/i2mint/dol/wiki/Mapping-Views](https://github.com/i2mint/dol/wiki/Mapping-Views)

#### is_valid_key(k, \*args, \_\_name='is_valid_key', \*\*kwargs)

`is_valid_key` on the inner key – see `mk_relative_path_store`.

#### validate_key(k, \*args, \_\_name='validate_key', \*\*kwargs)

`validate_key` on the inner key – see `mk_relative_path_store`.

### *class* haggle.dacc.RelZipFiles(rootdir, subpath='{zip_name}.zip', pattern_for_field=None, max_levels=0, zip_reader=<class 'dol.zipfiledol.ZipReader'>, \*\*zip_reader_kwargs)

Bases: `PrefixRelativizationMixin`, `Store`

#### is_valid_key(k, \*args, \_\_name='is_valid_key', \*\*kwargs)

`is_valid_key` on the inner key – see `mk_relative_path_store`.

#### validate_key(k, \*args, \_\_name='validate_key', \*\*kwargs)

`validate_key` on the inner key – see `mk_relative_path_store`.

### haggle.dacc.get_kaggle_dataset(dataset, rootdir='/home/runner/haggle')

Get a Kaggle dataset.

* **Parameters:**
  **dataset** – Either a Kaggle dataset ref (“owner/dataset”) or an http(s) Kaggle URL
  of the form “[https://www.kaggle.com/datasets](https://www.kaggle.com/datasets)/<owner>/<dataset>”.

### Examples

```pycon
>>> get_kaggle_dataset('https://www.kaggle.com/datasets/rtatman/emojinet')
...
```

### haggle.dacc.owner_and_dataset_slugs(ref)

try to get the owner and dataset slugs from a ref
