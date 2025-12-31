# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 12:40:26 2022

Original author: buxared
Fork and modifications: Schoenabatic

Atom Manga Reader, also referred to as AMR, is an application designed
to read manga on Kobo eReaders.

Copyright (C) 2022 buxared
Copyright (C) 2025 Schoenabatic

This file is part of Atom Manga Reader.

Atom Manga Reader is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Atom Manga Reader is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import flask
import requests
from PIL import Image
import io
import os
import csv
import shutil
import time

app=flask.Flask(__name__)

search_results={}
manga_data={}
user_selections={'manga':1000000, 'chapter':1000000} #Global choice tracker
pg_links={}
reader_src={}
lib_selection={}

@app.route("/")
def home():
    return flask.render_template('home.html')

@app.route("/search", methods=["POST","GET"])
def GetRes():
    search_results.clear()
    return flask.render_template('searchpage.html')

@app.route("/results/<srch>", methods=["POST","GET"])
def ShowRes(srch):
    user_selections['manga']=1000000 #reset global tracking
    search_string=flask.request.form["srchstr"]
    usable_search_string = search_string.replace("'","").lower() # removes apostrophes
            
    #title search:
    manga_results_html = requests.post(
    "https://weebcentral.com/search/simple",
    data={
        "text": usable_search_string,
        "location": "main"
    },
    headers={
        "User-Agent": "Mozilla/5.0",
        "HX-Request": "true"
    }
).text
    
    # print(manga_results_html)
    
    
    # #find actual titles from data (with author last chapter and update date and link)
    # ! schoenabtic: found title, url and img for now will find author later
    
    manga_list_html = manga_results_html.split('<div class="w-full join join-vertical flex absolute inset-x-0 z-50 mt-4 rounded-none" x-show="showResult">')[1].split('</div>\n</section>')[0]

    manga_chunks = manga_list_html.split('<a href="')

    for i, manga in enumerate(manga_chunks[1:], start=1): 
        manga_title = ''
        manga_url = ''
        manga_img = ''

        for line in manga.split('\n'):
            stripped_line = line.strip()

            if stripped_line and '<' not in stripped_line and '>' not in stripped_line:
                manga_title = stripped_line

            if 'class="btn' in stripped_line:
                manga_url = stripped_line.split('" class')[0]

            if 'source' in stripped_line:
                manga_img = stripped_line.split('"')[1]
                
            search_results[str(i+1)] = {             
                    'url': manga_url,
                    'title': manga_title,
                    'img': manga_img,
                    'author': "Lorem Ipsum",
                    'last_ch': "1"
                }
    
    
    return flask.render_template('searchres.html', n_manga=len(manga_chunks), res=search_results)   

@app.route("/manga_result/choice/<usr_choice>")
def GetMangaData(usr_choice):
    headers={
        "User-Agent": "Mozilla/5.0",
        "HX-Request": "true"
    }

    manga_selected=usr_choice
    user_selections['manga']=usr_choice #global tracking
    user_selections['chapter']=1000000 # to ensure that when a new manga is selected, but same chapter is selected, GetChap gets us the right info
    
    manga_data['url']=search_results[str(manga_selected)]['url']
    manga_data['title']=search_results[str(manga_selected)]['title']
    manga_data['img']=search_results[str(manga_selected)]['img']
    
    manga_page_url = 'https://cubari.moe/read/weebcentral/'+ manga_data['url'].split('/')[4] + '/'
    
    
    manga_page_html = requests.get(manga_page_url, headers=headers).text
    
    # ! schoenbatic: get manga title and chapter url
    
    chapters_html = manga_page_html.split('<tbody id="chapterTable">')[1].split('</tbody>')[0]

    chapters_list = chapters_html.split('</tr>')
    
    manga_data['ch_list']={}

    for chapter in chapters_list:
        ch_title = ''
        ch_link = ''
        
        if '<a' not in chapter or 'href="' not in chapter:
            continue
        
        ch_title = chapter.split('<a')[1].split('</a>')[0].split('>')[1].strip()
        ch_link = chapter.split('href="')[1].split('"')[0]
        
        ch_num = str(ch_title.strip().split(' ')[1])
        manga_data['ch_list'][ch_num]={'ch_link': ch_link,
                                       'ch_title': ch_title,
                                       'ch_update': 'N/A',
                                       'ch_url': '/manga_reader/ch/' + ch_num + '/p1'}
        
     
    return flask.render_template('mangapage.html', n_ch=len( manga_data['ch_list']), manga_data=manga_data)

@app.route("/manga_reader/ch/<ch_no>/p<p_no>")
def GetChap(ch_no,p_no):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://cubari.moe/",
    "Origin": "https://cubari.moe"
    
}
    # normalise types
    ch_no = int(ch_no)
    p_no = int(p_no)
        
    chapter_selected=ch_no
    user_selections['chapter']=ch_no #update for global tracking
    
    
    
    
    #! schoenbatic: open series data from the api which has the endpoints for all the chapters images
    series_api_url = 'https://cubari.moe/read/api/weebcentral/series/' + manga_data['ch_list'][str(chapter_selected)]['ch_link'].strip('/').split('/')[2] + '/'
    series_data = requests.get(series_api_url, headers={'User-agent': 'Mozilla/5.0'}).json()
    
    # print(series_data)
    # ! schoenabtic: get chapter images
    chapter_api_url = 'https://cubari.moe' + series_data['chapters'][str(chapter_selected)]['groups']['1']
    chapter_data = requests.get(chapter_api_url, headers=headers).text
    
    print(chapter_data)

    reader_src = chapter_data.strip()[1:-1].split('", "')
    reader_src = [url.strip('"') for url in reader_src]  
    
    next_ch_link = (
    f'/manga_reader/ch/{ch_no + 1}/p1'
    if str(ch_no + 1) in series_data['chapters']
    else None
)
    prev_ch_link = (
    f'/manga_reader/ch/{ch_no - 1}/p1'
    if ch_no > 1
    else f'/manga_reader/ch/{ch_no}/p1'   
)
    
    # ! schoenabatic: get last page of previous chapter
    
    if ch_no > 1 and str(ch_no - 1) in series_data['chapters']:
        prev_ch_api_url = "https://cubari.moe" + series_data['chapters'][str(ch_no - 1)]['groups']['1']
        prev_ch_data = requests.get(prev_ch_api_url, headers=headers).text

        prev_reader_src = prev_ch_data.strip()[1:-1].split('", "')
        prev_reader_src = [url.strip('"') for url in prev_reader_src]

        prev_ch_last_page = len(prev_reader_src)
    else:
        prev_ch_last_page = None
    
    return flask.render_template(
        "mangareader3.html",
        manga_title=manga_data.get("title", "Atom Manga Reader"),
        ch_no=ch_no,
        p_no=p_no,
        pg_last=len(reader_src),
        reader_src=reader_src,
        next_ch_link=next_ch_link,
        prev_ch_last_page=prev_ch_last_page,
        manga_home_link="#"
    )
        
        #look for <div class="container-chapter-reader">
    #     pg_data=chapter_data.split('<div class="container-chapter-reader">')[1].split('\n')[1].split('<img src')
    #     pg_links.clear()
        
    #     n_pg=len(pg_data)-1
    #     for i in range(n_pg):
    #         each_pg_link=pg_data[i+1].split('"')[1]
    #         pg_links[str(i+1)]=each_pg_link
        
    #     #Now, download all chapter pages and store in app 'chapter_cache' folder
        
    #     host_link=pg_links['1'].split('/')[2]
    #     referer_link=manga_data['ch_list'][str(chapter_selected)]['ch_link']

    #     s = requests.Session()

    #     headers = {
    #                 "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)", 
    #                 "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/jpg,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    #                 "accept-encoding" : "gzip, deflate, br", 
    #                 "accept-language" : "en-GB,en;q=0.9,en-US;q=0.8,de;q=0.7", 
    #                 "cache-control"   : "no-cache", 
    #                 "pragma" : "no-cache", 
    #                 "upgrade-insecure-requests" : "1" ,
    #                 "Host": host_link,#example: 'bu3.mkklcdnv6tempv3.com',#
    #                 "referer": referer_link
    #                 }
    #     s.headers = headers
        
    #     #here, try to get one image, if works, proceed, except (else) follow link to other server button, reconstruct session by changing host_link
    #     try:
    #         page_response=s.get(pg_links['1'], verify=True)
    #         img = Image.open(io.BytesIO(page_response.content))
    #     except:
    #         server_num=['','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','mn']
    #         for hostname in [host_link.split('.')[1], 'mncdnbuv1']:
    #             for num in server_num:
    #                 host_link='bu'+num+'.'+hostname+'.'+host_link.split('.')[2]
    #                 pg_links['1']='https://'+host_link+'/'+'/'.join(pg_links['1'].split('/')[3:])
    #                 headers = {
    #                             "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)", 
    #                             "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/jpg,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    #                             "accept-encoding" : "gzip, deflate, br", 
    #                             "accept-language" : "en-GB,en;q=0.9,en-US;q=0.8,de;q=0.7", 
    #                             "cache-control"   : "no-cache", 
    #                             "pragma" : "no-cache", 
    #                             "upgrade-insecure-requests" : "1" ,
    #                             "Host": host_link,
    #                             "referer": referer_link
    #                             }
    #                 s.headers = headers#redefined since host_link got updated
                    
    #                 try:
    #                     page_response=s.get(pg_links['1'], verify=True)
    #                     img = Image.open(io.BytesIO(page_response.content))
    #                     break
    #                 except:
    #                     pass
                
    #     #fix pg_links
    #     for pg_no in pg_links:
    #         pg_links[pg_no]='https://'+host_link+'/'+'/'.join(pg_links[pg_no].split('/')[3:])
            
    #     reader_src.clear()
        
    #     for pg_no in pg_links:
    #         page_response=s.get(pg_links[pg_no], verify=True)
    #         try:
    #             img = Image.open(io.BytesIO(page_response.content))
    #         except:
    #             img=Image.open('static/images/pgunavail.jpg', mode='r') 
            
    #         if img.mode != 'RGB':
    #             img = img.convert('RGB')
    #         img.save('static/chapter_cache/'+str(chapter_selected)+'-'+"{:03d}".format(int(pg_no))+'.jpg')
    #         # generate link to page for reader webpage
    #         reader_src[pg_no]='chapter_cache/'+str(chapter_selected)+'-'+"{:03d}".format(int(pg_no))+'.jpg'

        
    # #link for manga title page
    # manga_home_link='/manga_result/choice/'+user_selections['manga']
    
    # #we need key of next chap and previous chap
    # ch_all=list(manga_data['ch_list'].keys()) #list of keys
    # this_ch_index=ch_all.index(ch_no)         #index of this chapter in list
    
    # #construct links for next and previous chapter
    # if this_ch_index > 0: #this is not the first in the list [most recent release]
    #     next_ch_key=ch_all[this_ch_index-1]       #key of next chapter is this_ch_index - 1, since descending order
    #     next_ch_link='/manga_reader/ch/'+next_ch_key+'/p1'
    # else:
    #     next_ch_link=manga_home_link
        
    # if this_ch_index < len(ch_all)-1: #final index of the list [first or oldest chapter]
    #     prev_ch_key=ch_all[this_ch_index+1]       #similar for previous chapter
    #     prev_ch_link='/manga_reader/ch/'+prev_ch_key+'/p1'
    # else:
    #     prev_ch_link=manga_home_link
    
    # while True: #keep looping unless returning is possible
    #     try:
    #         return flask.render_template('mangareader3.html', ch_no=ch_no, p_no=int(p_no), pg_last=len(reader_src), pg_src=reader_src[str(p_no)], next_ch_link=next_ch_link, prev_ch_link=prev_ch_link, manga_home_link=manga_home_link)
    #     except:
    #         #wait if not done downloading all images
    #         time.sleep(3)

@app.route("/add2fav")
def FavAdd():    
    m_title=search_results[user_selections['manga']]['title']
    m_url=search_results[user_selections['manga']]['url']
    m_img=search_results[user_selections['manga']].get('img', '')

    #write data required to simulate search results
    #step 1:check if entry already exists
    counter=0
    with open('static/mangafavs.csv', 'r', newline='') as csv_file:
        reader=csv.reader(csv_file)
        for line in reader:
            if line and m_title == line[0]:
                counter=counter+1
    csv_file.close()
    #step 2: write entry if it doesn't exists
    with open('static/mangafavs.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)  # Note: writes lists, not dicts.
        if counter==0:#write only if entry does not exist already
            writer.writerow([m_title, m_url, m_img])
    csv_file.close()
        
    manga_home_link='/manga_result/choice/'+user_selections['manga']
    
    return flask.render_template('favadded.html', favtitle=m_title, manga_home_link=manga_home_link)

@app.route("/favorites")
def FavDisp():
    #reset user_selections
    user_selections['manga']=1000000
    user_selections['chapter']=1000000
    search_results.clear()
    
    #read data from mangafavs.csv to dictionary
    with open('static/mangafavs.csv', 'r', newline='') as csv_file:
        reader=csv.reader(csv_file)
        
        num=0
        for row in reader:
            if not row: continue
            num += 1
            title = row[0]
            url = row[1]
            img = row[2] if len(row) > 2 else ''
            
            search_results[str(num)] = {
                'title': title,
                'url': url,
                'img': img
            }
    csv_file.close()

    n_manga=len(search_results)
    #This page should be similar to searchres
    return flask.render_template('favoriteshome.html', n_manga=n_manga, res=search_results)

@app.route("/removeFavConfirm/<fav_num>")
def FavDel(fav_num):
    #delete entry from dictionary
    removed_title=search_results[fav_num]['title']
    
    rows = []
    #read data from mangafavs.csv
    with open('static/mangafavs.csv', 'r', newline='') as csv_file:
        reader=csv.reader(csv_file)
        for row in reader:
            if row and row[0] != removed_title:
                rows.append(row)
    csv_file.close()
    
    #rewrite updated list to mangafavs.csv
    with open('static/mangafavs.csv', 'w', newline='') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerows(rows)
    csv_file.close()
    #provide button to go back to favoriteshome page
    return flask.render_template('favremoval.html', removed_title=removed_title)

@app.route("/add2lib")
def LibUpdate():   
    #get usable manga and chapter title
    manga_title=manga_data['title'].strip()
    chapter_title=manga_data['ch_list'][user_selections['chapter']]['ch_title'].strip()
    
    bad_char=['.', ' ', '"', '?', '>', '<', '/' , '|', '\\', '*', ':', '\\0']
    for c in bad_char:
        if c in manga_title:
            manga_title=manga_title.replace(c, '_')
            
    for c in bad_char:
        if c in chapter_title:
            chapter_title=chapter_title.replace(c, '_')
            
    #Add (prefix) chapter number tag for sorting
    chapter_title='[c'+ str(float(user_selections['chapter'])).zfill(6) + ']' + chapter_title
    
    #if this manga title is not already in the library, create directory
    mangadir = 'static/library/'+manga_title
    if not os.path.exists(mangadir):
        os.makedirs(mangadir)
    
    #now that manga title is created or already exists, if this chapter title is not already under the manga title, create directory
    chapdir='static/library/'+manga_title+'/'+chapter_title

    if os.path.exists(chapdir):
        manga_home_link='/manga_result/choice/'+user_selections['manga']
        return flask.render_template('libadded.html', t=manga_data['title'], c=manga_data['ch_list'][user_selections['chapter']]['ch_title'], manga_home_link=manga_home_link)

    else: #if it does not exist, meaning that chapter is new; create dir
        os.makedirs(chapdir)
        #now that the chapter folder is created, copy chapter pages from chapter cache
        shutil.copytree('static/chapter_cache', chapdir, dirs_exist_ok=True)
        manga_home_link='/manga_result/choice/'+user_selections['manga']
        return flask.render_template('libadded.html', t=manga_data['title'], c=manga_data['ch_list'][user_selections['chapter']]['ch_title'], manga_home_link=manga_home_link)
    
    
@app.route("/library")
def LibDisp():
    #find all manga titles in library
    title_list=os.listdir('static/library/')
    
    #display titles in a table in libraryhome
    n_titles=len(title_list)
    
    return flask.render_template('libraryhome.html', n_titles=n_titles, title_list=title_list)

@app.route("/library/<title>")
def LibDispL2(title):
    #This is library level 2
    #Here we want to see chapters listed under the manga title
    mangapath='static/library/'+title+'/'
    chapter_list=os.listdir(mangapath)
    
    n_ch=len(chapter_list)
    
    #create lib_selection dictionary for creating links easily
    lib_selection['title']=title
    lib_selection['ch_list']=chapter_list
    lib_selection['ch_sel']=1000000 #"chapter selcted" initialized
    lib_selection['pg_links']=[] #empty list
    
    #display chapter titles in a table    
    return flask.render_template('librarymanga.html', m_title=title, n_ch=n_ch, chapter_list=chapter_list)

@app.route("/libChapRemoval/<title>/<ch_title>")
def LibChDel(title, ch_title):
    chapterpath='static/library/' + title + '/' + ch_title
    shutil.rmtree(chapterpath)
    return flask.render_template('libchremoval.html', removed_title=title, removed_ch=ch_title)

@app.route("/libTitleRemoval/<title>")
def LibTitleDel(title):
    mangapath='static/library/' + title
    shutil.rmtree(mangapath)
    return flask.render_template('libtitleremoval.html', removed_title=title)

@app.route("/offline_reader/ch/<ch_num>/p<p_num>")
def OpenOfflineReader(ch_num, p_num):
    if lib_selection['ch_sel']!=ch_num:
        lib_selection['ch_sel']=ch_num #set new selection
        
        #get pages in chapter
        ch_path='static/library/'+lib_selection['title']+'/'+lib_selection['ch_list'][int(ch_num)-1]+'/'
        lib_selection['pg_links']=[f for f in os.listdir(ch_path) if os.path.isfile(os.path.join(ch_path, f))]
    
    #create links    
    manga_home_link='/library/'+lib_selection['title']
    
    if int(ch_num)<len(lib_selection['ch_list']):
        next_ch_link='/offline_reader/ch/'+str(int(ch_num)+1)+'/p1'
    else:
        next_ch_link=manga_home_link
        
    
    if int(ch_num)>1:
        prev_ch_link='/offline_reader/ch'+str(int(ch_num)-1)+'/p1'
    else:
        prev_ch_link=manga_home_link
    
    while True: #keep looping unless pg_src is filled
        try:
            pg_src='library/'+lib_selection['title']+'/'+lib_selection['ch_list'][int(ch_num)-1]+'/'+lib_selection['pg_links'][int(p_num)-1]
            break
        except:
            #wait if not done loading pg_src
            time.sleep(2)
    
    return flask.render_template('offlinemangareader3.html', ch_no=ch_num, p_no=int(p_num), pg_last=len(lib_selection['pg_links']), pg_src=pg_src, next_ch_link=next_ch_link, prev_ch_link=prev_ch_link, manga_home_link=manga_home_link)
        
    

@app.route("/nav")
def navigationpage():
    return flask.render_template('navigation.html')

@app.route("/about")
def aboutpage():
    return flask.render_template('about.html')
    
@app.route("/shutdown", methods=["POST","GET"])
def shutdown():
    if flask.request.method=="POST":  
        #clear old files from cache
        dir2clear = 'static/chapter_cache'
        for f in os.listdir(dir2clear): 
            os.remove(os.path.join(dir2clear, f))
            
        try:
            os.remove('static/manga_cover/manga_cover.jpg')
        except:
            pass
            
        # return ip to what it was
        os.system('ip addr del 127.0.0.1/8 dev lo')
        os.system('ip addr del 127.0.0.42/32 dev lo')
        
        # shutdown_server()
        os.system('pkill -15 -f "AMR"')
        return flask.render_template('shutdown.html')
    else:
        return flask.render_template('shutdown.html')
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234, debug=True)
    
    

# if __name__=="__main__":
#     app.run(host='127.0.0.42', port=1234) #Alternative code to run; Must change last line in AMRrun.sh to: "/mnt/onboard/.AMR/amrpyenv/bin/python3 AMRmain.py
#     app.run(host='0.0.0.0', port= 1234) #For desktop only, do not run on Kobo

