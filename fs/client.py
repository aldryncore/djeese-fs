# -*- coding: utf-8 -*-
from django.utils.encoding import smart_str
from fs.security import sign
import hashlib
import json
import os
import requests


class SyncClient(object):
    '''
    Synchronouse (blocking) client
    '''
    def __init__(self, access_id, access_key, host):
        self.access_id = str(access_id)
        self.access_key = str(access_key)
        self.host = host
        self.session = requests.session(headers={'djeesefs-access-id': self.access_id})
        
    def _sign(self, data, keys=None):
        if keys is not None:
            data = dict((k, v) for k, v in data.items() if k in keys)
        return sign(self.access_key, data)
    
    def _get_url(self, method):
        return '/'.join([self.host, method])
    
    def _post(self, method, data, keys=None):
        headers = {
            'djeesefs-signature': self._sign(data, keys), 
        }
        url = self._get_url(method)
        return self.session.post(url, data=data, headers=headers)
    
    def _get(self, method, params, keys=None):
        headers = {
            'djeesefs-signature': self._sign(params, keys), 
        }
        url = self._get_url(method)
        return self.session.get(url, params=params, headers=headers)
        
    def delete(self, name):
        data = {'name': name}
        response = self._post('delete', data)
        return response.ok
    
    def exists(self, name):
        params = {'name': name}
        response = self._get('exists', params)
        return response.ok
    
    def listdir(self, path):
        params = {'name': path}
        response = self._get('listdir', params)
        response.raise_for_status()
        return json.loads(response.content)
    
    def size(self, name):
        params = {'name': name}
        response = self._get('size', params)
        response.raise_for_status()
        return int(response.content)
    
    def url(self, name):
        params = {'name': name}
        response = self._get('url', params)
        if not response.ok:
            return ''
        return response.content
    
    def get_content(self, name):
        url = self.url(name)
        response = requests.get(url)
        if not response.ok:
            return ''
        return response.content
    
    def save(self, name, fileobj):
        fileobj.seek(0)
        data = {'name': name}
        response = self._post('save', data)
        response.raise_for_status()
        info = json.loads(response.content)
        key, chunk_size = info['key'], info['chunk_size']
        while True:
            data = {'key': key}
            chunk = fileobj.read(chunk_size)
            if chunk:
                data['chunk'] = chunk
                response = self._post('upload', data, keys=['key'])
                response.raise_for_status()
            else:
                response = self._post('finish', data)
                response.raise_for_status()
                break
        fileobj.seek(0)
        return True
    
    def get_valid_name(self, name):
        name, ext = os.path.splitext(name)
        return '%s%s' % (hashlib.md5(smart_str(name)).hexdigest(), ext)
    
    def get_available_name(self, name):
        params = {'name': name}
        response = self._get('available-name', params)
        response.raise_for_status()
        return response.content

    def copy_container(self, source_access_id, source_access_key):
        """
        Copies the contents of another container into this one.
        Warning: Deletes EVERYTHING inside the current container!

        Requires the access credentials of the source container.
        """
        # we additionally sign our source container data with
        # the source container secret. The server can then
        # check both signatures to verify that the caller has
        # knowledge of the secrets for both containers.
        data = {'source_id': source_access_id}
        data['source_signature'] = sign(source_access_key, data)
        response = self._post('copy-container', data)
        return response.ok
