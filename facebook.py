# EAAGd8B5AmvwBAFSpwS72ccj9RewdZBqWLYbRRKGCr9h2EIyjt63TcO2C2ePO9dY5YOHqc4LvbaZAQkmlfj9qiXSw1lE02SAvdTNVtvMiORx2lJ1g8RfBfVAK7OijBfFzIBUeUy7tUQfmlYWaBEptbtgdP9s9HfpCC4pNL97MEMrtjY3R5Eabb2nPMeJZB2fLVLweRpeJAZDZD

import urllib.request
import re
from bs4 import BeautifulSoup
import requests

import csv
import sys

from pytrends.request import TrendReq

import pandas as pd
import datetime

import random

import time

now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d")

posts = open('facebook_output.csv', mode='w', errors='ignore')
post_writer = csv.writer(posts, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
post_writer.writerow(['Title','Content'])

links_file = open('links.txt','r',encoding='utf-8')
names_file = open('names.txt','r',encoding='utf-8')

links = []
names = []

def maxminposition(A):
   minposition = A.index(min(A))
   maxposition = A.index(max(A))
   return(maxposition,minposition)

for line in links_file:
    links.append(line.replace('\n',''))
    
for line in names_file:
    names.append(line.replace('\n',''))

count = 0
    
for i in range(len(links)):

    try:
    
        #print('trying ' + links[i] + '...')
        profile_id = links[i].split('/')[-2]
        
        link = links[i][0:len(links[i])-1] # get rid of final /
        temp = requests.get(link + '?locale=en_US')
        bs = BeautifulSoup(temp.text,'lxml').decode('utf-8', 'ignore')

        likes = re.findall(r'\n (.*?) people like this',str(bs))
        file = open('test.txt','w',encoding='utf-8')
        file.write(str(bs))
        
        # get image
        try:
            img_link = re.findall(r'<meta content="(.*?)" property="og:image"\/>',str(bs))[0]
            img_code = '<p><img class="alignleft" src="{}" />'.format(img_link)
        except:
            # user doesn't have a profile image somehow, use generic image
            img_code = '<p><img class="alignleft" src="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcScfearQ7GAPvnLZD_dFzdetQppDK1vUf-HyVp6FfU_QlO25eCJ" height="200px" width="200px"/>'
        
        try:
            likes = likes[0].replace(' ','')

            followers_fb = re.findall(r'\n (.*?) people follow this',str(bs))
            followers_fb = followers_fb[0].replace(' ','')

            page_created = re.findall(r'Page created - (.*?)\n',str(bs))[0]
            
            content_facebook = 'As of {}, {} has {} likes on their facebook page, {} followers and has been '.format(today, names[i], likes, followers_fb) + ' posting on the page since {}. '.format(page_created)
            
            posts_link = 'https://www.facebook.com/pg/{}/posts?locale=en_US'.format(profile_id)
            #print(posts_link)
            temp = requests.get(posts_link)
            
            # output the html to a txt file if desired
            bs = BeautifulSoup(temp.text,'lxml').decode('utf-8', 'ignore')
            file = open('test1.txt','w',encoding='utf-8')
            file.write(str(bs))
            
            share_counts = list(map(int, re.findall(r'"share_count":{"count":(.*?)}',str(bs))))[0:19]
            reaction_counts = list(map(int, re.findall(r'"reaction_count":{"count":(.*?)}',str(bs))))[0:19]
            comment_counts = list(map(int, re.findall(r'"comment_count":{"total_count":(.*?)}',str(bs))))[0:19]
            
            like_counts,love_counts,wow_counts,haha_counts,angry_counts,sad_counts = [],[],[],[],[],[]
            
            #reactions = re.findall(r'{"edges":\[{"i18n_reaction_count":"(.*?)}\]}',str(bs))[0:19]
            reactions = re.findall(r'{"edges":\[{"reaction_count":(.*?)}\]}',str(bs))[0:19]
            print(reactions)
            #print(len(reactions))
            for set in reactions:
                try:
                    like_counts.append(int(re.findall(r'"key":1},"reaction_count":(.*?)}',set)[0]))
                except:
                    like_counts.append(0)
                try:
                    love_counts.append(int(re.findall(r'"key":2},"reaction_count":(.*?)}',set)[0]))
                except:
                    love_counts.append(0)
                try:
                    wow_counts.append(int(re.findall(r'"key":3},"reaction_count":(.*?)}',set)[0]))
                except:
                    wow_counts.append(0)
                try:
                    haha_counts.append(int(re.findall(r'"key":4},"reaction_count":(.*?)}',set)[0]))
                except:
                    haha_counts.append(0)
                try:
                    angry_counts.append(int(re.findall(r'"key":8},"reaction_count":(.*?)}',set)[0]))
                except:
                    angry_counts.append(0)
                try:
                    sad_counts.append(int(re.findall(r'"key":7},"reaction_count":(.*?)}',set)[0]))
                except:
                    sad_counts.append(0)
            
            story_ids = list(map(int, re.findall(r'"subscription_target_id":"([0-9]+)","owning_profile',str(bs))))
            
            msi = maxminposition(share_counts)[0] # most shared index
            lsi = maxminposition(share_counts)[1] # least shared index
            
            print(like_counts)
            #print(names[i],profile_id,story_ids[msi],story_ids[msi],'{:,}'.format(share_counts[msi]),'{:,}'.format(reaction_counts[msi]),'{:,}'.format(like_counts[msi]),'{:,}'.format(love_counts[msi]),'{:,}'.format(wow_counts[msi]),'{:,}'.format(comment_counts[msi]))
            
            print(names[i],profile_id,story_ids[msi],story_ids[msi],'{:,}'.format(share_counts[msi]),'{:,}'.format(reaction_counts[msi]))
            
            posts_content = content_facebook + 'We analyzed the couple-dozen latest posts from {}. First, check out the most shared post (ID <a href="https://www.facebook.com/{}/posts/{}" target="_blank">{}</a>) with {} shares, {} reactions (including {} likes, {} \'loves\' and {} \'wow\'s) and {} comments:</p>'.format(names[i],profile_id,story_ids[msi],story_ids[msi],'{:,}'.format(share_counts[msi]),'{:,}'.format(reaction_counts[msi]),'{:,}'.format(like_counts[msi]),'{:,}'.format(love_counts[msi]),'{:,}'.format(wow_counts[msi]),'{:,}'.format(comment_counts[msi]))
            
            posts_content = posts_content + '<center><iframe src="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2F{}%2Fposts%2F{}&width=500" width="100%" height="350" style="border:none;overflow:hidden" scrolling="yes" frameborder="0" allowTransparency="true" allow="encrypted-media"></iframe></center>'.format(profile_id,story_ids[msi])
            
            mai = maxminposition(angry_counts)[0] # most angry index
            
            if angry_counts[mai] > 2:
            
                angry_comment = '<p>There are {} likes here. '.format('{:,}'.format(like_counts[msi]))
            
                if mai == msi: # most liked post also has most angry reactions
                    angry_comment = angry_comment + 'However, this same post also has <b>{} angry reactions</b>.'.format('{:,}'.format(angry_counts[mai]))
                else:
                    most_angry_story_id = story_ids[mai]
                    angry_comment = angry_comment + 'There is another post from {} (ID <a href="https://www.facebook.com/{}/posts/{}" target="_blank">{}</a>, with {} angry reactions:</p>'.format(names[i],profile_id,most_angry_story_id,most_angry_story_id,'{:,}'.format(angry_counts[mai])) + '<center><iframe src="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2F{}%2Fposts%2F{}&width=500" width="100%" height="350" style="border:none;overflow:hidden" scrolling="yes" frameborder="0" allowTransparency="true" allow="encrypted-media"></iframe></center><p>'.format(profile_id,most_angry_story_id)
            
                posts_content = posts_content + angry_comment
            
            if lsi is not mai: # least shared index is not most angry index
                least_popular = 'The least popular post is ID <a href="https://www.facebook.com/{}/posts/{}" target="_blank">{}</a>):</p>'.format(profile_id,story_ids[lsi],story_ids[lsi]) + '<center><iframe src="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2F{}%2Fposts%2F{}&width=500" width="100%" height="350" scrolling="yes"></iframe></center>'.format(profile_id,story_ids[lsi])
                try:
                    if share_counts[lsi] is 0:
                        least_popular = least_popular + '<p>This post has zero shares, {} comments and {} total reactions, with {} likes, {} loves, {} wow reactions, {} haha reactions, {} angry reactions and {} sad reactions.</p>'.format('{:,}'.format(share_counts[lsi]),'{:,}'.format(comment_counts[lsi]),'{:,}'.format(reaction_counts[lsi]),'{:,}'.format(like_counts[lsi]),'{:,}'.format(love_counts[lsi]),'{:,}'.format(wow_counts[lsi]),'{:,}'.format(haha_counts[lsi]),'{:,}'.format(angry_counts[lsi]),'{:,}'.format(sad_counts[lsi]))
                    else:
                        least_popular = least_popular + '<p>This post has just {} shares, {} comments and {} total reactions, with {} likes, {} loves, {} wow reactions, {} haha reactions, {} angry reactions and {} sad reactions.</p>'.format('{:,}'.format(share_counts[lsi]),'{:,}'.format(comment_counts[lsi]),'{:,}'.format(reaction_counts[lsi]),'{:,}'.format(like_counts[lsi]),'{:,}'.format(love_counts[lsi]),'{:,}'.format(wow_counts[lsi]),'{:,}'.format(haha_counts[lsi]),'{:,}'.format(angry_counts[lsi]),'{:,}'.format(sad_counts[lsi]))
                except Exception as e:
                    print(str(e))
                    print(share_counts[lsi])
                    print(comment_counts[lsi])
                    print(reaction_counts[lsi])
                    print(like_counts[lsi])
                    print(love_counts[lsi])
                    print(wow_counts[lsi])
                    print(haha_counts[lsi])
                    print(angry_counts[lsi])
                    print(sad_counts[lsi])
                
            else:
                if share_counts[lsi] is 0:
                    least_popular = 'This angry post is also the least shared, with zero shares, {} comments and {} total reactions, with {} likes, {} loves, {} wow reactions, {} haha reactions, {} angry reactions and {} sad reactions.</p>'.format('{:,}'.format(share_counts[lsi]),'{:,}'.format(comment_counts[lsi]),'{:,}'.format(reaction_counts[lsi]),'{:,}'.format(like_counts[lsi]),'{:,}'.format(love_counts[lsi]),'{:,}'.format(wow_counts[lsi]),'{:,}'.format(haha_counts[lsi]),'{:,}'.format(angry_counts[lsi]),'{:,}'.format(sad_counts[lsi]))
                else:
                    least_popular = 'This angry post is also the least shared, with just {} shares, {} comments and {} total reactions, with {} likes, {} loves, {} wow reactions, {} haha reactions, {} angry reactions and {} sad reactions.</p>'.format('{:,}'.format(share_counts[lsi]),'{:,}'.format(comment_counts[lsi]),'{:,}'.format(reaction_counts[lsi]),'{:,}'.format(like_counts[lsi]),'{:,}'.format(love_counts[lsi]),'{:,}'.format(wow_counts[lsi]),'{:,}'.format(haha_counts[lsi]),'{:,}'.format(angry_counts[lsi]),'{:,}'.format(sad_counts[lsi]))
            
            posts_content = posts_content + least_popular
                        
            print(posts_content)
            
            posts_content = posts_content.replace(' 0 ',' zero ')
            
            posts_content = img_code + posts_content
            
            post_writer.writerow([names[i],posts_content])
            
            print('done for',links[i])
            
            #break
            
            count += 1
            if count > 20:
                break
            
        except Exception as e:
            print(str(e), 'on line', sys.exc_info()[-1].tb_lineno, 'for',links[i])
            continue

    except Exception as e:
        print(str(e))
        print('failed for ' + names[i])
