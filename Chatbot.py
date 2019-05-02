#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import os, sys
import requests
import json
from datetime import datetime
import random


# 框架指定了 http 的通信协议, 用户可以通过 http post 的方式进行请求，示例如下：
# curl -d request_data http://ip:port/anyq，其中request_data是把输入接口序列化为字符串，参考如下：
# curl -d '{"log_id": "7758521", "version": "00003333", "request": {"query_info": {"type": "TEXT"}, "query": "今天天气怎么样"}, "bot_id": "5",
# "bot_session":""}' 10.14.25.15:8991/anyq

# In[2]:


def authentication():
    auth_url = "https://aip.baidubce.com/oauth/2.0/token"
    grant_type = "client_credentials"
    client_id = "Oe66NgcGLgaNGtsG53ypODYf"
    client_secret = "Eh8WSVNuUzqG1HmKDsAGFk9LMpZ2AR9C"
    
    payload = {'grant_type': grant_type, 'client_id': client_id, 'client_secret': client_secret}
    
    r = requests.post(auth_url, data=payload)
    
    return r


def get_session_id(uid):
    filename = 'session_ids/' + uid
    if(os.path.exists(filename)):
        f = open(filename, 'r')
        result = f.read()
        f.close()
        return result

    return ""




def update_session_id(uid, new_session_id):
    filename = 'session_ids/' + uid

    f = open(filename, 'w')
    f.write(new_session_id)
    f.close()


# In[3]:


def chatbot_test(access_token, session_string, query):

    version = "2.0"
    service_id = "S16521"
    log_id = "1437114514"
    skill_ids = ["50202","51064"]
    
    user_id = "1000000001"

    bot_session = ""
    url = "https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=" + access_token
    
    
    
    payload  = {
        "log_id": "7758521",
        "service_id": service_id,
        "skill_ids": skill_ids,
        "session_id": session_string,
        "request": {
            "bernard_level": 0,
            "query": query,
            "query_info": {
                "asr_candidates": [],
                "source": "KEYBOARD",
                "type": "TEXT"
            },
            "updates": "",
            "user_id": "88888"
        },
        
        "dialog_state": {
            "contexts":{
                "SYS_REMEMBERED_SKILLS": ["50202"]
            }
        },
        "version": version
    }
    
    json_payload = json.dumps(payload).encode("UTF-8")
    headers = {'Content-Type': 'application/json'}
    
    
    res = requests.post(url, data=json_payload, headers=headers)
    
    return res;


# In[4]:


def rounder(t):
    return t.replace(second=0, microsecond=0, minute=0, hour=t.hour+1)


# In[5]:


def movie_finder(datetime_obj):
    date_filename = "movie_avaliable/date_availble.csv"
    time_filename = "movie_avaliable/time_availble.csv"
    theatre_filename = "movie_avaliable/theatre_availble.csv"
    
    f_date = open(date_filename,"r",encoding='utf-8')
    f_time = open(time_filename, "r",encoding='utf-8')
    f_theatre = open(theatre_filename, "r",encoding='utf-8')
    
    date_str = f_date.read()
    time_str = f_time.read()
    theatre_str = f_theatre.read()
    
    f_date.close()
    f_time.close()
    f_theatre.close()
    
    date_arr = date_str.split(",")
    time_arr = time_str.split()
    theatre_arr = theatre_str.split(",")
    
    res = []
    date_obj = datetime_obj.date()
    time_obj = datetime_obj.time()
    
    for date in date_arr:
       # print(date, str(date_obj))
        if(date == str(date_obj)):
            for time in time_arr:
                dt_string = str(date) + " " + str(time)
                cur_dt_obj = datetime.strptime(dt_string, "%Y-%m-%d %H:%M")
                time_differ = (abs(cur_dt_obj - datetime_obj)).total_seconds()
                theatre_str = random.choice(theatre_arr)
                
                res.append( (date, time, theatre_str, time_differ))
    
    if(len(res) == 0):
        return []
    
    result = sorted(res,key=lambda x:(x[3]) )
    
    if(result[0][3] < 1):
        return [result[0]]
    
    if(len(res) < 3):
        return result
    
    return result[:3]


# In[9]:


def ticket_query(dt=datetime.now(), movie="复仇者联盟4", city="Hong Kong", person=1, isconfirm=False):
    
    
    res = "\n"
    res += 'Your movie: ' +  movie + '\n'
    
    dt_string = str(dt)
    is_exist_time = ":" in dt_string
    is_exist_date = "-" in dt_string
    
    date_time = ""
    
    res += 'Date & Time: '
    
    padding = ""
    
    if is_exist_time and is_exist_date:
        if "|" in dt_string:
            dt_obj = datetime.strptime(dt_string, "%Y-%m-%d|%H:%M:%S")
            padding += str(dt_obj.date()) + " " + dt_obj.strftime("%H:%M")
            
        
        else:
            dt_obj = dt
            padding += str(dt_obj.date()) + " " + dt_obj.strftime("%H:%M")
        
    else:
        dt_new_string = ""
        if not is_exist_date:
            
            dt_whole_string = ""
            dt_whole_string += str(datetime.today().date()) + " " + dt_string
            
            # a.strptime("2019-01-05 11:13:01","%Y-%m-%d %H:%M:%S") 
            dt_obj = datetime.strptime(dt_whole_string, "%Y-%m-%d %H:%M:%S")
            
            dt_new_string = dt_obj.strftime("%Y-%m-%d %H:%M")
            
            
        
        else:
            default_time =  rounder(datetime.now())
            dt_new_string += dt_string + " " + default_time.strftime("%H:%M")
            
            dt_obj = datetime.strptime(dt_new_string, "%Y-%m-%d %H:%M")
            
        padding += dt_new_string
    
    res += padding + "\n\n"
        
    if(isconfirm):

        movies = movie_finder(dt_obj)


        #res += padding + "\n\n"

        if(len(movies) > 0):
            res += "We find the following movie(s): \n\n"
            counter = 1
            for movie in movies:
                res += "Date: " + str(movie[0]) + "\n"
                res += "Time: " + str(movie[1]) + "\n"
                res += "Theatre: " + str(movie[2]) + "\n"
                res += "\n"


    res += 'City: ' + city + '\n'
    res += 'No. of person: ' + str(int(float(str(person)))) + '\n'
    
    return res
    


def chatbot_reply(access_token, session_id, query):

    response = json.loads(chatbot_test(access_token, session_id, query).text)

    #print(counter, response)
    
    #print(response)
    
    

    result = response['result']
    slots = result['response_list'][0]['schema']['slots']
    action_id = result['response_list'][0]['action_list'][0]['action_id']
    reply = result['response_list'][0]['action_list'][0]['say']
    
  #  print(result['response_list'][0]['action_list'][0])
    status = result['response_list'][0]['action_list'][0]['type']
    
    #print(action_id)
    
    
    
    if action_id == "movie_ticket_user_confirm_clarify":
        query_dict = dict()
        for unit in slots:
            name = unit['name']
            words = unit['normalized_word']
            if name == 'user_city':
                query_dict['city'] = words
            elif name == 'user_movie_name':
                query_dict['movie'] = words
            elif name == 'user_num':
                query_dict['num'] = words
            elif name == 'user_time':
                query_dict['date_time'] = words
        reply += ticket_query(query_dict['date_time'], query_dict['movie'], query_dict['city'], query_dict['num'], False)
        
        
        
        
   
    if status == 'satisfy' and session_id != "" and action_id != "faq_found_satisfy":
        query_dict = dict()
        for unit in slots:
            name = unit['name']
            words = unit['normalized_word']
            if name == 'user_city':
                query_dict['city'] = words
            elif name == 'user_movie_name':
                query_dict['movie'] = words
            elif name == 'user_num':
                query_dict['num'] = words
            elif name == 'user_time':
                query_dict['date_time'] = words
        reply += ticket_query(query_dict['date_time'], query_dict['movie'], query_dict['city'], query_dict['num'], True)
        
        
    new_session = "" if status == 'satisfy' else result['session_id']

    return new_session, reply

