def text_without_children(q):
    return "".join(text_nodes_without_children(q))

def text_nodes_without_children(q):
    return [e for e in q.contents() if isinstance(e, str)]
