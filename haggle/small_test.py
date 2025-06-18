"""
Some tests
"""

from haggle.dacc import KaggleDatasets


def simple_smoke_test():
    s = KaggleDatasets()  # make an instance
    # results = s.search('coronavirus')
    # ref = next(iter(results))  # see that results iteration works
    ref = "sanchman/coronavirus-present-data"
    if ref in s:  # delete if exists
        del s[ref]
    assert ref not in s  # see, not there
    v = s[ref]  # redownload
    assert ref in s  # see, not there
    assert "PresentData.xlsx" in set(v)  # and it has stuff in v

    try:
        import pandas as pd
        import io

        df = pd.read_excel(io.BytesIO(v["PresentData.xlsx"]))
        assert "Total Confirmed" in df.columns
        assert "Country" in df.columns
        assert "France" in df["Country"].values
    except ModuleNotFoundError:
        pass
