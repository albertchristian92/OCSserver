import MySQLdb
from linebot import LineBotApi
from linebot.models import *
import socketserver
from datetime import datetime
import calendar


line_bot_api = LineBotApi('aKYIbzTEv+C76MkXP1jPbFFsCLUpxrdK5ux9ShVdG+Zs3qFIytbrdx4qPsOWh7TRGCTy05C+/qVsvEyctI3VBrd7Rq/sbkaLiBv1WfYUcdNZH42+RexdUCGkKbU1zn1lFzzzHR3dyG4B+LT5xoiuBgdB04t89/1O/w1cDnyilFU=')
channel_secret ='U7a77a69cb7c24fd5c48821f2c122dbb7'
buttons_template_message = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        thumbnail_image_url='https://example.com/image.jpg',
        title='Menu',
        text='Do you want to accept the promotion?',
        actions=[
        URIAction(
                label='yes',
                uri='https://goo.gl/forms/FLhTFKasrJMCJB652'
            ),
            MessageAction(
                label='no',
                text='no'
            ),

        ]
    )
)

def quotaNotif():
    try:
        line_bot_api.push_message(channel_secret, TextSendMessage(text='your mobile network quota is empty'))
        line_bot_api.push_message(channel_secret, buttons_template_message)
        print("notification sent")
    except:
        print("Can't send message, internet off")


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    month_name = datetime.now().month
    month_name = calendar.month_name[month_name]
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "", "ocs_database")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    cursor.execute(
        "SELECT mobile_usage FROM tbl_totalnetworkusage where month_name= month_name order by mobile_usage DESC limit 1")
    print("\nfetch one:")
    res = cursor.fetchall()
    for row in res:
        compare = row[0]

    if compare > 2000:
        quotaNotif()
    db.close()

if __name__ == "__main__":
    print("Server On")
    HOST, PORT = "140.113.86.142", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()