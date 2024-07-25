from jobscriptgenerator.alias_handler import AliasHandler


class Foo(AliasHandler):
    pass


def test_alias_handler():
    foo = Foo()
    obj1 = object()
    obj2 = object()

    foo.bar = obj1
    foo.add_alias("bar", "my_bar")
    foo.add_alias("bar", "my_foo")

    assert foo.my_bar is obj1
    foo.my_foo = obj2
    assert foo.bar is obj2

    foo.foo = None
    foo.add_alias("foo", "foofoo")

    del foo.my_bar
    assert not (hasattr(foo, "bar") or hasattr(foo, "my_foo") or hasattr(foo, "my_bar"))
    assert hasattr(foo, "foofoo")


def test_alias_handler_with_alias():
    foo = Foo()
    obj = object()

    foo.add_alias("bar", "my_bar")
    foo.my_bar = obj

    assert foo.bar is obj
    assert "bar" in foo.__dict__
