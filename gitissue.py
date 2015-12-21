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
        content = urllib2.urlopen(u"https://api.github.com/repos/%s/%s/issues?state=all" % (user,repo,))
        
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


    author = "[%s](%s) on %s:\n\n" % (issue[u"user"][u"login"],issue[u"user"][u"html_url"],created_at,)
    content = issue[u"body"].encode("utf-8")

    if issue.has_key(u"comments_url"):
        commit_doc = dumpCommits(issue[u"comments_url"]).encode("utf-8")
    else:
        commit_doc = u""
    
    print filename
    cout = open(filename,"w")
    cout.write(author + '\n')
    cout.write(content + '\n')
    if commit_doc != "": cout.write(commit_doc + '\n')        
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

def dumpCommits(commits_url):
    """
    {
    "user": {
      "login": "acoada",
    },
    "created_at": "2015-12-10T02:59:32Z",
    "body": ""
    }
    """
    commits_doc = u"\n\n# 评论\n\n"

    
    content = urllib2.urlopen(commits_url)
    commits = json.loads(content.read())

    if not commits: return u""

    for commit in commits:
        commits_doc += "\n[%s](%s) on %s:\n\n %s \n" % (commit[u"user"][u"login"],commit[u"user"][u"html_url"], commit["created_at"], commit["body"],)

    return commits_doc

def analyse():
    """ Analyse all issues and generate a SUMMARY.md file"""
    
    issues_data = dict()
    label_data = dict()
    
    for issue in glob.glob("issues/*/*.md"):
        issuedir,label,issuename = issue.strip().split('/')

        issuename = issuename.split('-')
        issueNum,created_at,issueTitle = issuename[0],issuename[1:4],'-'.join(issuename[4:])

        year,month,day = created_at

        if label not in label_data:
            label_data[label] = 1
        else:
            label_data[label] += 1
            
        if not issues_data.has_key(year): issues_data[year] = {}
        if not issues_data[year].has_key(month): issues_data[year][month] = []
        issues_data[year][month].append([issueNum,label,issueTitle])

    return summary(label_data,issues_data)

def summary(label_data,issues_data):
    
    _header = "# 敏毅\n\n"
    _info   = "『士不可以不弘毅，任重而道远！』\n\n"
    _label_header = "# 标签\n\n"
    _table_header = "编号 | 标签 | 文章\n-----|------|----\n"
    _copyright = "# 版权说明\n\n未经允许，禁止转载！\n\n"
    
    with open("README.md","w") as cout:
        cout.write(_header)
        cout.write(_info)

        cout.write(_label_header)
        cout.write("- [All (%s篇)](https://github.com/LeslieZhu/MinYi/labels)\n" % (sum(label_data[x] for x in label_data),))
        for label in sorted(label_data):
            cout.write("- [%s (%s篇)](https://github.com/LeslieZhu/MinYi/labels/%s)\n" % (label,label_data[label],label,))
        cout.write('\n')

        for year in sorted(issues_data.keys(),reverse=True):
            cout.write("# %s年 (%s篇)\n\n" % (year,sum(label_data[x] for x in label_data),))
            for month in sorted(issues_data[year].keys(),reverse=True):
                cout.write("## %s年%s月 (%s篇)\n\n" % (year,month,len(issues_data[year][month]),))
                cout.write(_table_header)
                for issue in sorted(issues_data[year][month],key=lambda x: int(x[0][1:]),reverse=True):
                    issue_num,issue_label,issue_title = issue
                    
                    issue_num_url = "[%s](https://github.com/LeslieZhu/MinYi/issues/%s)" % (issue_num,issue_num[1:],)
                    issue_label_url = "[%s](https://github.com/LeslieZhu/MinYi/labels/%s)" % (issue_label,issue_label,)
                    issue_title_url = "[%s](https://github.com/LeslieZhu/MinYi/issues/%s)" % (issue_title.replace(".md",""),issue_num[1:],)
                    
                    cout.write('|'.join([issue_num_url,issue_label_url,issue_title_url]) + '\n')
                cout.write("\n")
            cout.write('\n')
        cout.write('\n')

        cout.write(_copyright)
        cout.write('\n')
                
        

                                    
        
def main(args):
    basedir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(basedir)
    if "update" in args:
        gitIssues("open","MinYi","LeslieZhu")
        analyse()
    elif "analyse" in args:
        analyse()
    else:
        print "Usage: %s [options]" % args[0]
        print
        print "Options:"
        print "\tupdate\t\tupdate new issues"
        print "\tanalyse\t\tanalyse the blog based on issues, generate SUMMARY.md"
        return -1
        
if __name__ == "__main__":
    sys.exit(main(sys.argv))

