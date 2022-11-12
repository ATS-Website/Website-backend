import base64
import datetime

import qrcode
import io
import csv


def generate_qr_code(data, size=10, border=0):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    return img


def generate_qr(text):
    generated_code = generate_qr_code(text, size=10, border=1)
    bio = io.BytesIO()
    generated_code.save(bio)
    png_qr = bio.getvalue()
    base64qr = base64.b64encode(png_qr)
    img_name = base64qr.decode("utf-8")
    context = {"file_type": "png", "image_base64": img_name}
    return context


def read_csv(file_name):
    with open(file_name, "r") as x:
        read = csv.DictReader(x)
        return list(read)


def write_log_csv(event, admin, message):
    with open("admin_activity_logs.csv", "a", newline="\n") as x:
        header = ["Date_Time", "Event", "Admin", "Message"]
        write = csv.DictWriter(x, fieldnames=header)

        data = {
            "Date_Time": datetime.datetime.now(),
            "Event": event,
            "Admin": admin,
            "Message": message,
        }

        if len(read_csv("admin_activity_logs.csv")) < 1:
            write.writeheader()
            write.writerow(data)
        else:
            write.writerow(data)


def write_server_logs(url: str, status_code: str):
    if status_code.startswith("2"):
        with open("access_server_logs.csv", "a", newline="\n") as x:
            header = ["Date_Time", "url"]
            write = csv.DictWriter(x, fieldnames=header)

            data = {
                "Date_Time": datetime.datetime.now(),
                "url": url
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
                "Date_Time": datetime.datetime.now(),
                "url": url
            }
            if len(read_csv("error_server_logs.csv")) < 1:
                write.writeheader()
                write.writerow(data)
            else:
                write.writerow(data)

    with open("complete_server_logs.csv", "a", newline="\n") as y:
        complete_header = ["Date_Time", "status", "url", "status_code"]
        complete_write = csv.DictWriter(y, fieldnames=complete_header)

        data = {
            "Date_Time": datetime.datetime.now(),
            "url": url,
            "status_code": status_code
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




