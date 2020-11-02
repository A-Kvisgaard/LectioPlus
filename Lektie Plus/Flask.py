# encoding: utf-8
import sys
from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import date, timedelta, datetime

path_to_folder = sys.path[0]
path_too_phantomjs = path_to_folder + "\\webdriver\\bin\\phantomjs.exe"
# Modificerer user-agent
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
                                             "(KHTML, like Gecko) Chrome/15.0.87")

app = Flask(__name__)  # Opretter server instans
app.debug = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 10

driver = url = usn = psw = school_number = error = ''  # Opretter globale variabler


def login(url, usn, psw):
    status = error = ''
    try:
        # Går ind på login siden på lectio
        driver.get(url)
        # Udfylder login oplysningerne
        user_input = driver.find_element_by_id('m_Content_username2')  # Finder brugernavn input
        user_input.clear()
        user_input.send_keys(usn)
        psw_input = driver.find_element_by_id('password2')  # finder kodeord input
        psw_input.clear()
        psw_input.send_keys(psw)
        driver.find_element_by_id('m_Content_submitbtn2').click()  # Finder og klikker på login knappen
    except:  # Hvis den ikke kan komme ind på login siden
        driver.quit()
        return False, 'Du har ikke adgang til Lectio'
    try:  # Går ind på forsiden af lectio
        assert 'forside' in driver.current_url
        status = True
    except:  # Hvis den ikke kan komme ind på forsiden, er det fordi den fejlede i at logge ind, og den får brugeren til at prøve igen.
        error = 'Brugernavnet og/eller adgangskoden er forkert!'
        Status = False
        driver.quit()
    finally:
        return status, error


def get_assignments():
    # Får opgaverne fra lectio
    cell_number = 1
    assignments_list = []
    assignment_compose = []
    append = False
    driver.find_element_by_link_text('Opgaver').click()  # Går til siden med opgaver
    cells = driver.find_elements_by_tag_name('td')  # Finder alle celler
    for cell in cells:
        # Hvis cellen indeholder den ønskede info, bliver den lagt i listen
        if cell_number == 2 or cell_number == 3 or cell_number == 9:
            assignment_compose.append(cell.text)
        elif cell_number == 4:
            # Splitter datoen i dag, måned, år, tidspunkt og finder en dato for hvornår opgaven skal laves.
            decoded = cell.text.decode('utf-8')  # Omskriver unicode til utf-8
            split_slah = decoded.split('/')
            split_dash = split_slah[1].split('-')
            assignment_compose.append(split_slah[0])  # Får dag
            assignment_compose.append(split_dash[0])  # Får måned
            assignment_compose.append(split_dash[1].split(' ')[0])  # Får år
            assignment_compose.append(split_dash[1].split(' ')[1])  # Får tidspunkt
        elif cell_number == 5:
            _date = date(int(assignment_compose[-2]), int(assignment_compose[-3]), int(assignment_compose[-4]))
            elevtid = int(cell.text.decode('utf-8').split(',')[0])
            dodate = str(_date - timedelta(days=elevtid))
            assignment_compose.append(cell.text)  # Elevtid
            assignment_compose.append(dodate.split('-')[0])  # Do year
            assignment_compose.append(dodate.split('-')[1])  # Do month
            assignment_compose.append(dodate.split('-')[2])  # Do day
        elif cell_number == 6:
            # Tjekker om opgave ikke er afleveret endnu
            if cell.text == 'Venter' or cell.text == 'Mangler':
                assignment_compose.append(cell.text)
                append = True
        if cell_number == 11:  # Sidste celle for opgaven
            if append:  # Opgaven er ikke afleveret
                assignments_list.append(assignment_compose)
            cell_number = 1
            append = False
            assignment_compose = []
        else:  # Ikke sidste celle
            cell_number += 1
    return assignments_list


def get_home_work():
    # Får lektierne fra lectio
    cell_number = number_of_loops = 1
    home_work_compose = []
    home_work_list = []
    driver.find_element_by_link_text('Lektier').click()
    cells = driver.find_elements_by_tag_name('td')
    for cell in cells:
        if cell_number == 1:  # Hvis cellen indeholder en dato
            #   Deler datoen i måned og dag og opretter en "do date", altså dagen den skal lave.
            decoded = cell.text.decode('utf-8')
            split_slash = decoded.split('/')
            split_space = split_slash[0].split(' ')
            day = int(split_space[1])
            month = int(split_slash[1])
            if day - 2 < 1 and month != 3:  #
                doMonth = month - 1
                doDay = 30
            elif day - 2 < 1 and month == 3:
                doMonth = month - 1
                doDay = 28
            else:
                doDay = day - 2
                doMonth = month
            home_work_compose.append(day)  # Dag
            home_work_compose.append(month)  # Måned
            home_work_compose.append(doDay)  # Do day
            home_work_compose.append(doMonth)  # Do month
        else:  # Cellen indeholder Modul, note eller lektie
            home_work_compose.append(cell.text)
        if cell_number == 4:  # Sidste celle
            home_work_list.append(home_work_compose)  # tilføjer den endelige liste til lektie listen
            home_work_compose = []
            cell_number = 1
        else:  # Ikke sidste celle
            cell_number += 1
    return home_work_list


def add_to_database(assignment_list, home_work_list):
    try:
        db = sqlite3.connect('./data.db')  # Forbinder til databasen
        db.row_factory = sqlite3.Row
        db.execute('Drop Table If Exists Assignments;')
        db.execute('Drop Table If Exists Homework;')
        # Opretter "assignments" tabel
        db.execute(
            'Create Table If Not Exists Assignments (Fag string, Opgavetitel string, Day real, Month real, Year real, '
            'Time string, Elevtid string, DoYear string, DoMonth string, DoDay string, Status string, Opgavenote string );')
        # Indsætter værdierne, hvis der er opgaver for
        if len(assignment_list) > 0:
            for assignment in assignment_list:
                db.execute('Insert Into Assignments Values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', assignment)
        # Opret "homework" tabel
        db.execute('CREATE table If Not Exists Homework (Day real, Month real, DoDay real, DoMonth real, '
                   'Module string, Note string, Task string);')
        # Indsætter værdierne, hvis der er lektier for
        if len(home_work_list) > 0:
            for work in home_work_list:
                print work
                db.execute('Insert Into homework Values (?, ?, ?, ?, ?, ?, ?);', work)
        db.commit()  # Gem ændringer
    except:
        pass
    finally:
        pass


def connect_db():
    rv = sqlite3.connect('./data.db')
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.route('/')
def do_index():
    global error
    if error != '':
        error_display = error
        error = ''
        return render_template('Login.html', error=error_display)
    else:
        return render_template('Login.html')


@app.route('/submit', methods=['POST'])
def do_submit():
    # Udtrækker data fra brugeren og opretter et webdriver instans
    global school_number, url, usn, psw, driver, status, error
    school_number = request.form['school']
    usn = request.form['usn']
    psw = request.form['psw']
    url = "https://www.lectio.dk/lectio/" + school_number + "/login.aspx"
    driver = webdriver.PhantomJS(executable_path=path_too_phantomjs, desired_capabilities=dcap)
    status, error = login(url, usn, psw)
    if status:
        return render_template('wait.html')
    else:
        return redirect(url_for('do_index'))


@app.route('/precalender')
def do_precalendar():
    # De næste to linjer dur kun, hvis man har logget ind på startsiden med et elev uni-login. Hvis man har et elevlogin
    # skal man bare fjerne hashtagget og logge ind fra startsiden (127.0.0.1:5000/)

    # add_to_database(get_assignments(), get_home_work()) # Sætter opgaverne og lektierne ind i databasen
    # driver.quit()
    return render_template('precalendar.html')


@app.route('/calender', methods=['GET'])
def do_calendar():
    db = get_db()
    day = request.args.get('day')  # Udtrækker 'day' parameteret fra URL'en og retunerer det som en string
    month = request.args.get('month')  # Udtrækker 'month' parameteret fra URL'en og retunerer det som en string
    year = request.args.get('year')  # Udtrækker 'year' parameteret fra URL'en og retunerer det som en string
    if request.method == 'GET':  # Hvis der bliver sendt en 'GET' request, bliver følgende kode kørt:
        has_homework = {}
        for i in db.execute('SELECT DoDay FROM Assignments WHERE DoMonth=' + str(int(month) + 1) + ' AND DoYear=' + str(
                year) + ';').fetchall():  # Går igennem databsen og finder alle dage i måneden man er på, hvor der er opgaver for
            has_homework[str(i['DoDay'])] = True  # Sætter dagene ind i en dictionary som keys, med 'True' som value
        for i in db.execute('SELECT DoDay FROM Homework WHERE DoMonth=' + str(float(int(
                month) + 1)) + ';').fetchall():  # Går igennem databsen og finder alle dage i måneden man er på, hvor der er opgaver forhas_homework[str(int(i['Day']))] = True  # Sætter dagene ind i en dictionary som keys, med 'True' som value.
            has_homework[str(int(i['DoDay']))] = True
        assignments = []
        homework_table = []
        for assignment in db.execute('SELECT * FROM Assignments WHERE DoDay=' + str(int(day)) + ' AND DoMonth=' + str(
                int(month) + 1) + ' AND DoYear=' + str(int(
            year)) + ';').fetchall():  # Går igennem databasen og hiver alt data ud for den dag man befinder sig på.
            date = str(int(assignment['Day'])) + '/' + str(int(assignment['Month'])) + '/' + str(
                int(assignment['Year'])) + ' kl. ' + str(assignment[
                                                             'Time'])  # Da dag, måned, år og klokkeslet er i hver sin kolonne, bliver de her sat sammen til én string.
            assignments.append({
                "fagO": assignment['Fag'],
                "dateO": date,
                "elevtid": assignment['Elevtid'],
                "titel": assignment['Opgavetitel'],
                "beskrivelseO": assignment['Opgavenote']
            })
        for homework in db.execute('SELECT * FROM Homework WHERE DoDay=' + str(float(int(day))) + ' AND DoMonth=' + str(
                float(int(month) + 1)) + ';').fetchall():
            date = str(int(homework['Day'])) + '/' + str(int(homework['Month']))
            string = homework['Module']
            string = string.split('-')
            modul = string[0]
            fag = string[1]
            homework_table.append({
                "fag": fag,
                "date": date,
                "modul": modul,
                "note": homework['Note'],
                "beskrivelse": homework['Task']
            })
        return render_template('calender.html', has_homework=has_homework, assignments=assignments,
                               homework_table=homework_table)  # Renderer templaten med de informationer den har fået ud af databsen


@app.route('/schoolnumber')
def do_schoolnumber():
    return render_template('schoolnumber.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


# Starter serveren
if __name__ == '__main__':
    app.run()
