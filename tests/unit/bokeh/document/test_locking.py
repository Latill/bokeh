#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2024, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import annotations # isort:skip

import pytest ; pytest

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
import asyncio

# Bokeh imports
from bokeh.document.document import Document
from bokeh.io import curdoc

# Module under test
import bokeh.document.locking as locking # isort:skip

#-----------------------------------------------------------------------------
# Setup
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

def test_next_tick_callback_works() -> None:
    d = locking.UnlockedDocumentProxy(Document())
    assert curdoc() is not d
    curdoc_from_cb: list[Document] = []
    def cb():
        curdoc_from_cb.append(curdoc())
    callback_obj = d.add_next_tick_callback(cb)
    callback_obj.callback()
    assert len(curdoc_from_cb) == 1
    assert curdoc_from_cb[0] is d._doc
    def cb2(): pass
    callback_obj = d.add_next_tick_callback(cb2)
    d.remove_next_tick_callback(callback_obj)

def test_other_attrs_raise() -> None:
    d = locking.UnlockedDocumentProxy(Document())
    assert curdoc() is not d
    for attr in (set(dir(d._doc)) - set(dir(d))) | {'foo'}:
        with pytest.raises(AttributeError) as e:
            getattr(d, attr)
        assert e.value.args[0] == locking.UNSAFE_DOC_ATTR_USAGE_MSG

def test_without_document_lock() -> None:
    d = Document()
    assert curdoc() is not d
    curdoc_from_cb: list[Document] = []
    @locking.without_document_lock
    def cb():
        curdoc_from_cb.append(curdoc())
    callback_obj = d.add_next_tick_callback(cb)
    callback_obj.callback()
    assert callback_obj.callback.nolock is True
    assert len(curdoc_from_cb) == 1
    assert curdoc_from_cb[0]._doc is d
    assert isinstance(curdoc_from_cb[0], locking.UnlockedDocumentProxy)

def test_without_document_lock_accepts_async_function() -> None:
    i = 0
    d = Document()

    @locking.without_document_lock
    async def cb():
        nonlocal i
        await asyncio.sleep(0.1)
        i += 1
    callback_obj = d.add_next_tick_callback(cb)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(callback_obj.callback())

    assert callback_obj.callback.nolock is True
    assert i == 1

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
