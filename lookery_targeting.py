#!/usr/bin/env python

#  This software code is made available "AS IS" without warranties of any
#  kind.  You may copy, display, modify and redistribute the software
#  code either by itself or as incorporated into your code; provided that
#  you do not remove any proprietary notices.  Your use of this software
#  code is at your own risk and you waive any claim against Amazon
#  Digital Services, Inc. or its affiliates with respect to your use of
#  this software code. (c) 2007-2009 Lookery

import base64
import hmac
import sha
import sys
import time
import urllib
import urlparse

LOOKERY_TAPI_VERSION = 2
DEFAULT_LOOKERY_BASE = 'http://services.lookery.com/targeting?'

class LookeryTargeting:
  
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    # computes the base64'ed hmac-sha hash of the canonical string and the secret
    # access key, optionally urlencoding the result
    def encode(self, str, urlencode=False):
        b64_hmac = base64.encodestring(hmac.new(self.secret_key, str, sha).digest()).strip()
        if urlencode:
            return urllib.quote_plus(b64_hmac)
        else:
            return b64_hmac

    # builds the query arg string
    def query_args_hash_to_string(self, query_args):
        query_string = ""
        pairs = []
        for k, v in query_args.items():
            piece = k
            if v != None:
                piece += "=%s" % urllib.quote_plus(str(v))
            pairs.append(piece)

        return '&'.join(pairs)
        
    def redirect(self, url, extra_params={}):
          timestamp = int(time.time())
          data = "LookeryTargeting%d%d" % (LOOKERY_TAPI_VERSION,timestamp)
          signature = self.encode(data, True)
          params = {}
          params["v"] = LOOKERY_TAPI_VERSION
          params["api_key"] = self.api_key
          params["r_url"] = urllib.quote_plus(url)
          params["timestamp"] = timestamp
          params["signature"] = signature

          params.update(extra_params)
          query = self.query_args_hash_to_string(params)
          
          return "%s%s" % (DEFAULT_LOOKERY_BASE, query)
          
if __name__ == "__main__":
  
  targeting = LookeryTargeting("<INSERT YOUR API KEY HERE>","<INSERT YOUR SECRET KEY HERE>")
  redirect = targeting.redirect("http://www.example.com/?a={profile_yob}&g={profile_gender")
  print redirect