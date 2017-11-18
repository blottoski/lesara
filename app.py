from datetime import datetime

import dill
import numpy
import pandas as pd
from flask import Flask

app = Flask("Lesara")

RESULT = pd.DataFrame()


def get_longest_interval(order_dates):
    """
    Return the longest interval between two dates from a tuple of dates.
    Return NaN if there are not at least 2 dates.
    """
    if len(order_dates) <= 1:
        return numpy.nan

    intervals = []
    order_dates = sorted(order_dates)
    for i in range(len(order_dates) - 1):
        od1 = order_dates[i]
        od2 = order_dates[i + 1]
        interval = (od2 - od1).days
        intervals.append(interval)

    return max(intervals)


def make_predictions():
    """
    Compute CLV predictions from the "orders.csv" input file.
    """
    with open("model.dill", "rb") as f:
        model = dill.load(f)

    df = pd.read_csv("orders.csv", parse_dates=[5])
    df = df.dropna()
    df[["order_item_id", "num_items"]] = df[["order_item_id", "num_items"]].astype(int)

    max_items_per_customer = df.groupby("customer_id")["num_items"].max()
    max_revenue_per_customer = df.groupby("customer_id")["revenue"].max()
    total_revenue_per_customer = df.groupby("customer_id")["revenue"].sum()
    total_number_of_orders_per_customer = df.groupby("customer_id")["order_id"].count()
    last_order_date_per_customer = df.groupby("customer_id")["created_at_date"].max()
    current_date = datetime(2017, 10, 17)
    days_since_last_order_per_customer = last_order_date_per_customer.apply(lambda x: (current_date - x).days)
    order_dates_per_customer = df.groupby("customer_id")["created_at_date"].aggregate(lambda x: tuple(x))
    longest_interval_per_customer = order_dates_per_customer.apply(get_longest_interval)

    result = pd.concat([
        max_items_per_customer,
        max_revenue_per_customer,
        total_revenue_per_customer,
        total_number_of_orders_per_customer,
        days_since_last_order_per_customer,
        longest_interval_per_customer,
    ], axis=1,
        keys=["max_items", "max_rev", "total_rev", "total_num_orders",
              "days_since_last_order", "longest_interval"])
    avg_longest_interval = result.longest_interval.mean()

    result.longest_interval[result.longest_interval.isna()] = \
        result.days_since_last_order[result.longest_interval.isna()] + avg_longest_interval

    result["predicted_clv"] = model.predict(result.values)
    global RESULT
    RESULT = result


@app.route('/predict_clv/<customer_id>/')
def predict_clv(customer_id):
    try:
        predicted_clv = RESULT.loc[customer_id]["predicted_clv"]
    except KeyError:
        predicted_clv = 0

    return predicted_clv, 200


@app.errorhandler(404)
def page_not_found(error):
    return "Page not found. Example usage: " \
           "/predict_clv/000011265b8a3727c4cc77b494134aca/", 404


if __name__ == "__main__":
    make_predictions()
    app.run()
