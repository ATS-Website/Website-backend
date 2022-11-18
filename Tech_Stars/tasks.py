from django.utils import timezone
from django.conf import settings
from celery import shared_task
import csv
timezone.activate(settings.TIME_ZONE)


def read_csv(file_name):
    with open(file_name, "r") as x:
        read = csv.DictReader(x)
        return list(read)


@shared_task(bind=True)
def write_log_csv(event, admin, message):
    with open("admin_activity_logs.csv", "a", newline="\n") as x:
        header = ["Date_Time", "Event", "Admin", "Message"]
        write = csv.DictWriter(x, fieldnames=header)

        data = {
            "Date_Time": timezone.now(),
            "Event": event,
            "Admin": admin,
            "Message": message,
        }

        if len(read_csv("admin_activity_logs.csv")) < 1:
            write.writeheader()
            write.writerow(data)
        else:
            write.writerow(data)

@shared_task(bind=True)
def write_server_logs(url: str, status_code: str, request_body=""):
    if status_code.startswith("2"):
        with open("access_server_logs.csv", "a", newline="\n") as x:
            header = ["Date_Time", "url", "request_body"]
            write = csv.DictWriter(x, fieldnames=header)

            data = {
                "Date_Time": timezone.localtime(timezone.now()),
                "url": url,
                "request_body": request_body
            }
            if len(read_csv("access_server_logs.csv")) < 1:
                write.writeheader()
                write.writerow(data)
            else:
                write.writerow(data)
    else:
        with open("error_server_logs.csv", "a", newline="\n") as x:
            header = ["Date_Time", "url"]
            write = csv.DictWriter(x, fieldnames=header)

            data = {
                "Date_Time": timezone.localtime(timezone.now()),
                "url": url
            }
            if len(read_csv("error_server_logs.csv")) < 1:
                write.writeheader()
                write.writerow(data)
            else:
                write.writerow(data)

    with open("complete_server_logs.csv", "a", newline="\n") as y:
        complete_header = ["Date_Time", "status",
                           "url", "status_code", "request_body"]
        complete_write = csv.DictWriter(y, fieldnames=complete_header)

        data = {
            "Date_Time": timezone.localtime(timezone.now()),
            "url": url,
            "status_code": status_code,
            "request_body": request_body
        }

        if status_code.startswith("2"):
            data["status"] = "Success"
        else:
            data["status"] = "Error"

        if len(read_csv("complete_server_logs.csv")) < 1:
            complete_write.writeheader()
            complete_write.writerow(data)
        else:
            complete_write.writerow(data)
