from flasgger import Swagger, swag_from
from flask import Flask, redirect, url_for, request, jsonify, make_response
from flask_restful import reqparse, abort, Api, Resource
from app import db
from app.models import Project, Worker, Temperature, Power, Alarm
from sqlalchemy import and_
import json
import random
import datetime, time

import bitstring
import json
import urllib
from app.email import send_email
from app.utils import index_color


# api = Api(app)
#
# swagger = Swagger(app)



avatars = [
  'https://gw.alipayobjects.com/zos/rmsportal/WdGqmHpayyMjiEhcKoVE.png', 
  # // Alipay
  'https://gw.alipayobjects.com/zos/rmsportal/zOsKZmFRdUtvpqCImOVY.png', 
  # // Angular
  'https://gw.alipayobjects.com/zos/rmsportal/dURIMkkrRFpPgTuzkwnB.png', 
  # // Ant Design
  'https://gw.alipayobjects.com/zos/rmsportal/sfjbOqnsXXJgNCjCzDBL.png', 
  # // Ant Design Pro
  'https://gw.alipayobjects.com/zos/rmsportal/siCrBXXhmvTQGWPNLBow.png', 
  # // Bootstrap
  'https://gw.alipayobjects.com/zos/rmsportal/kZzEzemZyKLKFsojXItE.png', 
  # // React
  'https://gw.alipayobjects.com/zos/rmsportal/ComBAopevLwENQdKWiIn.png', 
  # // Vue
  'https://gw.alipayobjects.com/zos/rmsportal/nxkuOJlFJuAUhzlMTCEe.png', 
  # // Webpack
]

avatars2 = [
  'https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
  'https://gw.alipayobjects.com/zos/rmsportal/cnrhVkzwxjPwAaCfPbdc.png',
  'https://gw.alipayobjects.com/zos/rmsportal/gaOngJwsRYRaVAuXXcmB.png',
  'https://gw.alipayobjects.com/zos/rmsportal/ubnKSIfAJTxIgXOKlciN.png',
  'https://gw.alipayobjects.com/zos/rmsportal/WhxKECPNujWoWEFNdnJE.png',
  'https://gw.alipayobjects.com/zos/rmsportal/jZUIxmJycoymBprLOUbT.png',
  'https://gw.alipayobjects.com/zos/rmsportal/psOgztMplJMGpVEqfcgF.png',
  'https://gw.alipayobjects.com/zos/rmsportal/ZpBqSxLxVEXfcUNoPKrz.png',
  'https://gw.alipayobjects.com/zos/rmsportal/laiEnJdGHVOhJrUShBaJ.png',
  'https://gw.alipayobjects.com/zos/rmsportal/UrQsqscbKEpNuJcvBZBu.png',
]

covers = [
  'https://gw.alipayobjects.com/zos/rmsportal/uMfMFlvUuceEyPpotzlq.png',
  'https://gw.alipayobjects.com/zos/rmsportal/iZBVOIhGJiAnhplqjvZW.png',
  'https://gw.alipayobjects.com/zos/rmsportal/uVZonEtjWwmUZPBQfycs.png',
  'https://gw.alipayobjects.com/zos/rmsportal/gLaIAoVWTtLbBWZNYEMg.png',
]

desc = [
  '那是一种内在的东西， 他们到达不了，也无法触及的',
  '希望是一个好东西，也许是最好的，好东西是不会消亡的',
  '生命就像一盒巧克力，结果往往出人意料',
  '城镇中有那么多的酒馆，她却偏偏走进了我的酒馆',
  '那时候我只会想自己想要什么，从不想自己拥有什么',
]

user = [
  '付小小',
  '曲丽丽',
  '林东东',
  '周星星',
  '吴加好',
  '朱偏右',
  '鱼酱',
  '乐哥',
  '谭小仪',
  '仲尼',
]


class Projects(Resource):
    '''
        get the projects.
    '''

    def get(self):

        projects = db.session.query(Project.id, Project.name).order_by(
            
            Project.id.asc()).all()

        projectLists = []

        for project in projects:
            project_id = project[0]
            project_name = project[1]
            projectLists.append({
                'id':project_id,
                'owner':'wjj',
                'title':project_name,
                'avatar':avatars[random.randint(0, 7)],
                'status': ['active', 'exception', 'normal'][random.randint(0, 2)],
                'percent': random.randint(0, 40) + 60,
                'logo': avatars[random.randint(0, 7)],
                'href': '/#/project/worker/' + project_name,
                'updatedAt': datetime.datetime.now(),
                'createdAt': datetime.datetime.now(),
                'subDescription': desc[random.randint(0, 4)],
                'description':project_name * 5 
                })

        print(projectLists)
        return jsonify(projectLists) 

    def post(self):
        pass


    def delete(self):
        pass


    def put(self):
        pass


class Workers(Resource):
    '''
        get the workers.
    '''

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project_name', type=str)
        args = parser.parse_args()

        print('--------project_name-------', args)

        projectName = args['project_name']


        workers = db.session.query(Worker.id, Worker.name).join(
            Project, Project.id == Worker.project_id).filter(
            Project.name == projectName).order_by(
            Worker.id.asc()).all()


        worker_names=[]

        for worker in workers:

            worker_id = worker[0]
            worker_name = worker[1]
            worker_names.append({
                'id':worker_id,
                'owner':'wjj',
                'title':worker_name,
                'avatar':avatars[random.randint(0, 7)],
                'status': ['active', 'exception', 'normal'][random.randint(0, 2)],
                'percent': random.randint(0, 40) + 60,
                'logo': avatars[random.randint(0, 7)],
                'href': '/#/dashboard/analysis/' + worker_name,
                'updatedAt': datetime.datetime.now(),
                'createdAt': datetime.datetime.now(),
                'subDescription': desc[random.randint(0, 4)],
                'description':worker_name * 5 
                })

        return jsonify(worker_names) 

    def post(self):
        pass


    def delete(self):
        pass

    def put(self):
        pass



class TemperatureRealtime(Resource):
    '''
        get the lates temp.
    '''

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('worker_name', type=str)
        args = parser.parse_args()

        print('--------worker_name-------', args)

        workerName = args['worker_name']

        temp_realtime = db.session.query(Temperature.datetime, Temperature.value).join(
            Worker, Worker.id == Temperature.worker_id).filter(
            Worker.name == workerName).order_by(
            Temperature.datetime.desc()).first()



        print('--------temp_realtime--------\n' * 3)
        print(temp_realtime)

        temp_values = json.loads(temp_realtime[1])
        temp_datetime = temp_realtime[0]
        temp_datetime_str = datetime.datetime.strftime(temp_datetime, "%H-%M-%S")
        temp_dict = {'name':temp_datetime_str}

        temp_dict_list = []
        for temp_value in temp_values:
            temp_dict[temp_value[0]] = float(temp_value[1])
        temp_dict_list.append(temp_dict)

        print('--------temp_dict_list---- \n' *3)
        print(temp_dict_list)

        realtimeBars = []
        # for temp_value in temp_values:
        for i in range(len(temp_values)):
            temp_value = temp_values[i]
            realtimeBars.append({'dataKey': temp_value[0], 'fill':index_color(i)})

        return jsonify({'temperatureData': temp_dict_list, 'realtimeBars': realtimeBars}) 

    def post(self):
        pass


    def delete(self):
        pass

    def put(self):
        pass


class TemperatureAlarm(Resource):
    '''
        get the lates alarm.
    '''

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('worker_name', type=str)
        args = parser.parse_args()

        print('--------worker_name-------', args)

        workerName = args['worker_name']

        temp_alarm = db.session.query(Alarm.datetime, Alarm.value).join(
            Worker, Worker.id == Alarm.worker_id).filter(
            Worker.name == workerName).order_by(
            Alarm.datetime.desc()).first()

        temp_alarms = json.loads(temp_alarm[1])

        alarm_dict_list = []
        for temp_alarm in temp_alarms:
            print(temp_alarm[1])
            if temp_alarm[1] == '1':
                alarm_dict = {'type': 'danger', 'icon':'warning', 'channel': temp_alarm[0], 'alarm': temp_alarm[1]}
            else:
                alarm_dict = {'type': 'dashed', 'icon':'sync', 'channel': temp_alarm[0], 'alarm': temp_alarm[1]}

            alarm_dict_list.append(alarm_dict)


        return jsonify({'temperatureAlarm': alarm_dict_list}) 

    def post(self):
        pass


    def delete(self):
        pass

    def put(self):
        pass


class TemperatureHistory(Resource):
    '''
        get the lates 10 temps.
    '''

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('worker_name', type=str)
        args = parser.parse_args()

        print('--------worker_name-------', args)

        workerName = args['worker_name']

        temp_history = db.session.query(Temperature.datetime, Temperature.value).join(
            Worker, Worker.id == Temperature.worker_id).filter(
            Worker.name == workerName).order_by(
            Temperature.datetime.desc()).limit(20).all()


        temp_dict_lists = []
        for temperatures in temp_history:
            temp_datetime = temperatures[0]
            temp_datetime_str = datetime.datetime.strftime(temp_datetime, "%H:%M:%S")
            temp_values = json.loads(temperatures[1])

            print(temp_values)

            temp_dict = {'time':temp_datetime_str}
            for temp_value in temp_values:
                temp_dict[temp_value[0]] = float(temp_value[1])
            temp_dict_lists.append(temp_dict)

        print(temp_dict_lists)

        historyLines = []

        temp_value = temp_history[0]
        temp_lines = json.loads(temp_value[1])
        print('all lines:', temp_lines)

        for i in range(len(temp_lines)):
            temp_line = temp_lines[i]
            historyLines.append({'type': 'monotone', 'dataKey':temp_line[0], 'stroke':index_color(i)})

        return jsonify({'temperatureHistory': temp_dict_lists, 'historyLines': historyLines}) 

    def post(self):
        pass


    def delete(self):
        pass

    def put(self):
        pass


class TemperatureRecord(Resource):
    '''
        get the temp records by the input datetime. %H:%M:S%
    '''

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('worker_name', type=str)
        args = parser.parse_args()

        print('--------worker_name-------', args)

        workerName = args['worker_name']

        temps_records = db.session.query(Temperature.datetime, Temperature.value).join(
            Worker, Worker.id == Temperature.worker_id).filter(
            Worker.name == workerName).order_by(
            Temperature.datetime.desc()).all()


        temp_dict_lists = []
        # for temperatures in temps_records:
        for i in range(len(temps_records)):
            temperatures = temps_records[i]
            temp_datetime = temperatures[0]
            temp_datetime_str = datetime.datetime.strftime(temp_datetime, "%Y-%m-%d %H:%M:%S")
            temp_values = json.loads(temperatures[1])

            print(temp_values)

            temp_dict = {'key':i, 'datetime':temp_datetime_str}

            for temp_value in temp_values:
                temp_dict[temp_value[0]] = float(temp_value[1])

            temp_dict_lists.append(temp_dict)

        print('--temp_dict_lists---\n' * 3)
        print(temp_dict_lists)


        temps_record = temps_records[0][1]
        recordColumns = [{
                  'title': '时间',
                  'dataIndex': 'datetime',
                  'key': 'datetime',
                }]


        channels = json.loads(temps_record)
        for channel in channels:
            recordColumns.append({'title': channel[0],
                  'dataIndex': channel[0],
                  'key': channel[0],})
        print('-----recordColumns---\n' * 3)

        print(recordColumns)

        return jsonify({'temperatureRecord': temp_dict_lists, 'recordColumns':recordColumns}) 

    def post(self):
        pass


    def delete(self):
        pass

    def put(self):
        pass


class CurrentPower(Resource):
    '''
        get the power voltage and current value. 
    '''

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('worker_name', type=str)
        args = parser.parse_args()

        print('--------worker_name-------', args)

        workerName = args['worker_name']

        current_power = db.session.query(Power.datetime, Power.value).order_by(Power.datetime.desc()).first()
        # current_power = db.session.query(Power.datetime, Power.value).filter(
        #     and_(Power.project == 1, Power.worker == 1)).order_by(Power.datetime.desc()).first()

        history_power = db.session.query(Power.datetime, Power.value).order_by(
            Power.datetime.desc()).limit(10).all()

        # history_power = db.session.query(Power.datetime, Power.value).filter(
        #     and_(Power.project == 1, Power.worker == 1)).order_by(
        #     Power.datetime.desc()).limit(10).all()

        powerValues = json.loads(current_power[1])

        # first power
        powerValues1 = powerValues[0]
        print('-----------powerValues1------------')
        print(powerValues1)


        mini_area_data1 = []
        mini_area_data2 = []
        mini_area_data3 = []
        mini_area_data4 = []



        for i in range(0,len(history_power)):
            historyPowerValues = history_power[i]
            datetime = historyPowerValues[0].strftime("%H:%M:%S")

            print(datetime)

            # first power
            historyPowerValue = json.loads(historyPowerValues[1])[0]


            print('-----------historyPowerValue-------------')
            print(historyPowerValue)

            
            voltage_dict1 = {'x': datetime,
                            'y': historyPowerValue[1][1]}
            mini_area_data1.append(voltage_dict1)

            voltage_dict2= {'x': datetime,
                            'y': historyPowerValue[1][3]}
            mini_area_data2.append(voltage_dict2)

            voltage_dict3 = {'x': datetime,
                            'y': historyPowerValue[1][5]}
            mini_area_data3.append(voltage_dict3)

            voltage_dict4 = {'x': datetime,
                            'y': historyPowerValue[1][7]}
            mini_area_data4.append(voltage_dict4)

        print('------mini_area_data1-----')
        print(mini_area_data1)
        print(mini_area_data2)
        print(mini_area_data3)
        print(mini_area_data4)


        print(current_power[0])

        current_time = current_power[0].strftime("%Y-%m-%d %H:%M:%S")
        
        channel1_dict ={'bordered':True,
        'title':'电压1',
        'tooltip_title':'通道1',
        'voltage':powerValues1[1][1],
        'footer_label':'时间',
        'footer_value':current_time,
        'contentHeight':46,
        'mini_area_color':'#DC143C',
        'mini_area_data':mini_area_data1,
        }
        

        channel2_dict ={'bordered':True,
        'title':'电压2',
        'tooltip_title':'通道2',
        'voltage':powerValues1[1][3],
        'footer_label':'时间',
        'footer_value':current_time,
        'contentHeight':46,
        'mini_area_color':'#975FE4',
        'mini_area_data':mini_area_data2,
        }
        

        channel3_dict ={'bordered':False,
        'title':'电压3',
        'tooltip_title':'通道3',
        'voltage':powerValues1[1][5],
        'footer_label':'时间',
        'footer_value':current_time,
        'contentHeight':46,
        'mini_area_color':'#0000FF',
        'mini_area_data':mini_area_data3,
        }
        

        channel4_dict ={'bordered':False,
        'title':'电压4',
        'tooltip_title':'通道4',
        'voltage':powerValues1[1][7],
        'footer_label':'时间',
        'footer_value':current_time,
        'contentHeight':46,
        'mini_area_color':'#00FFFF',
        'mini_area_data':mini_area_data4,
        }
        
        current_power_list = []
        current_power_list.append(channel1_dict)
        current_power_list.append(channel2_dict)
        current_power_list.append(channel3_dict)
        current_power_list.append(channel4_dict)

        # return jsonify({'currentPower': current_power_list}) 
        return jsonify({'currentPower': []}) 

    def post(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass


class HistoryPower(Resource):
    '''
        get the power voltage and current value history records.  
    '''

    def get(self):
        current_power = db.session.query(Power.datetime, Power.voltage1, Power.current1, Power.voltage2, Power.current2, Power.voltage3, Power.current3, Power.voltage4, Power.current4).order_by(
            Power.datetime.desc()).first()

        power_log = []
        for i in range(len(temp_records)):
            temp_log.append(
                {"key": i, "time": temp_records[i][3].strftime("%Y-%m-%d %H:%M:%S"), "Temp1": temp_records[i][0],
                 "Temp2": temp_records[i][1], "Temp3": temp_records[i][2]})

        temps_reverse = temp_log[::-1]
        print('------------temps_records--------------')
        # print(temps_reverse)

        temps_record_dict = {"airConTempRecord": temps_reverse}
        return temps_record_dict

    def post(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass

