from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
from src.models import Event
from src import app, db
from flask_login import current_user
from flask_moment import Moment
moment = Moment(app)
# import pdb; pdb.set_trace()

event_blueprint = Blueprint('event_blueprint', __name__, template_folder='../../templates')

@event_blueprint.route("/events", methods=["GET", "POST"])
@login_required
def events():
    events = Event.query.all()
    if request.method == "POST":
        new_event = Event(
            event_name = request.form["event_name"],
            event_description = request.form["event_description"],
            event_banner = request.form["event_banner"],
            event_address = request.form["event_address"],
            event_time = request.form["event_time"],
            ticket_price = request.form["ticket_price"],
            ticket_stock = request.form["ticket_stock"],
            user_id = current_user.id
        )
        db.session.add(new_event)
        db.session.commit()
        flash("Successfully added a new event.", "success")
        return redirect(url_for("event_blueprint.events"))
    return render_template("event/events.html", events = events)

@event_blueprint.route("/events/<id>", methods=["GET", "POST"])
def event_detail(id):
    action = request.args.get('action')
    event = Event.query.get(id)
    return render_template("event/view_event.html", event = event)
