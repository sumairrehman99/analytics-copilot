def recommend_chart(results: list):

    if not results:
        return None

    first_row = results[0]
    columns = list(first_row.keys())

    if len(columns) != 2:
        return None

    x = columns[0]
    y = columns[1]

    if "date" in x:
        chart = "line"

    elif "hour" in x:
        chart = "bar"

    elif "count" in y or "amount" in y or "revenue" in y:
        chart = "bar"

    else:
        chart = "table"

    return {
        "type": chart,
        "x": x,
        "y": y
    }