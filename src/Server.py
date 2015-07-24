# This file is part of ASTRID.
#
# ASTRID is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ASTRID is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ASTRID.  If not, see <http://www.gnu.org/licenses/>.

import ASTRID
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename
import koremutake as km
import threading
import json
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER']='/tmp/'

syllables = "BA BE BI BO BU BY DA DE DI DO DU DY FA FE FI FO FU FY GA GE GI GO GU GY HA HE HI HO HU HY JA JE JI JO JU JY KA KE KI KO KU KY LA LE LI LO LU LY MA ME MI MO MU MY NA NE NI NO NU NY PA PE PI PO PU PY RA RE RI RO RU RY SA SE SI SO SU SY TA TE TI TO TU TY VA VE VI VO VU VY BRA BRE BRI BRO BRU BRY DRA DRE DRI DRO DRU DRY FRA FRE FRI FRO FRU FRY GRA GRE GRI GRO GRU GRY PRA PRE PRI PRO PRU PRY STA STE STI STO STU STY TRA TRE".split() # from http://shorl.com/koremutake.php

def random_jobid():
    jobid = ""
    while jobid in jobdict:
        jobid = km.encode(random.randint(0, 128**3))
    return jobid

@app.route("/")
def index():
    return render_template('ASTRID.html')

@app.route("/start", methods=['POST'])
def startjob():
    job = ASTRID.ASTRID(request.files['genetrees'].read())
    if 'jobid' in request.form and len(request.form['jobid']):
        jobid = request.form['jobid']
    else:
        jobid = random_jobid()
    thread = threading.Thread(target = job.run, args=(request.form['method'],))
    print jobid
    thread.start()
    jobdict[jobid] = ("started", job, thread, request)
    print jobdict
    return jobid

@app.route("/status")
def checkstatus():
    print request.args
    if 'jobid' not in request.args:
        return json.dumps({'error':"No jobid in request"})
    jobid = request.args['jobid']
    print jobdict
    if jobid not in jobdict:
        return json.dumps({'error':"jobid " + jobid + " not found"})
    status = jobdict[jobid]
    if status[0] == "done":
        return json.dumps({'status':'done', 'tree':status[1]})
    
    job = status[1]
    js = job.state
    if js == "Done":
        jobdict[jobid] = ("done", job.tree_str())
        return json.dumps({'status':'done', 'tree':job.tree_str()})
    
    return json.dumps({'status':js,
                       'pct':job.pct})
    

if __name__ == "__main__":
    jobdict = {"":()}
    app.debug = True
    app.run()
