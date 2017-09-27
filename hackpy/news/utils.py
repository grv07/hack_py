from collections import OrderedDict


def reply_on_comments(comments):
    comment_and_reply = OrderedDict({})
    comment_only = []
    comment_id_dict = {}
    for comment in comments:
        comment_id_dict[comment.id] = comment
        if comment.is_reply:
            comment_and_reply.setdefault(comment.parent_comment_id, []).append(comment.id)
        else:
            comment_only.append(comment.id)
    data = []
    _call = comment_and_reply.keys()
    comment_only = [comment for comment in comment_only if comment not in _call]
    while len(_call) > 0:
        _seq = get_sequence(comment_and_reply, _call[0])
        data.extend(_seq)
        _call = [_c for _c in _call if _c not in _seq]
    data.extend(comment_only)
    sequence_comment_list = []
    for seq_comment_id in data:
        sequence_comment_list.append(comment_id_dict[seq_comment_id])
    # print sequence_comment_list
    return sequence_comment_list


def get_sequence(data, pre_key):
    _temp_final = []
    if pre_key:
        _temp_final.append(pre_key)
        for d in data.get(pre_key, []):
            seq_data = get_sequence(data, d)
            _temp_final.extend(seq_data)
    return _temp_final
