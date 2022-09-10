from finalscrapper import app, csvcreate
from flask import request, render_template, send_file
from finalscrapper.db2 import db, YtScrape, comments
from finalscrapper.scrapper import Scrape
from finalscrapper.getsite import getYoutubeSite
from finalscrapper.csvcreate import csvWriter


@app.route('/', methods = ["GET", "POST"])
def table1():
    if request.method == "POST":
        
        if request.form["no_of_videos"] == '' or request.form["channel_link"]=='' :
            return render_template ('index.html')
        
        if "https://www.youtube.com/c/" not in request.form["channel_link"] and "https://www.youtube.com/user/" not in request.form["channel_link"] :
             return render_template ('index.html')
        
        channel = request.form["channel_link"]
        no_of_videos=int(request.form["no_of_videos"])

        

        db.session.query(YtScrape).delete()
        db.session.commit()
        db.session.query(comments).delete()
        db.session.commit()

        urls = getYoutubeSite(channel, no_of_videos)
        try: 
            Scrape(urls)
        except:
            return render_template('index.html')

        
        data = [[u.id, u.video_url, u.thumbnail_urls,u.title,u.likes,u.no_of_comments,u.views,u.download_link] for u in YtScrape.query.all()]                                     #--4
        csvWriter(data)

        return render_template('details.html', data = data)
    else:
        return render_template('index.html')

@app.route('/details', methods = ["GET"])
def details_page():
    return render_template('details.html')

@app.route('/comment', methods = ["GET"])
def comment_page():
    unique_titles =[each.title for each in YtScrape.query.distinct(YtScrape.title)]
    full = [[u.title, u.commentators, u.comments] for u in comments.query.all()] #gives list of LIST of all the records

    return render_template('comment.html',full=full, unique_titles=unique_titles)



@app.route('/downloads', methods = ["GET"])
def download_csv():
    return send_file("temp\\yt.csv",
                        mimetype='text/csv',
                        download_name = 'YTdetails.csv',
                        as_attachment=True )



