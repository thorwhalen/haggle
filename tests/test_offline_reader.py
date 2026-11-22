"""Offline tests for haggle.dacc with a fake KaggleApi (no credentials, no network)."""

import io
import os
import zipfile

import pytest

from haggle import dacc


class _Item:
    def __init__(self, ref):
        self.ref = ref


class FakeApi:
    pages = [[_Item("a/one"), _Item("a/two")], [_Item("b/three")], []]
    downloads = []
    write_zip = True

    def authenticate(self):
        pass

    def dataset_list(self, page, **filt):
        FakeApi.last_filt = filt
        idx = page - 1  # reader starts at page 1
        return self.pages[idx] if 0 <= idx < len(self.pages) else []

    def dataset_download_files(self, dataset, path, quiet, force):
        FakeApi.downloads.append(dataset)
        if FakeApi.write_zip:
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as z:
                z.writestr("data.csv", "x\n1\n")
            with open(os.path.join(path, "d.zip"), "wb") as f:
                f.write(buf.getvalue())


@pytest.fixture(autouse=True)
def fake_api(monkeypatch, tmp_path):
    monkeypatch.setattr(dacc, "KaggleApi", FakeApi)
    monkeypatch.chdir(tmp_path)  # the bytes reader uses a relative temp dir
    FakeApi.downloads = []
    FakeApi.write_zip = True


def test_info_reader_pages_and_filters():
    r = dacc.KaggleDatasetInfoReader(search="covid", user="u", max_n_pages=5)
    assert list(r) == ["a/one", "a/two", "b/three"]
    assert len(r) == 3
    assert r["b/three"].ref == "b/three"
    assert r.max_pages_reached is True
    assert FakeApi.last_filt == {"search": "covid", "user": "u"}
    with pytest.raises(KeyError):
        r["nope/nope"]


def test_info_reader_respects_max_pages_and_warns():
    r = dacc.KaggleDatasetInfoReader(max_n_pages=1, warn_if_there_are_more_items=True)
    assert list(r) == ["a/one", "a/two"]
    assert r.last_page == 2
    r.max_pages_reached = True  # as if the API had more
    with pytest.warns(UserWarning, match="max number of pages"):
        len(r)


def test_owner_and_dataset_slugs():
    assert dacc.owner_and_dataset_slugs("me/data") == ("me", "data")
    with pytest.raises(ValueError, match="owner_slug/dataset_slug"):
        dacc.owner_and_dataset_slugs("no-slash")
    with pytest.raises(ValueError):
        dacc.owner_and_dataset_slugs("a/b/c")


def test_bytes_reader_returns_zip_and_cleans_up(tmp_path):
    r = dacc.KaggleBytesDatasetReader()
    b = r["me/data"]
    assert FakeApi.downloads == ["me/data"]
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        assert z.namelist() == ["data.csv"]
    assert not os.path.exists("_temp_kaggle_downloads/me_data")


def test_bytes_reader_missing_zip_raises_and_cleans_up():
    FakeApi.write_zip = False
    with pytest.raises(FileNotFoundError, match="No zip file"):
        dacc.KaggleBytesDatasetReader()["me/data"]
    assert not os.path.exists("_temp_kaggle_downloads/me_data")


def test_paged_items_index_by_ref():
    p = dacc.DataInfoPaggedItems()
    p.append([_Item("x/1"), _Item("x/2")])
    p.append([_Item("y/3")])
    assert len(p) == 3 and p.n_pages() == 2
    assert p["y/3"].ref == "y/3" and p.get_page_contents(0)[1].ref == "x/2"


def test_clog_and_handle_missing_dir(tmp_path, capsys, monkeypatch):
    dacc.clog(True, "hello")
    dacc.clog(False, "silent")
    assert capsys.readouterr().out == "hello\n"
    target = str(tmp_path / "newdir")
    dacc.handle_missing_dir(target, ask_first=False, verbose=False)
    assert os.path.isdir(target)
    other = str(tmp_path / "declined")
    monkeypatch.setattr("builtins.input", lambda _="": "n")
    dacc.handle_missing_dir(other, verbose=False)
    assert not os.path.exists(other)
    third = str(tmp_path / "accepted")
    monkeypatch.setattr("builtins.input", lambda _="": "")
    dacc.handle_missing_dir(third, verbose=False)
    assert os.path.isdir(third)
