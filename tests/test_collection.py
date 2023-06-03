# from sys import settrace
# from callcache.callhooks import tracer, set_watch_files
# from callcache.cache.file import list_args_for_func


# def test_one():

#     def foo(bar, baz):
#         return bar(baz)

#     def spam(name):
#         print(f"Hello, {name}")
#         return 5

#     set_watch_files([__file__])
#     settrace(tracer)
#     foo(spam, "universe")

#     spam("one")
#     spam("two")

#     foo(spam, "goose")
#     settrace(None)

#     assert ['universe', 'one', 'two', 'goose'] == list(map(lambda x: x.locals['name'], list_args_for_func(__file__, 'spam')))
