"""
Data access
"""
import os

try:
    from kaggle.api import KaggleApi
except OSError as err:
    raise OSError(
        f'''{err}
Do you have a kaggle API token? Did you put it in the right place? 
See https://github.com/Kaggle/kaggle-api#api-credentials for more information.
It's quick and easy (oh, and free!)!!
'''
    )
except ModuleNotFoundError as err:
    raise ModuleNotFoundError(
        f'''{err}
You might try to do a `pip install kaggle` in the terminal?
'''
    )

from dol import KvReader, FilesOfZip
from dol.util import lazyprop

DFLT_MAX_ITEMS = 200
DFLT_MAX_PAGES = 10

ROOTDIR_ENVVAR = 'HAGGLE_ROOTDIR'
DFLT_ROOTDIR = os.environ.get(ROOTDIR_ENVVAR, os.path.expanduser('~/haggle'))


def clog(condition, *args):
    if condition:
        print(*args)


def handle_missing_dir(dirpath, prefix_msg='', ask_first=True, verbose=True):
    if not os.path.isdir(dirpath):
        if ask_first:
            clog(verbose, prefix_msg)
            clog(verbose, f"This directory doesn't exist: {dirpath}")
            answer = input('Should I make that directory for you? ([Y]/n)?') or 'Y'
            if next(iter(answer.strip().lower()), None) != 'y':
                return
        clog(verbose, f'Making {dirpath}...')
        os.mkdir(dirpath)


class DataInfoPaggedItems:
    def __init__(self):
        self.pages = []
        self.ref_to_idx = dict()

    def append(self, page_contents):
        # TODO: Atomize this code so it can't be broken by async
        page = self.n_pages()
        for i, v in enumerate(page_contents):
            ref = v.get('ref', None)
            if ref is not None:
                self.ref_to_idx[ref] = (page, i)
        self.pages.append(page_contents)

    def __getitem__(self, ref):
        page, i = self.ref_to_idx[ref]
        return self.pages[page][i]

    def __len__(self):
        return len(self.ref_to_idx)

    def get_page_contents(self, page):
        return self.pages[page]

    def n_pages(self):
        return len(self.pages)


class KaggleDatasetInfoReader(KvReader):
    """
    A KvReader to access Kaggle resources.

    Prerequisites:
        pip install kaggle
        Having a kaggle api token where the kaggle library will be looking for it
            (see https://github.com/Kaggle/kaggle-api#api-credentials)

    You seed a Reader by specifying any combination of things like search terms, groups,
    filetypes etc.
    See `kaggle.api` for more information.
    Additional (and specific to py2store reader) arguments are
        start_page (default 0, but useful for paging),
        max_n_pages (to not hit the API too hard if your query is large), and
        warn_if_there_are_more_items if you want to be warned if there's more items than
        what you see

    >>> ka = KaggleDatasetInfoReader(search='coronavirus covid')  # doctest: +SKIP
    >>> ka = KaggleDatasetInfoReader(
    ...         user='sudalairajkumar', start_page=1, max_n_pages=2)  # doctest: +SKIP

    """

    def __init__(
        self,
        *,
        group=None,
        sort_by=None,
        filetype=None,
        license=None,
        tagids=None,
        search=None,
        user=None,
        start_page=1,
        max_n_pages=DFLT_MAX_PAGES,
        warn_if_there_are_more_items=False,
        **kwargs,
    ):
        """
        :param async_req bool
        :param str group: Display datasets by a particular group
        :param str sort_by: Sort the results
        :param str filetype: Display datasets of a specific file type
        :param str license: Display datasets with a specific license
        :param str tagids: A comma separated list of tags to filter by
        :param str search: Search terms
        :param str user: Display datasets by a specific user or organization
        :param int start_page: Page to start at (default is 0)
        :param int max_n_pages: Maximum number of pages the container should hold
            (to avoid API overuse)
        :param bool warn_if_there_are_more_items: To be warned if there's more items
            than what you see
        :param int max_size: Max Dataset Size (bytes)
        :param int min_size: Max Dataset Size (bytes)
        :param kwargs:
        """
        explicit_fields = {
            'group',
            'sort_by',
            'filetype',
            'license',
            'tagids',
            'search',
            'user',
        }
        locs = locals()
        kwargs.update(**{k: locs[k] for k in explicit_fields if locs[k] is not None})
        self.dataset_filt = kwargs
        self._source = KaggleApi()
        self._source.authenticate()
        self.start_page = start_page
        self.max_n_pages = max_n_pages
        self.warn_if_there_are_more_items = warn_if_there_are_more_items
        self.last_page = None
        self.max_pages_reached = None

    def _info_items_gen(self):
        page_num = self.start_page
        while (page_num - self.start_page) < self.max_n_pages:
            new_page_contents = self._source.datasets_list(
                page=page_num, **self.dataset_filt
            )
            if len(new_page_contents) > 0:
                yield from new_page_contents
                page_num += 1
            else:
                self.max_pages_reached = True
                break
        self.last_page = page_num

    @lazyprop
    def info_of_ref(self):
        return {item['ref']: item for item in self.cached_info_items}

    @lazyprop
    def cached_info_items(self):
        return list(self._info_items_gen())

    def __iter__(self):
        yield from self.info_of_ref

    def __getitem__(self, k):
        """
        Get information (a dict) about a dataset, given its ref
        (a 'user_slug/dataset_slug' string).
        Note: Allows to access all valid references. Not just those within the current
        container.
        """
        return self.info_of_ref[k]

    def __len__(self):
        n = len(self.info_of_ref)
        self._warn_reached_max(n)
        return n

    def _warn_reached_max(self, n):
        if self.max_pages_reached and self.warn_if_there_are_more_items:
            from warnings import warn

            warn(
                f'The container has {n} items, but the max number of pages'
                f'({self.max_n_pages}) was reached, so there may be more '
                f'on kaggle than what you see! '
                'If you want more, set max_items to something higher '
                '(but beware of overusing your API rights)'
            )


def owner_and_dataset_slugs(ref):
    """try to get the owner and dataset slugs from a ref"""
    try:
        owner_slug, dataset_slug = ref.split('/')
    except ValueError:
        raise ValueError(
            f'Invalid ref: {ref}. Should be of the form "owner_slug/dataset_slug"'
        )
    return owner_slug, dataset_slug


# TODO: Make it less wasteful to get from a KaggleDatasetInfoReader to
#  KaggleDatasetReader.
#   For example, by having a from_info_reader classmethod constructor,
#   or putting both together.
class KaggleBytesDatasetReader(KaggleDatasetInfoReader):
    def __getitem__(self, k):
        """
        Download a dataset, given its ref (a 'user_slug/dataset_slug' string).
        Will return the binary of the dataset, which should be saved to a file to be
        persisted.
        Note: Allows to access all valid references. Not just those within the current
        container.

        >>> s = KaggleDatasetInfoReader()  # doctest: +SKIP
        >>> v = s['rtatman/english-word-frequency']  # doctest: +SKIP
        >>> type(v)  # doctest: +SKIP
        bytes

        """
        owner_slug, dataset_slug = owner_and_dataset_slugs(k)
        response = self._source.process_response(
            self._source.datasets_download_with_http_info(
                owner_slug=owner_slug, dataset_slug=dataset_slug, _preload_content=False
            )
        )
        return response.read()


class KaggleDatasetReader(KaggleBytesDatasetReader):
    def __getitem__(self, k):
        """
        Download a dataset, given its ref (a 'user_slug/dataset_slug' string).
        Will return the binary of the dataset, which should be saved to a file to be
        persisted.
        Note: Allows to access all valid references. Not just those within the current
        container.
        """
        return FilesOfZip(super().__getitem__(k))


class KaggleMetadataReader(KaggleDatasetInfoReader):
    def __getitem__(self, k):
        """Get metadata of a dataset"""
        owner_slug, dataset_slug = owner_and_dataset_slugs(k)
        return self._source.metadata_get(owner_slug, dataset_slug)


# TODO: Get rid of py2store dep
from py2store.stores.local_store import AutoMkDirsOnSetitemMixin, LocalJsonStore


from dol.zipfiledol import ZipFilesReaderAndBytesWriter
from dol.caching import mk_sourced_store
from dol.filesys import (
    mk_relative_path_store,
    LocalFileDeleteMixin,
    ensure_slash_suffix,
)
from dol.trans import add_ipython_key_completions, kv_wrap
from dol.paths import str_template_key_trans
from dol.appendable import appendable


@mk_relative_path_store(prefix_attr='rootdir')
class RelZipFiles(ZipFilesReaderAndBytesWriter, LocalFileDeleteMixin):
    pass


local_zips_key_trans = str_template_key_trans(
    '{user}/{dataset_name}.zip', str_template_key_trans.key_types.str
)
local_meta_key_trans = str_template_key_trans(
    '{user}/{dataset_name}.json', str_template_key_trans.key_types.str
)
remote_key_trans = str_template_key_trans(
    '{user}/{dataset_name}', str_template_key_trans.key_types.str
)


@add_ipython_key_completions
@kv_wrap(local_zips_key_trans)
class LocalKaggleZips(AutoMkDirsOnSetitemMixin, RelZipFiles):
    def __init__(self, rootdir):
        handle_missing_dir(rootdir)
        super().__init__(rootdir=ensure_slash_suffix(rootdir), max_levels=1)


kaggle_remote_datasets_bytes = kv_wrap(remote_key_trans)(KaggleBytesDatasetReader)()

# mk_kaggle_datasets_store(rootdir)
_KaggleDatasets = mk_sourced_store(
    store=LocalKaggleZips,
    source=kaggle_remote_datasets_bytes,
    return_source_data=False,
    __name__='KaggleDatasets',
    __module__=__name__,
)


@add_ipython_key_completions
@appendable(item2kv=appendable.mk_item2kv_for.field('ref'))
@kv_wrap(local_meta_key_trans)
class LocalKaggleMeta(AutoMkDirsOnSetitemMixin, LocalJsonStore):
    def __init__(self, rootdir):
        handle_missing_dir(rootdir)
        super().__init__(path_format=ensure_slash_suffix(rootdir), max_levels=1)


# mk_kaggle_datasets_store(rootdir)
KaggleMeta = mk_sourced_store(
    store=LocalKaggleMeta,
    source=KaggleMetadataReader(),
    return_source_data=True,
    __name__='KaggleMeta',
    __module__=__name__,
)


# TODO: Add caching of search results info locally
@add_ipython_key_completions
class KaggleDatasets(_KaggleDatasets):
    def __init__(self, rootdir=DFLT_ROOTDIR, cache_metas_on_search=True):
        rootdir = rootdir or DFLT_ROOTDIR
        handle_missing_dir(rootdir, 'You (or defaults) asked for a rootdir...')
        self.rootdir = rootdir
        handle_missing_dir(self.zips_dir, ask_first=False)
        handle_missing_dir(self.meta_dir, ask_first=False)
        super().__init__(self.zips_dir)  # make the _KaggleDatasets instance
        self.meta = KaggleMeta(self.meta_dir)  # make the LocalKaggleInfo instance
        self.cache_metas_on_search = cache_metas_on_search

    def pjoin(self, *p):
        return os.path.join(self.rootdir, *p)

    @property
    def zips_dir(self):
        return self.pjoin('zips')

    @property
    def meta_dir(self):
        return self.pjoin('meta')

    @property
    def kaggle_api(self):
        return (
            self._src.store._source
        )  # TODO: Use dig methods instead (also perfect example of inconsistent naming!)

    def search(self, search_term):
        ka = KaggleDatasetInfoReader(search=search_term)
        if self.cache_metas_on_search:
            self.meta.extend(ka.cached_info_items)  # cache these
        return ka
