from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required
from ..forms import TableAssignmentForm
from ..models import db, Employee, Order, OrderDetail, Table, MenuItem, MenuItemType
from sqlalchemy.orm import joinedload

orders_bp = Blueprint("orders", __name__, url_prefix="")

@orders_bp.route("/")
@login_required
def index():
    assignmentForm = TableAssignmentForm()

    # Get the tables and open orders
    tables = Table.query.order_by(Table.number).all()
    open_orders = Order.query.filter(Order.finished == False)

    # Get the table ids for the open orders
    busy_table_ids = [order.table_id for order in open_orders]

    # Filter the list of tables for only the open tables
    open_tables = [table for table in tables if table.id not in busy_table_ids]

    # Finally, convert those tables to tuples for the select field and set the
    # choices property to it
    assignmentForm.tables.choices = [(t.id, f"Table {t.number}") for t in open_tables]

    employees = Employee.query.all()
    assignmentForm.servers.choices = [(em.id, f"Server {em.name}") for em in employees]

    open_orders_data = [(order.id, order.table_id, order.total_price) for order in open_orders]

    menu_item_types_with_items = MenuItemType.query.options(joinedload(MenuItemType.menu_items)).all()
    menu_items_data = [(item.name, [(itm.id, itm.name) for itm in item.menu_items]) for item in menu_item_types_with_items]

    return render_template("orders.html",
                           assignmentForm=assignmentForm,
                           orders=open_orders_data,
                           menu_items=menu_items_data)


@orders_bp.route("/assign", methods=["POST"])
@login_required
def assign_table():
    table_id = request.form.get("tables")
    server_id = request.form.get("servers")

    if table_id is None or server_id is None:
        return redirect(url_for(".index"))

    table = Table.query.get(table_id)
    server = Employee.query.get(server_id)
    new_order = Order(employee=server, table=table, finished=False)

    db.session.add(new_order)
    db.session.commit()

    return redirect(url_for(".index"))


@orders_bp.route("/closetable/<int:orderId>", methods=["POST"])
@login_required
def close_table(orderId):
    order_to_close = Order.query.get(orderId)
    order_to_close.finished = True
    db.session.commit()
    return redirect(url_for(".index"))


@orders_bp.route("/orders/<int:orderId>/items", methods=["POST"])
@login_required
def add_to_order(orderId):
    order_to_add_to = Order.query.get(orderId)
    for menu_item_id in request.form.getlist("checkboxes"):
        menu_item = MenuItem.query.get(menu_item_id)
        new_order_details = OrderDetail(order=order_to_add_to, menu_item=menu_item)
        db.session.add(new_order_details)
    db.session.commit()
    return redirect(url_for(".index"))
