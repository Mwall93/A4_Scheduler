from flask import request, Blueprint, render_template, url_for, session

from datetime import datetime

from core import JsonResponse
from core import Database
from core import Config
from core import Authorization

from model.Term import Term as TermModel

Settings = Blueprint('Settings', __name__)

@Settings.route('/settings', methods=['GET'])
def List():
    """ Lists all campuses using campus_list.html """
    # Authenticate user
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return render_template('error/no_access.html')
    
    # Get list of terms
    terms = TermModel.all()
    term_list = []

    for term in terms:
        term_list.append({
            'term': term,
            'startDate': datetime.utcfromtimestamp(term.getStartDate()).strftime("%B %Y"),
            'endDate': datetime.utcfromtimestamp(term.getEndDate()).strftime("%B %Y"),
            'startDateHtml': datetime.utcfromtimestamp(term.getStartDate()).strftime("%Y-%m-%d"),
            'endDateHtml': datetime.utcfromtimestamp(term.getEndDate()).strftime("%Y-%m-%d")
        })

    return render_template('settings.html', data = {
        'terms': term_list
    })


@Settings.route('/settings/term', methods=['POST'])
def CreateTerm():
    """ Creates a new Campus """
    # Authenticate user
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this page. Contact system administrator.'})

    term = request.form.get('term')
    term_start = request.form.get('term_start')
    term_end = request.form.get('term_end')

    if not term or not term_start or not term_end:
        return JsonResponse.badRequest({'message': 'missing_parameters', 'nice_message': 'Please enter term number, term start date and term end date.'})

    if term not in ('1', '2', '3', 1, 2, 3):
        return JsonResponse.badRequest({'message': 'bad_request', 'nice_message': 'Please select a term number between 1 and 3.'})
    
    term_start = yyyyMmDdToTimestamp(term_start)
    term_end = yyyyMmDdToTimestamp(term_end)

    termObj = TermModel()

    termObj.setTerm(int(term)) \
           .setStartDate(term_start) \
           .setEndDate(term_end) \
           .save()
    
    return JsonResponse.ok()

@Settings.route('/settings/term/<term_id>', methods=['POST'])
def UpdateTerm(term_id):
    """ Creates a new Campus """
    # Authenticate user
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})

    term = request.form.get('term')
    term_start = request.form.get('term_start')
    term_end = request.form.get('term_end')

    if not term or not term_start or not term_end:
        return JsonResponse.badRequest({'message': 'missing_parameters', 'nice_message': 'Please enter a new term number, start date or end date.'})

    if term not in ('1', '2', '3', 1, 2, 3):
        return JsonResponse.badRequest({'message': 'bad_request', 'nice_message': 'Please select a term between 1 and 3.'})
    
    termObj = TermModel.findById(term_id)

    if not termObj:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Term not found.'})
    
    if term:
        termObj.setTerm(term)
    
    if term_start:
        termObj.setStartDate(yyyyMmDdToTimestamp(term_start))
    
    if term_end:
        termObj.setEndDate(yyyyMmDdToTimestamp(term_end))
    
    termObj.save()
    
    return JsonResponse.ok()

@Settings.route('/settings/term/<term_id>', methods=['DELETE'])
def DeleteTerm(term_id):
    """ Creates a new Campus """
    # Authenticate user
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})

    if not term_id:
        return JsonResponse.badRequest({'message': 'bad_request', 'nice_message': 'Please enter the term'})
    
    term = TermModel.findById(term_id)

    if not term:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Term not found.'})

    term.delete()
    
    return JsonResponse.ok()

def yyyyMmDdToTimestamp(theDate):
    theDate = theDate.split('-')

    theDate[0] = int(theDate[0])
    theDate[1] = int(theDate[1])
    theDate[2] = int(theDate[2])

    yearInSeconds = 86400 * 365
    monthInSeconds = 30.4167 * 86400
    dayInSeconds = 86400

    out = 1

    out = (theDate[0] - 1970) * yearInSeconds
    out = out + ( theDate[1] * monthInSeconds )
    out = out + ( theDate[2] * dayInSeconds )
    out = out + 120 # for good measure

    return out