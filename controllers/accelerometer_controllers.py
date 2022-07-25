from datetime import datetime, timedelta
from decimal import Decimal
import os
import time
from flask_cors import CORS
from flask import Flask, render_template, url_for, request, redirect, session, jsonify, send_file, Blueprint, make_response
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from model import ResponseData, db, Accelerometer
import jwt
from config import SECRET_KEY, UPLOAD_FOLDER
from configs.utils import *
from sqlalchemy import func
import sqlalchemy as sa
import csv

accelerometer_router = Blueprint('accelerometer_router', __name__)


@accelerometer_router.route('/api/accelerometer', methods=['GET', 'POST'])
@token_required
def accelerometer_handler(current_user):
    if request.method == 'POST':
        if request.is_json:
        
            # global iter
            # global global_data
            # global global_data_temp
            if request.is_json:
                iter += 1
                datas = request.json['data']
                x = []
                y = []
                z = []
                for item in datas:
                    x.append(item['x'])
                    y.append(item['y'])
                    z.append(item['z'])
                print(x)
                # global_data_temp.extend(datas)
                # global_data.extend(datas)

                # if iter % 6 == 0:
                #     datas = convert_data(global_data)
                #     print("30s")
                #     global_data = []
                # else:
                #     datas = convert_data(datas)

                # result = predict(datas)

                # print(type(datas))
                # print(datas.shape, result)
                # print(iter)
                # print("Length: " + str(len(datas)))
                # print(convert_data(datas))

                return str("result")
        # submitted_file = request.files['file']
        # if submitted_file and allowed_filename(submitted_file.filename):
        #     filename = secure_filename(
        #         submitted_file.filename)
        #     split_filename = '.' in filename and filename.rsplit('.', 1)
        #     filename = ''.join(
        #         split_filename[:-1]) + "_" + str(time.time()) + "." + split_filename[-1]
        #     os.makedirs(os.path.dirname(UPLOAD_FOLDER), exist_ok=True)
        #     submitted_file.save(os.path.join(UPLOAD_FOLDER, filename))
        # else:
        #     return jsonify({"error": "Exception: {}".format(e)}), 404

        # firstLine = open(os.path.join(UPLOAD_FOLDER, filename)).readline().split(" ")[
        #     3].strip().replace("T", " ")

        current_hour = datetime.strptime(firstLine, '%Y-%m-%d %H:%M:%S')

        response_data = ResponseData.query.all()
        get_one = None
        for response in response_data:
            ts = response.timestamp
            if ts.year == current_hour.year and ts.month == current_hour.month and ts.day == current_hour.day and ts.hour == current_hour.hour:
                get_one = response

        if get_one == None:
            get_one = ResponseData(steps=100, timstamp=current_hour)
            db.session.add(get_one)
            db.session.commit()
        else:
            get_one.steps += 1000
            get_one.timestamp = current_hour
            db.session.commit()

        # with open(os.path.join(UPLOAD_FOLDER, filename)) as f:
        #     data = f.readlines()
        #     for line in data:

        #         arr = line.split(" ")
        #         x = Decimal(arr[0])
        #         y = Decimal(arr[1])
        #         z = Decimal(arr[2])
        #         time_string = arr[3].strip().replace("T", " ")

        #         timestamp = datetime.strptime(
        #             time_string, "%Y-%m-%d %H:%M:%S")
        #         acc = Accelerometer(
        #             x=x, y=y, z=z, timestamp=timestamp, id_user=current_user.id)
        #         db.session.add(acc)
        #         db.session.commit()

        # res = {
        #     'msg': get_one.toDict()
        # }
        # except Exception as e:
        #     return jsonify({"error": "Exception: {}".format(e)}), 400
        # return jsonify(res), 200
    elif request.method == 'GET':
        try:
            data = Accelerometer.query.filter(
                Accelerometer.user_id == current_user.id).group_by(func.date_format(Accelerometer.timestamp, '%H')).all()

            res = []
            for acc in data:
                res.append(acc.toDict())
        except Exception as e:
            return jsonify({"error": "Exception: {}".format(e)}), 400
        return jsonify(res), 200
