import cn2an
import re
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class NLPCron:
    """
    2023-04-07 14:03:00
    quqinglei@icloud.com
    只有在句子中包含每日|天|周|月 才会触发，太笼统的不触发
    """

    def __init__(self, message):
        message = cn2an.transform(message, 'cn2an')
        message = message.replace(' ', '').replace('\t', '').replace('到', '-')
        self.message = message
        self.freq = 'T'
        self.dict = {'month': '*', 'day': '*', 'hour': '9', 'min': '0', 'week': '*'}
        self.now = datetime.now()
        self.a1 = re.findall('(每)(天|周|日|月|个月)', self.message)
        self.a2 = re.findall('(定时)|(提醒)|(记得)|(别忘)|(叫)|(要准备)|(提前)|(要去)|(下周)|(本周)|(后天)|(下个月)|(小时)', self.message)
        self.extract_freq()
        self.a2ora1()

    def a2ora1(self):
        test = self.a2 and (not self.a1)
        if not test:
            return
        self.freq = 'F'
        today = re.findall('(今)(天|日)', self.message)
        if today:
            self.dict['day'] = str(self.now.day)
            return
        tomorrow = re.findall('(明)|(天|日)', self.message)
        if tomorrow:
            self.dict['day'] = str((self.now + timedelta(days=1)).day)
            return
        after_tomorrow = re.findall('(后)|(天|日)', self.message)
        if after_tomorrow:
            self.dict['day'] = str((self.now + timedelta(days=2)).day)
            return
        aafter_tomorrow = re.findall('(大后)|(天|日)', self.message)
        if aafter_tomorrow:
            self.dict['day'] = str((self.now + timedelta(days=3)).day)
            return
        weekday = re.findall('下周(\\d)', self.message)
        if '下周' in self.message and (not weekday):
            wd = self.now.weekday()
            last_days = 6 - wd
            next_week_day = self.now + timedelta(days=last_days + 1)
            self.dict['day'] = str(next_week_day.day)
            self.dict['month'] = str(next_week_day.month)
            return
        if weekday:
            weekday = weekday[0]
        if weekday:
            weekday = int(weekday)
            wd = self.now.weekday()
            last_days = 6 - wd
            next_week_day = self.now + timedelta(days=last_days + weekday)
            self.dict['day'] = str(next_week_day.day)
            self.dict['month'] = str(next_week_day.month)
            return
        if '下个月' in self.message:
            tmp = re.findall('下个月(\\d{1,2})', self.message)
            next_month = (self.now + relativedelta(months=1)).replace(day=1)
            self.dict['month'] = str(next_month.month)
            if not tmp:
                self.dict['day'] = '1'
            else:
                self.dict['day'] = tmp[0]
            return

    def is_leap_year(self, year):
        if year % 400 == 0:
            return True
        elif year % 100 == 0:
            return False
        elif year % 4 == 0:
            return True
        else:
            return False

    def extract_freq(self):
        if '每个月' in self.message:
            self.message = self.message.replace('个', '')
        if '每月' in self.message:
            self.dict['month'] = '*'
            day = re.findall('每月(\\d{1,2})', self.message)
            if day:
                self.dict['day'] = str(day[0])
            elif '最后1天' in self.message:
                self.dict['day'] = 'L'
            else:
                self.dict['day'] = '1'
        wk = re.findall('每月周(\\d{1})', self.message)
        if wk:
            self.dict['week'] = wk[0]
            self.dict['day'] = '*'
        elif '每周' in self.message:
            if '每周日' in self.message:
                self.dict['week'] = '0'
            wd = re.findall('每周(\\d{1})', self.message)
            if wd:
                week = wd[0]
                self.dict['week'] = week
        elif '每天' in self.message:
            self.dict['day'] = '*'
        if '点' in self.message:
            hour = re.findall('(\\d{1}|\\d{2})点', self.message)
            if hour:
                h = int(hour[0])
                if h > 23:
                    h = h % 10
                self.dict['hour'] = str(h)
            else:
                self.dict['hour'] = '12'
        if '分' in self.message:
            min = re.findall('(\\d+)分', self.message)
            if min:
                self.dict['min'] = str(min[0])
            else:
                self.dict['min'] = '0'
        if ':' in self.message:
            s = re.findall('(\\d+)\\:(\\d+)', self.message)
            if not s:
                return None
            (hour, min) = s[0]
            self.dict['hour'] = hour
            self.dict['min'] = min
        if '下午' in self.message or '晚上' in self.message or '傍晚' in self.message:
            hour = int(self.dict['hour'])
            if hour < 12:
                hour = hour + 12
            self.dict['hour'] = str(hour)
        if '中午' in self.message:
            self.dict['hour'] = '12'
        if self.dict['day'] == '29':
            year = self.now.year
            if self.is_leap_year(year):
                self.dict['day'] = '28'
        if '月末' in self.message or '月底' in self.message or '最后一天' in self.message:
            self.dict['day'] = 'L'
        if '点半' in self.message:
            self.dict['min'] = '30'
        if '点' in self.message and '分' not in self.message and ('点半' not in self.message):
            min = re.findall('点(\\d+)', self.message)
            if not min:
                min = '0'
            else:
                min = min[0]
            self.dict['min'] = str(min)
        if '每小时' in self.message:
            self.dict['min'] = '0'
            self.dict['hour'] = '*'
            self.dict['day'] = '*'
            self.dict['month'] = '*'
            self.dict['week'] = '*'

    def check(self, min, hour, day, month, week):
        if min != '*':
            m = int(min)
            if m > 59:
                return None
        if hour != '*' and int(hour) > 23:
            return None
        if day not in ['*', 'L'] and (month == '*' or month == '2'):
            day = int(day)
            if self.is_leap_year(self.now.year) and day > 28:
                return None
        if (month == '*' or month in ('1', '3', '5', '7', '8', '10', '12')) and day not in ('*', 'L'):
            if int(day) > 31:
                return None
        if (month == '*' or month in ('2', '4', '6', '9', '11')) and day not in ('*', 'L'):
            if int(day) > 30:
                return None
        return True

    def crontab(self):
        if self.a1 or self.a2:
            ck = self.check(self.dict['min'], self.dict['hour'], self.dict['day'], self.dict['month'], self.dict['week'])
            if ck is None:
                return None
            cron = str(self.dict['min']) + ' ' + str(self.dict['hour']) + ' ' + str(self.dict['day']) + ' ' + str(self.dict['month']) + ' ' + str(self.dict['week']) + ' ' + str(self.freq)
            return cron
        return None

    def cron(self):
        if self.a1 or self.a2:
            ck = self.check(self.dict['min'], self.dict['hour'], self.dict['day'], self.dict['month'], self.dict['week'])
            if ck is None:
                return None
            cron = str(self.dict['min']) + ' ' + str(self.dict['hour']) + ' ' + str(self.dict['day']) + ' ' + str(self.dict['month']) + ' ' + str(self.dict['week'])
            return cron
        return None

def nlp2cron(message):
    nlpcron = NLPCron(message)
    return nlpcron.cron()

def nlp2crons(message):
    nlpcron = NLPCron(message)
    return nlpcron.crontab()
if __name__ == '__main__':
    tasks = ['明天要去医院看病，要带上病历和身份证。', '下周二是最后一天交作业，要抓紧时间写作。', '今天晚上要去参加公司晚宴，别忘了准备礼服和名片。', '明天是国庆节，要提前准备好旅游计划和行程安排。', '今天晚上要去机场接人，别忘了带上车钥匙和行李架。', '明天是父亲的生日，要准备份礼物。', '下周一要提交报告，要抓紧时间写作。', '今天晚上要去参加朋友的生日聚会，别忘了带礼物。', '明天要去旅游，要提前准备好行李和路线规划。', '今天晚上要去健身房锻炼，别忘了带运动鞋和水杯。', '明天要去超市购物，要带上购物清单和购物袋。', '下周五要参加面试，要准备好简历和面试资料。', '今天晚上要去参加音乐会，别忘了带上门票和身份证。', '明天要去旅游，要提前准备好护照和行李箱。', '今天晚上要去参加生日派对，别忘了准备礼物和祝福语。', '每天晚上8点发送课程业绩给张明', '后天晚上10点同学聚会', '每月末10点叫我去上班', '下周5, 10点叫我去公园遛娃', '每周叫我去拜佛', '约好了哈下周我们一起去爬山', '下个月12号我们去北京', '每月周五10点30去爬山', '每周五早上10点25分写周报', '每周五下午3点发送邮件', '每天早上6点定时备份数据库', '每月1号凌晨2点清理日志', '每个月3号10点35去南京', '每小时执行一次备份', '每个月1号凌晨2点清理日志', '每个月最后一天12点20分去散步', '每周日10点去散步', '每周五下午6点10分去散步']
    for task in tasks:
        crontab = nlp2cron(task)
        print(task + ': ' + str(crontab))