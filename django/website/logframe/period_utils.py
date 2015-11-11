from datetime import date, timedelta


def get_month_shift(month, num_periods, period_offset=1):
    """ Given a start month return the calendar month of the period with
    offset by period_offset.

    If the month is in the next calendar year add_year is 1, so it can be
    taken into account by the caller.
    """
    new_month = month + (12 / num_periods) * period_offset

    add_year = 0 if new_month < 13 else 1
    new_month = new_month if new_month < 13 else new_month % 12
    if new_month == 0:  # December
        new_month = 12
    return (new_month, add_year)


def get_periods(start_date, end_date, year_start, num_periods):
    """ Given the time frame start_date to end_date, year start month and
    number of periods return the minimum list of periods to cover all of it.

    So the first period will contain start_date, and the last period will
    contain end_date.
    """
    periods_begin = [get_month_shift(year_start, num_periods, p) for p
                     in range(num_periods)]
    periods = []
    # Start year earlier to catch also start: 1.1. End is always covered by
    # the last period of the year
    for year in range(start_date.year - 1, end_date.year + 1):
        for month, year_carry in periods_begin:
            periods.append(date(year + year_carry, month, 1))
    start = end = 0
    for i, period in enumerate(periods):
        if period <= start_date:
            start = i
        if period > end_date:
            end = i  # Matches i-1 as the last index
            break
    if not end:
        end = len(periods)
    periods = periods[start:end]
    return periods


def get_period(start_date, num_periods):
    start_date = date(*[int(x) for x in start_date.split("-")])
    new_month, add_year = get_month_shift(start_date.month, num_periods)
    next_period = date(start_date.year + add_year, new_month, 1)
    return (start_date, next_period - timedelta(days=1))


def periods_intersect(s, e, x, y):
    '''
          x|---------1---------|y
    <----2-----|y
                          x|-----3---->
    <-4--|y
               x|----5---|y
         x|----6---|y
                       x|----7---|y
    <---------------8----------------->
                                x|-9-->
             s               e
    ---------|---------------|---------

    Correct matches:
        1) x >= s & x <= e      [3, 5, 7]
        2) x <= s & y >= s      [1, 2, 6]

        3) x <= e & y is None (no end date)
        4) y >= s & x is None (no start date)

        5) x & y both None      [8]

    assumptions: x < y, s < e
    '''
    if not y and not x:
        return True
    if not y:
        return x <= e
    elif not x:
        return y >= s
    else:
        return (x >= s and x <= e) or (x <= s and y >= s)
