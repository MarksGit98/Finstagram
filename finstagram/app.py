from flask import Flask, render_template, request, session, redirect, url_for, send_file
import os
import uuid
import hashlib
import pymysql.cursors
from functools import wraps
import time

app = Flask(__name__)
app.secret_key = "super secret key"
IMAGES_DIR = os.path.join(os.getcwd(), "images")
connection = pymysql.connect(host="localhost",
                             user="root",
                             password="Typeoff16",
                             db="Finstagram",
                             charset="utf8mb4",
                             port=8889,
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True)


def login_required(f):
    @wraps(f)
    def dec(*args, **kwargs):
        if not "username" in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return dec


@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("home"))
    return render_template("index.html")


@app.route("/home")
@login_required
def home():
    requestQuery = f"""SELECT username_follower FROM Follow WHERE username_followed = 
    '{session["username"]}' AND followstatus = 0"""
    with connection.cursor() as cursor:
        cursor.execute(requestQuery)
        requestData = cursor.fetchall()
    return render_template("home.html", username=session["username"], followSuccess = 0, requests = requestData, requestsUpdated=0)


@app.route("/upload", methods=["GET"])
@login_required
def upload():
    belongToQuery = f"""SELECT DISTINCT groupName, owner_username FROM BelongTo WHERE member_username = '{session["username"]}' OR owner_username = '{session["username"]}'"""
    with connection.cursor() as cursor:
        cursor.execute(belongToQuery)
        groupData = cursor.fetchall()
    return render_template("upload.html", groups = groupData)


# PART 3.1b FOR PROJECT
@app.route("/images", methods=["GET"])
@login_required
def images():
    print(session["username"])
    photoQuery = f"""SELECT DISTINCT *
            FROM Photo AS P JOIN Follow AS F ON
            P.photoPoster = F.username_followed LEFT JOIN SharedWith AS S
            ON S.photoID = P.photoID LEFT JOIN BelongTo AS B ON S.groupName = B.groupName 
            AND S.groupOwner = B.owner_username
            WHERE (F.username_follower = '{session["username"]}' AND F.followstatus = 1 AND
            P.allFollowers = 1)
            UNION SELECT DISTINCT *
            FROM Photo AS P JOIN SharedWith AS S ON
            P.photoID = S.photoID JOIN BelongTo AS B
            ON B.groupName = S.groupName AND B.owner_username = S.groupOwner 
            LEFT JOIN Follow AS F ON P.photoPoster = F.username_followed
            WHERE B.member_username = '{session["username"]}'
            ORDER BY postingdate"""
    personQuery = f"""SELECT * FROM Person"""
    tagQuery = f"""SELECT * FROM Tagged WHERE tagstatus = 1"""
    likeQuery = f"""SELECT username, photoID, rating FROM Likes"""
    with connection.cursor() as cursor:
        cursor.execute(photoQuery)
        image_data = cursor.fetchall()
        try:
            image_data.reverse()
        except:
            print("No results")
        #print(image_data)
        cursor.execute(personQuery)
        person_data = cursor.fetchall()
        #print(person_data)
        cursor.execute(tagQuery)
        tag_data = cursor.fetchall()
        #print(tag_data)
        cursor.execute(likeQuery)
        like_data = cursor.fetchall()
        #print(like_data)
    return render_template("images.html", images=image_data, persons=person_data, tags=tag_data, likes=like_data)


@app.route("/image/<image_name>", methods=["GET"])
def image(image_name):
    image_location = os.path.join(IMAGES_DIR, image_name)
    if os.path.isfile(image_location):
        return send_file(image_location, mimetype="image/jpg")


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")


@app.route("/loginAuth", methods=["POST"])
def loginAuth():
    if request.form:
        requestData = request.form
        username = requestData["username"]
        plaintextPassword = requestData["password"]
        hashedPassword = hashlib.sha256(plaintextPassword.encode("utf-8")).hexdigest()

        with connection.cursor() as cursor:
            query = "SELECT * FROM Person WHERE username = %s AND password = %s"
            cursor.execute(query, (username, plaintextPassword))
        data = cursor.fetchone()
        if data:
            session["username"] = username
            return redirect(url_for("home"))

        error = "Incorrect username or password."
        return render_template("login.html", error=error)

    error = "An unknown error has occurred. Please try again."
    return render_template("login.html", error=error)


@app.route("/registerAuth", methods=["POST"])
def registerAuth():
    if request.form:
        requestData = request.form
        username = requestData["username"]
        plaintextPassword = requestData["password"]
        hashedPassword = hashlib.sha256(plaintextPassword.encode("utf-8")).hexdigest()
        print(username, hashedPassword)
        firstName = requestData["fname"]
        print(firstName)
        lastName = requestData["lname"]

        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO Person (username, password, firstName, lastName) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (username, plaintextPassword, firstName, lastName))
        except pymysql.err.IntegrityError:
            error = "%s is already taken." % (username)
            return render_template('register.html', error=error)

        return redirect(url_for("login"))

    error = "An error has occurred. Please try again."
    return render_template("register.html", error=error)


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username")
    return redirect("/")


@app.route("/uploadImage", methods=["POST"])
@login_required
def uploadImage():
    belongToQuery = f"""SELECT DISTINCT groupName, owner_username FROM BelongTo WHERE member_username = '{session["username"]}' OR owner_username = '{session["username"]}'"""
    with connection.cursor() as cursor:
        cursor.execute(belongToQuery)
        groupData = cursor.fetchall()
    if request.form:
        startPoint = 3
        addPhotoList = []
        requestData = request.form
        print(requestData)
        image_name = requestData["imageToUpload"]
        caption = requestData["caption"]
        try:
            allFollowers = requestData["allFollowers"]
        except:
            allFollowers = "False"
            startPoint-=1
        for data in requestData:
            addPhotoList.append(data)
        addPhotoList = addPhotoList[startPoint:]
        print(addPhotoList)
        filepath = os.path.join(IMAGES_DIR, image_name)
        if allFollowers == "True":
            allFollowers = 1
        else:
            allFollowers = 0
        if caption == '':
            caption = None
        query = "SELECT MAX(photoID) AS currID FROM Photo"
        with connection.cursor() as cursor:
            cursor.execute(query)
        currID = int(cursor.fetchall()[0]['currID'])
        uploadQuery = "INSERT INTO Photo (photoID, postingdate, filePath, allFollowers, caption, photoPoster) VALUES (%s, %s, %s, %s, %s, %s)"
        sharedWithQuery ="INSERT INTO SharedWith (groupOwner, groupName, photoID) VALUES (%s, %s, %s)"
        try:
            with connection.cursor() as cursor:
                cursor.execute(uploadQuery, (currID+1, time.strftime('%Y-%m-%d %H:%M:%S'), filepath, allFollowers, caption, session["username"]))
                try:
                    for group in addPhotoList:
                        cursor.execute(sharedWithQuery, (group.split(' | ')[1], group.split(' | ')[0], currID+1))
                    message = "Image has been successfully uploaded."
                except:
                    message = "Image has been successfully uploaded but failed to add to a certain group(s)"
        except:
            message = "Failed to upload image."
        return render_template("upload.html", message=message, groups = groupData)
    else:
        message = "Failed to upload image."
        return render_template("upload.html", message=message, groups = groupData)

@app.route("/followUser", methods=["POST"])
@login_required
def followUser():
    requestQuery = f"""SELECT username_follower FROM Follow WHERE username_followed = 
    '{session["username"]}' AND followstatus = 0"""
    with connection.cursor() as cursor:
        cursor.execute(requestQuery)
        requestData = cursor.fetchall()
    followSuccess = 0
    if request.form:
        requestData = request.form
        followedUsername = requestData["username"]
        followQuery = "INSERT INTO Follow (username_followed, username_follower, followstatus) VALUES (%s, %s, %s)"
        try:
            with connection.cursor() as cursor:
                cursor.execute(followQuery, (followedUsername, session["username"], 0))
                followSuccess = 1
        except:
            followSuccess = 2
    return render_template("home.html", username=session["username"], followSuccess = followSuccess, requestUser = followedUsername, requests=requestData, requestsUpdated = 0)

@app.route("/followAccept", methods=["POST"])
@login_required
def followAccept():
    if request.form:
        requestData = request.form
        for name in requestData:
            addQuery = f"""UPDATE FOLLOW SET followstatus=1 WHERE username_followed='{session["username"]}'
                        AND username_follower = '{name}'"""
            with connection.cursor() as cursor:
                cursor.execute(addQuery)

        removeQuery = f"""DELETE FROM Follow WHERE username_followed='{session["username"]}' AND followstatus = 0"""
        with connection.cursor() as cursor:
            cursor.execute(removeQuery)

    return redirect(url_for("home"))
if __name__ == "__main__":
    if not os.path.isdir("images"):
        os.mkdir(IMAGES_DIR)
    app.run()
