# haggle.dacc

Data access

## Classes

| [`KaggleDatasetInfoReader`](#haggle.dacc.KaggleDatasetInfoReader)   | A KvReader to access Kaggle resources.                                                |
|----------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| [`KaggleBytesDatasetReader`](#haggle.dacc.KaggleBytesDatasetReader)  | Downloads the dataset as a zip file to a temporary location and then reads its bytes. |
| [`KaggleDatasetReader`](#haggle.dacc.KaggleDatasetReader)       | Downloads the dataset as a zip file to a temporary location and then reads its bytes. |
| [`KaggleMetadataReader`](#haggle.dacc.KaggleMetadataReader)      | A KvReader to access Kaggle resources.                                                |
| [`RelZipFiles`](#haggle.dacc.RelZipFiles)               | Like ZipFilesReader, but the ability to write bytes (assumed to be valid bytes of     |
| [`LocalKaggleZips`](#haggle.dacc.LocalKaggleZips)           | A mixin that will automatically create directories on setitem, when missing.          |
| [`LocalKaggleMeta`](#haggle.dacc.LocalKaggleMeta)           | A mixin that will automatically create directories on setitem, when missing.          |

## Functions

| [`owner_and_dataset_slugs`](#haggle.dacc.owner_and_dataset_slugs)(ref)           | try to get the owner and dataset slugs from a ref   |
|-----------------------------------------------------------------------------------------|-----------------------------------------------------|
| [`get_kaggle_dataset`](#haggle.dacc.get_kaggle_dataset)(dataset[, rootdir]) | Get a Kaggle dataset.                               |

## Module Contents

### *class* haggle.dacc.KaggleDatasetInfoReader(, group=None, sort_by=None, filetype=None, license=None, tagids=None, search=None, user=None, start_page=1, max_n_pages=DFLT_MAX_PAGES, warn_if_there_are_more_items=False, \*\*kwargs)

Bases: `dol.KvReader`

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

### haggle.dacc.owner_and_dataset_slugs(ref)

try to get the owner and dataset slugs from a ref

### *class* haggle.dacc.KaggleBytesDatasetReader(, group=None, sort_by=None, filetype=None, license=None, tagids=None, search=None, user=None, start_page=1, max_n_pages=DFLT_MAX_PAGES, warn_if_there_are_more_items=False, \*\*kwargs)

Bases: [`KaggleDatasetInfoReader`](#haggle.dacc.KaggleDatasetInfoReader)

Downloads the dataset as a zip file to a temporary location and then reads its bytes.
This is necessary because the `dataset_download_files` method in the current
Kaggle API handles saving files directly to disk, rather than returning bytes.

### *class* haggle.dacc.KaggleDatasetReader(, group=None, sort_by=None, filetype=None, license=None, tagids=None, search=None, user=None, start_page=1, max_n_pages=DFLT_MAX_PAGES, warn_if_there_are_more_items=False, \*\*kwargs)

Bases: [`KaggleBytesDatasetReader`](#haggle.dacc.KaggleBytesDatasetReader)

Downloads the dataset as a zip file to a temporary location and then reads its bytes.
This is necessary because the `dataset_download_files` method in the current
Kaggle API handles saving files directly to disk, rather than returning bytes.

### *class* haggle.dacc.KaggleMetadataReader(, group=None, sort_by=None, filetype=None, license=None, tagids=None, search=None, user=None, start_page=1, max_n_pages=DFLT_MAX_PAGES, warn_if_there_are_more_items=False, \*\*kwargs)

Bases: [`KaggleDatasetInfoReader`](#haggle.dacc.KaggleDatasetInfoReader)

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

### *class* haggle.dacc.RelZipFiles(rootdir, subpath='{zip_name}.zip', pattern_for_field=None, max_levels=0, zip_reader=ZipReader, \*\*zip_reader_kwargs)

Bases: `dol.zipfiledol.ZipFilesReaderAndBytesWriter`, `dol.filesys.LocalFileDeleteMixin`

Like ZipFilesReader, but the ability to write bytes (assumed to be valid bytes of
the zip format) to a key

### *class* haggle.dacc.LocalKaggleZips(rootdir)

Bases: `py2store.stores.local_store.AutoMkDirsOnSetitemMixin`, [`RelZipFiles`](#haggle.dacc.RelZipFiles)

A mixin that will automatically create directories on setitem, when missing.

### *class* haggle.dacc.LocalKaggleMeta(rootdir)

Bases: `py2store.stores.local_store.AutoMkDirsOnSetitemMixin`, `py2store.stores.local_store.LocalJsonStore`

A mixin that will automatically create directories on setitem, when missing.

### haggle.dacc.get_kaggle_dataset(dataset, rootdir=DFLT_ROOTDIR)

Get a Kaggle dataset.

* **Parameters:**
  **dataset** – Either a Kaggle dataset ref (“owner/dataset”) or an http(s) Kaggle URL
  of the form “[https://www.kaggle.com/datasets](https://www.kaggle.com/datasets)/<owner>/<dataset>”.

### Examples

```pycon
>>> get_kaggle_dataset('https://www.kaggle.com/datasets/rtatman/emojinet')
...
```
