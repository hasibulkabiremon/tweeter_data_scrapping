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
        scraped_at,
        total_views=None,
        source_img=None,
        scraping_duration=None,
        device=None,
        source_id=None,
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
        self.total_views = total_views
        self.source_img = source_img
        self.scraping_duration = scraping_duration
        self.scraped_at = scraped_at
        self.device = device
        self.source_id = source_id


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


from datetime import datetime


class CreatedBy:
    def __init__(
        self,
        id,
        created_by,
        created_at,
        created_from,
        modified_by,
        modified_at,
        modified_from,
        is_archived,
        archived_by,
        archived_at,
        archived_from,
        remarks,
        status,
        name,
        description,
        permission,
    ):
        self.id = id
        self.created_by = created_by
        self.created_at = datetime.fromisoformat(created_at) if created_at else None
        self.created_from = created_from
        self.modified_by = modified_by
        self.modified_at = datetime.fromisoformat(modified_at) if modified_at else None
        self.modified_from = modified_from
        self.is_archived = is_archived
        self.archived_by = archived_by
        self.archived_at = datetime.fromisoformat(archived_at) if archived_at else None
        self.archived_from = archived_from
        self.remarks = remarks
        self.status = status
        self.name = name
        self.description = description
        self.permission = permission


class FbUser:
    def __init__(
        self,
        id,
        title,
        platform,
        name,
        email,
        username,
        phone,
        password,
        status,
    ):
        self.id = id
        self.title = title
        self.platform = platform
        self.name = name
        self.email = email
        self.username = username
        self.phone = phone
        self.password = password
        self.status = status


class Source:
    def __init__(
        self,
        id,
        title,
        url,
        platform,
        type,
        is_active,
    ):
        self.id = id
        self.title = title
        self.url = url
        self.platform = platform
        self.type = type
        self.is_active = is_active


class DeviceData:
    def __init__(
        self,
        id,
        device_name,
        platform,
        device,
        fb_user,
        hostname,
        last_running,
        node_status,
        sources,
        scraping_duration,
    ):
        self.id = id
        self.device_name = device_name
        self.platform = platform
        self.device = device
        self.fb_user = FbUser(**fb_user)
        self.hostname = hostname
        self.last_running = (
            datetime.fromisoformat(last_running) if last_running else None
        )
        self.node_status = node_status
        self.sources = [Source(**source) for source in sources]
        self.scraping_duration = scraping_duration


class Response:
    def __init__(
        self,
        status,
        message,
        data,
    ):
        self.status = status
        self.message = message
        try:
            self.data = DeviceData(**data)
        except Exception as e:
            self.data = []
            print(e)
