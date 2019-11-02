import pytest


@pytest.mark.pytestto
class TestPytestDemo(object):
    def setup_class(self):
        pass

    @pytest.mark.asserttest
    def test_assert(self):
        assert 3 < 4, "3期望是小于4"

    @pytest.mark.strtest
    def test_str(self):
        b = "hello"
        assert "h" in b, "字符h期望在单词hello中出现"