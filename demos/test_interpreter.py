#!/usr/bin/python
# Test interpreter
# by Albert Zeyer, 2011
# code under GPL

import sys, os, os.path
if __name__ == '__main__':
    MyDir = os.path.dirname(sys.argv[0]) or "."
else:
    MyDir = "."

sys.path.append(MyDir + "/../..") # so that 'import cinterpreter' works as expected
sys.path.append(MyDir + "/..") # so that 'import better_exchook' works

#~ import better_exchook
#~ better_exchook.install()

import cinterpreter

def prepareState():
    state = cinterpreter.State()
    state.autoSetupSystemMacros()
    state.autoSetupGlobalIncludeWrappers()
    return state

state = prepareState()
cinterpreter.parse(MyDir + "/test_interpreter.c", state)

import cinterpreter.interpreter

interpreter = cinterpreter.interpreter.Interpreter()
interpreter.register(state)

if __name__ == '__main__':
    print "erros so far:"
    for m in state._errors:
        print m

    for f in state.contentlist:
        if not isinstance(f, cinterpreter.CFunc): continue
        if not f.body: continue

        print
        print "parsed content of " + str(f) + ":"
        for c in f.body.contentlist:
            print c

    print
    print "PyAST of main:"
    interpreter.dumpFunc("main")

    print
    print
    interpreter.runFunc("main", len(sys.argv), sys.argv + [None])

