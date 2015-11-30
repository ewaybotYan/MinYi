#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
gitissue.py  --- 基于GitHub Issues功能博客的备份工具

使用GitHub的API，比如:

$ curl  https://api.github.com/repos/LeslieZhu/MinYi/issues

以JSON格式获取项目的issue状态，进而对issue做其它操作。
'''

import sys,os,time
import urllib2
import json
import glob,subprocess


def dumpIssues(state="open", repo=u"MinYi", user=u"LeslieZhu"):
    """
    根据GitHub用户名、项目名、Issue状态条件，批量备份Issues.
    """
    
    if state != "":
        content = urllib2.urlopen(u"https://api.github.com/repos/%s/%s/issues?state=%s" % (user,repo,state,))
    else:
        content = urllib2.urlopen(u"https://api.github.com/repos/%s/%s/issues" % (user,repo,))
        
    issues = json.loads(content.read())
    
    for issue in issues:
        # [u'body', u'labels', u'locked', u'title', u'url', u'labels_url', u'created_at', u'events_url', \
        #    u'comments_url', u'html_url', u'comments', u'number', u'updated_at', u'assignee', u'state', \
        #    u'user', u'milestone', u'closed_at', u'id']

        title = issue[u"title"]
        number = issue[u"number"]
        
        label = issue[u"labels"][0][u"name"]
        label_folder = u"issues/%s" % (label,)
        
        if not os.path.exists(label_folder):
            os.makedirs(label_folder)

        created_at = issue[u"created_at"][:10]
        filename = u"%s/#%s-%s-%s.md" % (label_folder,number,created_at,title,) # Warn: 可能本地文件名会有点乱码，但在GitHub网站则会显示正常。

        # 当标题修改了，导致文件名也修改，防止一个issue保存了多个文件
        for issuefile in glob.glob(u"issues/*/#%s-*.md" % (number,)):
            if issuefile != filename:
                subprocess.Popen(["git","mv","-f",issuefile,filename])

        
        content = issue[u"body"]
        
        print filename
        cout = open(filename,"w")
        cout.write(content.encode("utf-8") + '\n')
        cout.close()


        milestone = issue[u"milestone"]
        milestone_num = milestone[u"number"]
        milestone_name = milestone[u"title"]
        
        if milestone.has_key(u"description"):
            milestone_description = milestone[u"description"]
        else:
            milestone_description = u""

        milestone_file = u"milestones/#%s-%s.md" % (milestone_num,milestone_name,)
        if not os.path.exists(milestone_file) or (time.time() - os.stat(milestone_file).st_ctime) > 120:
            print milestone_file
            cout = open(milestone_file,"w")
            cout.write(milestone_description.encode("utf-8") + '\n')
            cout.close()
    

if __name__ == "__main__":
    sys.exit(dumpIssues("open","MinYi","LeslieZhu"))

