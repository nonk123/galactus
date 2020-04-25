def text_without_children(q):
    return q.clone().children().remove().end().text()
