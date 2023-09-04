from flask import Blueprint, render_template
from flask_login import login_required


orders_pb = Blueprint("orders", __name__, url_prefix="")

@orders_pb.route("/")
@login_required
def index():
    return render_template("orders.html")
