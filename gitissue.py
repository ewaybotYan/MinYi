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

__author__ = "Leslie Zhu (pythonisland@gmail.com)"
__version__ = "1.0.0"

def gitIssues(state="open", repo=u"MinYi", user=u"LeslieZhu"):
    """
    根据GitHub用户名、项目名、Issue状态条件，批量备份Issues.
    """
    
    if state != "":
        content = urllib2.urlopen(u"https://api.github.com/repos/%s/%s/issues?state=%s" % (user,repo,state,))
    else:
        content = urllib2.urlopen(u"https://api.github.com/repos/%s/%s/issues" % (user,repo,))
        
    issues = json.loads(content.read())
    
    for issue in issues:
        dumpIssues(issue)
        
        if issue.has_key(u"milestone"):
            dumpMilestones(issue[u"milestone"])

def dumpIssues(issue):
    """
    issue是一个字典，如:

    {
      "number": 2,
      "title": "",
      "labels": [
            {
               "name": "iOS",
            }
       ],
      "state": "open",
      "milestone": {
                   },
      "comments": 0,
      "created_at": "2015-07-22T13:47:32Z",
      "updated_at": "2015-11-30T09:33:16Z",
      "closed_at": null,
      "body": ""
    },
    """
    
    title = issue[u"title"]
    number = issue[u"number"]
    
    label = issue[u"labels"][0][u"name"]
    label_folder = u"issues/%s" % (label,)
    created_at = issue[u"created_at"][:10]
    
    if not os.path.exists(label_folder):
        os.makedirs(label_folder)
        
    filename = u"%s/#%s-%s-%s.md" % (label_folder,number,created_at,title,) # Warn: 可能本地文件名会有点乱码，但在GitHub网站则会显示正常。
    
    # 当标题修改了，导致文件名也修改，防止一个issue保存了多个文件
    for issuefile in glob.glob(u"issues/*/#%s-*.md" % (number,)):
        if issuefile != filename:
            subprocess.Popen(["git","mv","-f",issuefile,filename])

        
    content = issue[u"body"].encode("utf-8")
    
    print filename
    cout = open(filename,"w")
    cout.write(content + '\n')
    cout.close()


def dumpMilestones(milestone):
    """
    milestone是一个字典结构，如:

    {
      "number": 1,
      "title": "before 2015",
      "description": "",
      "open_issues": 7,
      "closed_issues": 0,
      "state": "open",
      ...
    },
    """
        
    # 如果里程碑已经关闭，则默认不会更新里程碑的定义
    if milestone[u"state"] != "open": return
        
    milestone_num = milestone[u"number"]
    milestone_name = milestone[u"title"]
    milestone_file = u"milestones/#%s-%s.md" % (milestone_num,milestone_name,)
    
    # 当标题修改了，导致文件名也修改，防止一个issue保存了多个文件
    for milestonefile in glob.glob(u"milestones/#%s-*.md" % (milestone_num,)):
        if milestonefile != milestone_file:
            subprocess.Popen(["git","mv","-f",milestonefile,milestone_file])
            
    if milestone.has_key(u"description"):
        milestone_description = milestone[u"description"].encode("utf-8")
    else:
        milestone_description = u""
        
    if not os.path.exists(milestone_file) or os.stat(milestone_file).st_size != len(milestone_description + '\n'):
        print milestone_file
        cout = open(milestone_file,"w")
        cout.write(milestone_description + '\n')
        cout.close()
    

if __name__ == "__main__":
    sys.exit(gitIssues("open","MinYi","LeslieZhu"))

