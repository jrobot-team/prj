# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta

from base_creator import Booking
from botutils import get_booking
from sender import alert_auto_func


def cheker():
    date = datetime.now()
    delta_end = date + timedelta(minutes=10)
    delta_start = date - timedelta(minutes=10)
    bookings = get_booking('true_booking', dtf=True)
    for book in bookings:
        d = book.get('date')
        hours_chek = d - timedelta(hours=3)
        day_chek = d - timedelta(days=1)
        if book.get('hours_alert'):
            if d < date:
                Booking.update(status='done_booking').where(Booking.id == book.get('id')).execute()
        if book.get('alerted') == 0:
            if day_chek > date:
                alert_auto_func(book.get('id'))
                Booking.update(alerted=1).where(Booking.id == book.get('id')).execute()
        if book.get('hours_alert') == 0:
            if hours_chek > delta_start and hours_chek < delta_end:
                alert_auto_func(book.get('id'))
                Booking.update(hours_alert=1).where(Booking.id == book.get('id')).execute()


def main():
    while True:
        try:
            cheker()
            time.sleep(300)
        except:
            pass


if __name__ == "__main__":
    main()
