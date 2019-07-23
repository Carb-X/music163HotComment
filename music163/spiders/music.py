# -*- coding: utf-8 -*-

import json
from scrapy import Spider, Request, FormRequest
from music163.items import Music163Item
from music163.settings import DEFAULT_REQUEST_HEADERS


class MusicSpider(Spider):

    name = 'music'
    allowed_domains = ['163.com']
    base_url = 'https://music.163.com/'

    # 歌手分类url: https://music.163.com/#/discover/artist/cat?id=1001&amp;initial=65 中的id与initial参数集合
    ids = ['1001', '1002', '1003', '2001', '2002', '2003', '6001',
           '6002', '6003', '7001', '7002', '7003', '4001', '4002', '4003']
    initials = [i for i in range(65, 91)]+[0]

    def start_requests(self):
        """ 生成歌手分类页url """

        for ID in self.ids:
            for initial in self.initials:
                url = '{url}/discover/artist/cat?id={id}&initial={initial}'.format(url=self.base_url,
                                                                                   id=ID,
                                                                                   initial=initial)
                yield Request(url, callback=self.parse_index)

    def parse_index(self, response):
        """ 获取歌手id，生成歌手专辑页url """

        artists = response.xpath('//*[@id="m-artist-box"]/li/div/a/@href').extract()
        for artist in artists:
            artist_url = self.base_url + '/artist' + '/album?' + artist[8:]
            yield Request(artist_url, callback=self.parse_artist)

    def parse_artist(self, response):
        """ 获取专辑id，生成每个专辑url """

        albums = response.xpath('//*[@id="m-song-module"]/li/div/a[@class="msk"]/@href').extract()
        for album in albums:
            album_url = self.base_url + album
            yield Request(album_url, callback=self.parse_album)

    def parse_album(self, response):
        """ 获取歌曲id，生成每首歌曲的url """

        musics = response.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        for music in musics:
            music_id = music[9:]
            music_url = self.base_url + music
            yield Request(music_url, meta={'id': music_id}, callback=self.parse_music)

    def parse_music(self, response):
        """ 获取歌曲的歌名和演唱者，模拟获取评论的ajax请求 """

        music_id = response.meta['id']
        music = response.xpath('//div[@class="tit"]/em[@class="f-ff2"]/text()').extract_first()
        artist = response.xpath('//div[@class="cnt"]/p[1]/span/a/text()').extract_first()

        data = {
            'csrf_token': '',
            'params': 'copy-your-params-here',
            'encSecKey': 'copy-your-encSecKey-here'
        }
        DEFAULT_REQUEST_HEADERS['Referer'] = self.base_url + '/playlist?id=' + str(music_id)
        music_comment_url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(music_id)

        yield FormRequest(music_comment_url,
                          meta={'id': music_id, 'music': music, 'artist': artist},
                          callback=self.parse, formdata=data)

    def parse(self, response):
        """ 获取热评，生成item """

        id = response.meta['id']
        music = response.meta['music']
        artist = response.meta['artist']
        result = json.loads(response.text)
        comments = []
        if 'hotComments' in result.keys():
            for comment in result.get('hotComments'):
                comments.append(comment['content'])

        item = Music163Item()
        for field in item.fields:
            try:
                item[field] = eval(field)
            except:
                print('Field is not defined', field)
        yield item
