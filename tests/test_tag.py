from article.tag import Tag


class TestTag:
    def test_tag_add(self):
        a = ["abc"]
        Tag.tag_add("def", a)

        assert a == ["abc", "def"]

    def test_tag_scan(self):
        assert False
