import datetime
import logging
import sqlite3
import sys

# Command-line parameters.
FAKE = True
assert len(sys.argv) >= 3, 'Usage: migrater.py /path/to/src.db /path/to/dst.db [fake]'
src_path = sys.argv[1]
dst_path = sys.argv[2]
if (len(sys.argv) >= 4) and (sys.argv[3] == 'real'):
    FAKE = False

#------------------------------------------------------------
# Utilities.
#------------------------------------------------------------

def fail(table, fields, exc):
    '''Report failure.'''
    logging.error("Failing on {table} with {fields} because {error}".format(
            table=table, fields=fields, error=e))
    sys.exit(1)


def info(table):
    '''Report successful migration of given table, and commit.'''
    logging.info("Successfully migrated '{table}' table".format(table=table))


def fake(i, slug, personal, middle, family, email, gender, github, twitter, url):
    '''Redact personal identifying information.'''
    if not FAKE:
        return slug, personal, middle, family, email, gender, github, twitter, url
    where = 'I{0}.edu'.format(i)
    return 'S{0}'.format(i), \
           'F{0}'.format(i), \
           'M{0}'.format(i), \
           'L{0}'.format(i), \
           '{0}@{1}'.format(i, where), \
           ('M', 'F', 'O')[i % 3], \
           'U_{0}'.format(i), \
           '@U{0}'.format(i), \
           'http://{0}/U_{1}'.format(where, i)

def select_one(cursor, query, default='NO DEFAULT'):
    cursor.execute(query)
    result = cursor.fetchall()
    if result and (len(result) == 1):
        return result[0][0]
    if default != 'NO DEFAULT':
        return default
    assert False, 'select_one could not find exactly one record for "{0}"'.format(query)

def select_least(cursor, query):
    cursor.execute(query)
    results = cursor.fetchall()
    if not results:
        return None
    results.sort()
    return results[0][1]

#------------------------------------------------------------
# Setup.
#------------------------------------------------------------

assert len(sys.argv) == 3, 'Usage: migrater.py /path/to/src.db /path/to/dst.db'

old_cnx = sqlite3.connect(sys.argv[1])
old_crs = old_cnx.cursor()
new_cnx = sqlite3.connect(dst_path)
new_crs = new_cnx.cursor()

#------------------------------------------------------------
# Sites.
#------------------------------------------------------------

# Site
new_crs.execute('delete from workshops_site;')
old_crs.execute('select site, fullname, country from site;')
site_lookup = {}
i = 1
for (site, fullname, country) in old_crs.fetchall():
    site_lookup[site] = i
    try:
        fields = (i, site, fullname, country, '')
        new_crs.execute('insert into workshops_site values(?, ?, ?, ?, ?);', fields)
    except Exception, e:
        fail('site', fields, e)
    i += 1

info('site')

#------------------------------------------------------------
# Airports.
#------------------------------------------------------------

# Airport
new_crs.execute('delete from workshops_airport;')
old_crs.execute('select fullname, country, latitude, longitude, iata from airport;')
airport_lookup = {}
i = 1
for (fullname, country, lat, long, iata) in old_crs.fetchall():
    airport_lookup[iata] = i
    try:
        fields = (i, fullname, country, lat, long, iata)
        new_crs.execute('insert into workshops_airport values(?, ?, ?, ?, ?, ?);', fields)
    except Exception, e:
        fail('airport', fields, e)
    i += 1

info('airport')

#------------------------------------------------------------
# Persons.
#------------------------------------------------------------

# load Facts for lookup in Person
old_crs.execute('select person, gender, active, airport, github, twitter, site from facts;')
facts_lookup = {}
for record in old_crs.fetchall():
    person = record[0]
    facts_lookup[person] = record[1:]

# Person
new_crs.execute('delete from workshops_person;')
old_crs.execute('select person, personal, middle, family, email from person;')
person_lookup = {}
i = 1
for (person, personal, middle, family, email) in old_crs.fetchall():
    person_lookup[person] = i
    if person in facts_lookup:
        gender, active, airport, github, twitter, url = facts_lookup[person]
    else:
        gender, active, airport, github, twitter, url = None, None, None, None, None, None

    person, personal, middle, family, email, gender, github, twitter, url = \
        fake(i, person, personal, middle, family, email, gender, github, twitter, url)
    if airport is not None:
        airport = airport_lookup[airport]

    try:
        fields = (i, personal, middle, family, email, airport, gender, github, twitter, url, person, active)
        new_crs.execute('insert into workshops_person values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', fields)
    except Exception, e:
        fail('person', fields, e)
    i += 1

info('person')

#------------------------------------------------------------
# Tags for events.
#------------------------------------------------------------

tag_lookup = {}
tag_id = 1
for (name, details) in (('SWC', 'Software Carpentry Workshop'),
                        ('DC', 'Data Carpentry Workshop'),
                        ('LC', 'Library Carpentry Workshop'),
                        ('WiSE', 'Women in Science and Engineering'),
                        ('TTT', 'Train the Trainers')):
    new_crs.execute('insert into workshops_tag values(?, ?, ?);', (tag_id, name, details))
    tag_lookup[name] = tag_id
    tag_id += 1

info('tags')

#------------------------------------------------------------
# Events.
#------------------------------------------------------------

# Event
new_crs.execute('delete from workshops_event;')
old_crs.execute('select startdate, enddate, event, site, kind, eventbrite, attendance, url from event;')
event_lookup = {}
event_id = 1
event_tag_id = 1
for (startdate, enddate, event, site, kind, eventbrite, attendance, url) in old_crs.fetchall():
    event_lookup[event] = event_id
    try:
        fields = (event_id, startdate, enddate, event, eventbrite, attendance, site_lookup[site], url, None, 0.0, '', True)
        new_crs.execute('insert into workshops_event values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', fields)
    except Exception, e:
        fail('event', fields, e)
    try:
        fields = (event_tag_id, event_id, tag_lookup[kind])
        new_crs.execute('insert into workshops_event_tags values(?, ?, ?);', fields)
    except Exception, e:
        fail('event_tag', fields, e)
    event_id += 1
    event_tag_id += 1

info('event')

# Add some unpublished events for testing purposes.
if FAKE:
    new_crs.execute('select * from workshops_event where (id>=?) and (id<?);', ((event_id-10), (event_id-5)))
    records = new_crs.fetchall()
    for r in records:
        try:
            r = list(r)
            r[0] = event_id # move on to next record
            r[1] = None # no start date
            r[2] = None # so no end date
            r[3] = None # which means no slug
            r[4] = None # no Eventbrite
            r[5] = None # and no attendance
            # r[6] # unchanged: site
            r[7] = None # no URL
            # r[8] # unchanged: organizer (which will be NULL)
            r[9] = 0.0 # admin fee
            r[10] = 'unpublished event'
            r[11] = False # not published (the whole point)
            new_crs.execute('insert into workshops_event values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', r)
        except Exception, e:
            fail('unpublished event', fields, e)
        try:
            fields = (event_tag_id, event_id, tag_lookup['SWC'])
            new_crs.execute('insert into workshops_event_tags values(?, ?, ?);', fields)
        except Exception, e:
            fail('event_tag', fields, e)
        event_id += 1
        event_tag_id += 1

    info('unpublished events')

#------------------------------------------------------------
# Tasks.
#------------------------------------------------------------

# Roles
new_crs.execute('delete from workshops_role;')
i = 1
role_lookup = {}
for role in 'helper instructor host learner organizer tutor'.split():
    role_lookup[role] = i
    try:
        fields = (i, role)
        new_crs.execute('insert into workshops_role values(?, ?);', fields)
    except Exception, e:
        fail('role', fields, e)
    i += 1

info('roles')

# Tasks
new_crs.execute('delete from workshops_task;')
old_crs.execute('select event, person, task from task;')
task_id = 1
for (event, person, task) in old_crs.fetchall():
    try:
        fields = (task_id, event_lookup[event], person_lookup[person], role_lookup[task])
        new_crs.execute('insert into workshops_task values(?, ?, ?, ?);', fields)
    except Exception, e:
        fail('task', fields, e)
    task_id += 1

info('task')

#------------------------------------------------------------
# Instructor qualifications.
#------------------------------------------------------------

# Skills
new_crs.execute('delete from workshops_skill;')
old_crs.execute('select distinct skill from skills;')
i = 1
skill_lookup = {}
for (skill,) in old_crs.fetchall():
    skill_lookup[skill] = i
    try:
        fields = (i, skill)
        new_crs.execute('insert into workshops_skill values(?, ?);', fields)
    except Exception, e:
        fail('skill', fields, e)
    i += 1

info('skill')

# Qualifications
new_crs.execute('delete from workshops_qualification;')
old_crs.execute('select person, skill from skills;')
i = 1
for (person, skill) in old_crs.fetchall():
    try:
        fields = (i, person_lookup[person], skill_lookup[skill])
        new_crs.execute('insert into workshops_qualification values(?, ?, ?);', fields)
    except Exception, e:
        fail('qualification', fields, e)
    i += 1

info('qualification')

#------------------------------------------------------------
# Instructor training (turned into events and tasks).
#------------------------------------------------------------

def mangle_name(name):
    year, month, day, tag = name.split('-')
    return '-'.join([year, month, day, 'ttt', tag])

# Turn training cohorts into events.
old_crs.execute('select startdate, cohort, active, venue from cohort;')
cohort_lookup = {}
cohort_start = {}
for (start, name, active, venue) in old_crs.fetchall():
    cohort_lookup[name] = event_id
    cohort_start[name] = start
    try:
        venue = site_lookup['online']
        end = select_one(old_crs, "select max(awards.awarded) from awards join trainee on awards.person=trainee.person where awards.badge='instructor' and trainee.cohort='{0}' and awards.person not in (select distinct awards.person from awards join trainee join cohort on awards.person=trainee.person and trainee.cohort=cohort.cohort where awards.badge='instructor' and cohort.startdate>'{1}');".format(name, start), None)
        slug = mangle_name(name)
        event_lookup[slug] = event_id
        if slug == '2014-04-14-ttt-pycon':
            end = start
        reg_key = None
        attendance = select_one(old_crs, "select count(*) from trainee where cohort='{0}';".format(name))
        url = None # FIXME
        organizer_id = site_lookup['software-carpentry.org']
        notes = ""
        published = True
        admin_fee = None
        fields = (event_id, start, end, slug, reg_key, attendance, venue, url, organizer_id, admin_fee, notes, published)
        new_crs.execute('insert into workshops_event values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', fields)
    except Exception, e:
        fail('cohort', fields, e)
    try:
        fields = (event_tag_id, event_id, tag_lookup['TTT'])
        new_crs.execute('insert into workshops_event_tags values(?, ?, ?);', fields)
    except Exception, e:
        fail('event_tag for cohort', fields, e)
    event_id += 1
    event_tag_id += 1

info('cohort')

# Turning trainees into tasks.
old_crs.execute('select person, cohort, status from trainee;')
learner = select_one(new_crs, "select id from workshops_role where name='learner';")
for (person, cohort, status) in old_crs.fetchall():
    try:
        fields = (task_id, cohort_lookup[cohort], person_lookup[person], learner)
        new_crs.execute('insert into workshops_task values(?, ?, ?, ?);', fields)
    except Exception, e:
        fail('trainee', fields, e)
    task_id += 1

info('trainee')

#------------------------------------------------------------
# Badges and awards.
#------------------------------------------------------------

def get_badge_event(cursor, person, badge, lookups):

    # Creator and member are simply awarded.
    if badge in ('creator', 'member'):
        return None

    # First event for which this person was an organizer.
    if badge == 'organizer':
        key = select_least(cursor, "select event.startdate, event.event from event join task on event.event=task.event where task.task='organizer' and task.person='{0}';".format(person))
        return lookups[badge].get(key, None)

    if badge == 'instructor':
        key = select_least(cursor, "select cohort.startdate, cohort.cohort from cohort join trainee on cohort.cohort=trainee.cohort where trainee.person='{0}';".format(person))
        return lookups[badge].get(key, None)

    assert False, 'unknown badge type "{0}"'.format(badge)

# Badges
badge_stuff = (
    ('creator',    'Creator',    'Creating learning materials and other content'),
    ('instructor', 'Instructor', 'Teaching at workshops or online'),
    ('member',     'Member',     'Software Carpentry Foundation member'),
    ('organizer',  'Organizer',  'Organizing workshops and learning groups')
)

old_crs.execute('select badge, title, criteria from badges;')
i = 1
badge_lookup = {}
for (badge, title, criteria) in badge_stuff:
    try:
        badge_lookup[badge] = i
        fields = (i, badge, title, criteria)
        new_crs.execute('insert into workshops_badge values(?, ?, ?, ?);', fields)
    except Exception, e:
        fail('badge', fields, e)
    i += 1
    
info('badge')

# Awards
new_crs.execute('delete from workshops_award;')
old_crs.execute('select person, badge, awarded from awards;')
i = 1
for (person, badge, awarded) in old_crs.fetchall():
    try:
        event = get_badge_event(old_crs, person, badge, {'organizer' : event_lookup, 'instructor' : cohort_lookup})
        fields = (i, awarded, badge_lookup[badge], person_lookup[person], event)
        new_crs.execute('insert into workshops_award values(?, ?, ?, ?, ?);', fields)
    except Exception, e:
        fail('award', fields, e)
    i += 1

info('award')

trainer_stuff =  [
    ['2012-08-26-ttt-online', ['wilson.g']],
    ['2012-10-11-ttt-online', ['wilson.g']],
    ['2013-01-06-ttt-online', ['wilson.g']],
    ['2013-03-12-ttt-online', ['wilson.g']],
    ['2013-05-12-ttt-online', ['wilson.g']],
    ['2013-08-12-ttt-online', ['wilson.g']],
    ['2013-09-30-ttt-online', ['wilson.g']],
    ['2014-01-16-ttt-online', ['wilson.g']],
    ['2014-04-14-ttt-pycon', ['wilson.g']],
    ['2014-04-24-ttt-online', ['wilson.g']],
    ['2014-04-28-ttt-mozilla', ['wilson.g']],
    ['2014-06-05-ttt-online', ['wilson.g']],
    ['2014-06-11-ttt-online', ['wilson.g']],
    ['2014-09-10-ttt-online', ['wilson.g']],
    ['2014-09-22-ttt-uva', ['wilson.g', 'mills.b']],
    ['2014-10-22-ttt-tgac', ['wilson.g', 'mills.b', 'pawlik.a']],
    ['2014-11-12-ttt-washington', ['wilson.g', 'mills.b']],
    ['2015-01-06-ttt-ucdavis', ['wilson.g', 'mills.b', 'teal.t', 'pawlik.a']],
    ['2015-02-01-ttt-online', ['wilson.g']],
    ['2015-04-xx-ttt-nih', ['wilson.g']],
    ['2015-05-01-ttt-online', ['wilson.g']],
    ['2015-09-01-ttt-online', ['wilson.g']]
]
instructor = select_one(new_crs, "select id from workshops_role where name='instructor';")
for (slug, all_persons) in trainer_stuff:
    for person in all_persons:
        try:
            fields = (task_id, event_lookup[slug], person_lookup[person], instructor)
            new_crs.execute('insert into workshops_task values(?, ?, ?, ?);', fields)
        except Exception, e:
            fail('training instructors', fields, e)
        task_id += 1

#------------------------------------------------------------
# Wrap up.
#------------------------------------------------------------

# Commit all changes.
new_cnx.commit()
