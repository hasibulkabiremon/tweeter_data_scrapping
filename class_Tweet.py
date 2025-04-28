class Tweet:
    def __init__(
        self,
        # _id,
        type,
        source,
        post_url,
        post_title,
        post_url_web,
        url_screenshot,
        posted_at,
        post_text,
        post_topic,
        comments,
        reactions,
        featured_image,
        total_comments,
        percent_comments,
        total_shares,
        vitality_score,
        checksum,
    ):
        # self._id = _id.__dict__
        self.type = type
        self.source = source
        self.post_url = post_url
        self.post_title = post_title
        self.post_url_web = post_url_web
        self.url_screenshot = url_screenshot
        self.posted_at = posted_at
        self.post_text = post_text
        self.post_topic = post_topic.__dict__
        self.comments = []
        for comment in comments:
            if comment is not None:
                self.comments.append(comment.__dict__)
        self.reactions = reactions.__dict__
        self.featured_image = featured_image
        self.total_comments = total_comments
        self.percent_comments = percent_comments
        self.total_shares = total_shares
        self.vitality_score = vitality_score
        self.checksum = checksum


class ID:
    def __init__(self, oid):
        self.oid = oid


class PostedAt:
    def __init__(self, posted_at):
        self.posted_at = posted_at


class Topic:
    def __init__(self, label, score):
        self.label = label
        self.score = score


class PostTopic:
    def __init__(self, status, topic):
        self.status = status
        self.topic = topic.__dict__


class Comment:
    def __init__(
        self,
        user_pro_pic,
        comment_time,
        user_name,
        user_profile_url,
        comment_text,
        comments_replies_list,
    ):
        self.user_pro_pic = user_pro_pic
        self.comment_time = comment_time
        self.user_name = user_name
        self.user_profile_url = user_profile_url
        self.comment_text = comment_text
        self.comment_replies = comments_replies_list


class Reactions:
    def __init__(self, Total, Sad, Love, Wow, Like, Haha, Angry, Care):
        self.Total = Total
        self.Sad = Sad
        self.Love = Love
        self.Wow = Wow
        self.Like = Like
        self.Haha = Haha
        self.Angry = Angry
        self.Care = Care
