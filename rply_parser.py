'''
Copyright (c) Alex Gaynor and individual contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of rply nor the names of its contributors may be used
       to endorse or promote products derived from this software without
       specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
# 摘自 rply 源码, commit 6e16262dc6d434fc467eed83ed31ca764ba01a34
from rply.errors import ParsingError


class LRParser(object):
    def __init__(self, lrparser):
        self.lr_table = lrparser.lr_table
        self.error_handler = lrparser.error_handler

    def parse(self, tokenizer, state=None):
        from rply.token import Token

        lookahead = None
        lookaheadstack = []

        statestack = [0]
        symstack = [Token("$end", "$end")]

        current_state = 0
        while True:
            if self.lr_table.default_reductions[current_state]:
                t = self.lr_table.default_reductions[current_state]
                current_state = self._reduce_production(
                    t, symstack, statestack, state
                )
                continue

            if lookahead is None:
                if lookaheadstack:
                    lookahead = lookaheadstack.pop()
                else:
                    try:
                        lookahead = next(tokenizer)
                    except StopIteration:
                        lookahead = None

                if lookahead is None:
                    lookahead = Token("$end", "$end")

            ltype = lookahead.gettokentype()
            if ltype in self.lr_table.lr_action[current_state]:
                t = self.lr_table.lr_action[current_state][ltype]
                if t > 0:
                    statestack.append(t)
                    current_state = t
                    symstack.append(lookahead)
                    lookahead = None
                    continue
                elif t < 0:
                    current_state = self._reduce_production(
                        t, symstack, statestack, state
                    )
                    continue
                else:
                    n = symstack[-1]
                    return n
            else:
                # TODO: actual error handling here
                if self.error_handler is not None:
                    if state is None:
                        self.error_handler(lookahead)
                    else:
                        self.error_handler(state, lookahead)
                    lookahead = None
                    continue
                else:
                    raise ParsingError(None, lookahead.getsourcepos())

    def _reduce_production(self, t, symstack, statestack, state):
        # reduce a symbol on the stack and emit a production
        p = self.lr_table.grammar.productions[-t]
        pname = p.name
        plen = p.getlength()
        start = len(symstack) + (-plen - 1)
        assert start >= 0
        targ = symstack[start + 1:]
        start = len(symstack) + (-plen)
        assert start >= 0
        del symstack[start:]
        del statestack[start:]
        if state is None:
            value = p.func(targ)
        else:
            value = p.func(state, targ)
        symstack.append(value)
        current_state = self.lr_table.lr_goto[statestack[-1]][pname]
        statestack.append(current_state)
        return current_state
