from oarepo_model_builder.stack import ModelBuilderStack

def test_stack():
    stack = ModelBuilderStack()
    stack.push('a', {'b': [1, 2]})
    assert stack.path == '/a'
    assert stack.top.key == 'a'
    assert stack.top.data == {'b': [1, 2]}
    stack.push('b', [1, 2])
    assert stack.path == '/a/b'
    assert stack.top.key == 'b'
    assert stack.top.data == [1, 2]
    stack.pop()
    assert stack.path == '/a'
    assert stack.top.key == 'a'
    assert stack.top.data == {'b': [1, 2]}
    stack.pop()