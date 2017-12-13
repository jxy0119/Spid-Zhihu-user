# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from zhihuuser.items import ZhihuuserItem
import json


class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    follows_url = '''https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&amp; 
                  offset={offset}&amp;limit={limit}'''
    start_user = 'excited-vczh'
    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,' \
                 'follower_count,following_count,cover_url,following_topic_count,' \
                 'following_question_count,following_favlists_count,following_columns_count,' \
                 'avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,' \
                 'commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,' \
                 'marked_answers_text,message_thread_token,account_status,is_active,is_bind_phone,' \
                 'is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,' \
                 'show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,' \
                 'vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,' \
                 'description,hosted_live_count,participated_live_count,allow_message,industry_category,' \
                 'org_name,org_homepage,badge[?(type=best_answerer)].topics'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,' \
                    'badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), self.parse_user)
        yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20),
                      self.parse_follow)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = ZhihuuserItem()
        for field in item:
            if field in result.keys():
                item[field] = result.get(field)
        yield item
        yield Request(self.user_url.format(user=result.get('url_token'), include=self.follows_query),
                      self.parse_follow)
# print(response.text)

    def parse_follow(self, response):
        results = json.loads(response.text)
        if 'data'in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.follows_query),
                              self.parse_user)
        if 'paging'in results.keys()and results.get('paging').get('is_end') is False:
            next_page = results.get('paging').get('next')
            yield Request(next_page, self.parse_follow)


# print(response.text)

    def parse(self, response):
        pass
