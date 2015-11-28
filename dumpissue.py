#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
dumpissue.py  --- 用于备份issues

使用GitHub的API，比如:

$ curl  https://api.github.com/repos/LeslieZhu/MinYi/issues

以JSON格式获取项目的issue状态，进而对issue做其它操作。
'''

import sys,os
import urllib2
import json


def dumpIssues(state="open", repo=u"MinYi", user=u"LeslieZhu"):
    content = urllib2.urlopen(u"https://api.github.com/repos/%s/%s/issues?state=%s" % (user,repo,state,))
    issues = json.loads(content.read())
    
    for issue in issues:
        # [u'body', u'labels', u'locked', u'title', u'url', u'labels_url', u'created_at', u'events_url', u'comments_url', u'html_url', u'comments', u'number', u'updated_at', u'assignee', u'state', u'user', u'milestone', u'closed_at', u'id']

        title = issue[u"title"]
        number = issue[u"number"]
        
        label = issue[u"labels"][0][u"name"]
        label_folder = u"issues/%s" % (label,)
        
        if not os.path.exists(label_folder):
            os.makedirs(label_folder)

        created_at = issue[u"updated_at"][:10]
        filename = u"%s/#%s-%s-%s.md" % (label_folder,number,created_at,title,)
        content = issue[u"body"]
        
        print filename
        cout = open(filename,"w")
        cout.write(content.encode("utf-8"))
        cout.close()
    

if __name__ == "__main__":
    sys.exit(dumpIssues())

