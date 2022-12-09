# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class NoiceIE(InfoExtractor):
    IE_NAME = 'noice'
    _VALID_URL = r'https://open\.noice\.id/content/(?P<id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
    _TEST = {
        'url': 'https://open.noice.id/content/531140f5-2af8-4a08-8689-707a3bb04354',
        'info_dict': {
            'id': '531140f5-2af8-4a08-8689-707a3bb04354',
            'ext': 'mp3',
            'title': 'Eps 77: Bullying, Kepala Charger, Leukemia',
            'series': 'Lambemu',
            'description': 'md5:c830af36307cff3f73a5abafaa10362c',
        }
    }

    def _real_extract(self, url):
        podcast_id = self._match_id(url)
        webpage = self._download_webpage(url, podcast_id,
                                         headers={'User-Agent': 'Mozilla/5.0'})

        content = self._parse_json(self._search_regex(
            r'<script[^>]+id="__NEXT_DATA__"[^>]*>({.+?})</script>',
            webpage, 'json __NEXT_DATA__'), podcast_id)['props']['pageProps']['contentDetails']

        return {
            'id': content.get('id') or podcast_id,
            'title': content.get('title'),
            'description': content.get('description'),
            'ext': 'mp3',
            'series': content['catalog']['title'],
            'url': content.get('rawContentUrl'),
            'format_id': 'mp3',
            'vcodec': 'none',
            'acodec': 'mp3',
            'thumbnails': [{
                'id': content.get('id') or podcast_id,
                'url': content.get('image')
            }],
        }


class NoiceCatalogIE(InfoExtractor):
    IE_NAME = 'noice:catalog'
    _VALID_URL = r'https://open\.noice\.id/catalog(/episodes)?/(?P<id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
    _TEST = {
        'url': 'https://open.noice.id/catalog/ce9867f1-15aa-4ecc-85fa-269dc9008aa3',
        'info_dict': {
            'id': 'ce9867f1-15aa-4ecc-85fa-269dc9008aa3',
            'title': 'Musuh Masyarakat',
            'description': 'Tretan Muslim & Adriano Qalbi hadir dengan opini-opini berani & kontroversial yang mungkin bisa bikin mereka jadi Musuh Masyarakat.',
        },
        'playlist_mincount': 4,
    }

    def _real_extract(self, url):
        catalog_id = self._match_id(url)
        webpage = self._download_webpage(url, catalog_id,
                                         headers={'User-Agent': 'Mozilla/5.0'})

        catalog = self._parse_json(self._search_regex(
            r'<script[^>]+id="__NEXT_DATA__"[^>]*>({.+?})</script>',
            webpage, 'json __NEXT_DATA__'), catalog_id)['props']['pageProps']['catalogDetails']

        entries = []
        for content in catalog.get('contents'):
            entries.append({
                'id': content.get('id'),
                'title': content.get('title'),
                'description': content.get('description'),
                'ext': 'mp3',
                'session': content['seasonName'],
                'url': content.get('rawContentUrl'),
                'format_id': 'mp3',
                'vcodec': 'none',
                'acodec': 'mp3',
                'thumbnails': [{
                    'id': content.get('id'),
                    'url': content.get('image')
                }],
            })

        return self.playlist_result(entries,
                                    playlist_id=catalog.get('id'),
                                    playlist_title=catalog.get('title'),
                                    playlist_description=catalog.get('description'))
