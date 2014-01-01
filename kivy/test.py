#!/usr/bin/python

def test(**d):
    for count, thing in d.items():
        print '{0}. {1}'.format(count, thing)

test(apple = '1,', fsdf = '2', fsdfd = '3')