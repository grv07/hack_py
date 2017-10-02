from collections import OrderedDict
import datetime
from django.utils.timezone import utc


def reply_on_comments(comments):
    comment_and_reply = OrderedDict({})
    comment_only = []
    comment_id_dict = OrderedDict()
    for comment in comments:
        comment_id_dict[comment.id] = comment
        if comment.is_reply:
            comment_and_reply.setdefault(comment.parent_comment_id, []).append(comment.id)
        else:
            comment_and_reply.setdefault(comment.id, [])
            # comment_only.append(comment.id)
    data = []
    _call = comment_and_reply.keys()
    # comment_only = [comment for comment in comment_only if comment not in _call]
    while len(_call) > 0:
        _seq = get_sequence(comment_and_reply, _call[0])
        data.extend(_seq)
        _call = [_c for _c in _call if _c not in _seq]
    # data.extend(comment_only)
    sequence_comment_list = []
    for seq_comment_id in data:
        if comment_id_dict.has_key(seq_comment_id):
            sequence_comment_list.append(comment_id_dict[seq_comment_id])
    return sequence_comment_list


def get_sequence(data, pre_key):
    _temp_final = []
    if pre_key:
        _temp_final.append(pre_key)
        for d in data.get(pre_key, []):
            seq_data = get_sequence(data, d)
            _temp_final.extend(seq_data)
    return _temp_final


def get_time_diff(self):
    if self.created_time:
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff = now - self.created_time
        _diff_sec = timediff.total_seconds()
        if _diff_sec < 60 :
            return str(int(round(timediff.total_seconds()))) + " sec ago"
        elif (_diff_sec/60) < 59:
            return str(int(round(timediff.total_seconds() / 60))) + " minutes ago"
        else:
            return str(int(round((timediff.total_seconds() / 60) / 60, 0))) + " hours ago"