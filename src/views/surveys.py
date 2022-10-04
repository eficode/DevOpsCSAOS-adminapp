from flask import render_template, redirect, request, abort, Blueprint
from flask import current_app as app
import helper
from services.survey_service import survey_service


surveys = Blueprint("surveys", __name__)


@surveys.route("/new_survey")
def new():
    """Renders the new survey page
    """
    if not helper.logged_in():
        return redirect("/")

    return render_template("surveys/new_survey.html", ENV=app.config["ENV"])


@surveys.route("/surveys/edit/<survey_id>")
def surveys_edit(survey_id):
    """Renders the edit survey page
    """
    if not helper.logged_in():
        return redirect("/")

    survey = survey_service.get_survey(survey_id)

    return render_template("surveys/edit_survey.html", survey=survey, survey_id=survey_id)


@surveys.route("/surveys/update", methods=["POST"])
def surveys_update():
    """ Form handler for updating an existing survey info
    """

    if not helper.valid_token(request.form):
        abort(403)

    survey_id = request.form["survey_id"]
    name = request.form["name"]
    title = request.form["title"]
    survey = request.form["text"]

    # TODO: Implement the SQL query for updating a survey
    #  result = survey_service.update_survey(survey_id, name, title, text)

    route = f"/surveys/{survey_id}"

    return redirect(route)


@surveys.route("/create_survey", methods=["POST"])
def create_survey():
    """ Takes arguments from new.html
    and calls a db function using them
    which creates a survey into Surveys
    """

    if not helper.valid_token(request.form):
        abort(403)

    name = request.form["name"]
    title = request.form["title"]
    survey = request.form["survey"]
    survey_id = survey_service.create_survey(name, title, survey)
    route = f"/surveys/{survey_id}"

    return redirect(route)


@surveys.route("/surveys/<survey_id>")
def view_survey(survey_id):
    """ Looks up survey information based
    on the id with a db function and renders
    a page with the info from the survey """

    if not helper.logged_in():
        return redirect("/")

    survey = survey_service.get_survey(survey_id)
    questions = survey_service.get_questions_of_survey(survey_id)

    return render_template("surveys/view_survey.html", survey=survey, questions=questions, survey_id=survey_id)


@surveys.route("/surveys/statistics/<survey_id>")
def surveys_statistics(survey_id):
    """ Open up statistics for the given survey
    """

    if not helper.logged_in():
        return redirect("/")

    survey = survey_service.get_survey(survey_id)

    #  TODO: get statistics
    statistics = "JUGE STATS HERE!"

    return render_template("surveys/statistics.html", survey=survey, statistics=statistics, survey_id=survey_id)


@surveys.route("/add_question", methods=["POST"])
def add_question():
    """ Adds a new question to the database
    """

    if not helper.valid_token(request.form):
        abort(400, 'Invalid CSRF token.')

    categories = survey_service.get_all_categories()
    try: 
        category_weights = helper.category_weights_as_json(
            categories, request.form)
    except ValueError:
        return "Invalid weights"    
    text = request.form["text"]
    survey_id = request.form["survey_id"]
    survey_service.create_question(text, survey_id, category_weights)
    return redirect(f"/surveys/{survey_id}")


@surveys.route("/<survey_id>/new_question", methods=["GET"])
def new_question(survey_id):
    """  Retuns the page for creating a new question.
    """
    stored_surveys = survey_service.get_all_surveys()
    stored_categories = survey_service.get_all_categories()
    survey = survey_service.get_survey(survey_id)
    # pylint: disable-next=line-too-long
    return render_template("questions/new_question.html", ENV=app.config["ENV"], surveys=stored_surveys, categories=stored_categories, survey=survey)


@surveys.route("/edit_question")
def edit_question():
    """Renders the page for editing a question
    """
    if not helper.logged_in():
        return redirect("/")

    return render_template("questions/edit_question.html", ENV=app.config["ENV"])
