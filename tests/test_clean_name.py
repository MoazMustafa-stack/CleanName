from filename_utils import clean_name


def test_clean_name_examples():
    assert (
        clean_name(
            "FALLSEM2025-26_VL_BSTS302P_00100_SS_2025-07-28_The-Celebrity-problem.pdf"
        )
        == "The-Celebrity-problem.pdf"
    )

    assert clean_name("example_file_name.txt") == "name.txt"
    assert clean_name("no_underscore.pdf") == "underscore.pdf"
    assert clean_name("nounderscore") == "nounderscore"
