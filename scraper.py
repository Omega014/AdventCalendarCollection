import json
import os
import urllib.request

from bs4 import BeautifulSoup


YEAR = "2016"

ADVENTAR_URL = "http://www.adventar.org/users/7109?year=2016"

QIITA_TARGET_USERS = ["OMEGA014"]  # TwitterとGithubとでどっちも登録しちゃった時用
QIITA_URL = "http://qiita.com/advent-calendar/2016/my-calendar"
QIITA_CATEGORIES = [
    "to_be_decided",
    "programming_languages",
    "libraries",
    "databases",
    "web_technologies",
    "mobile",
    "devops",
    "iot",
    "os",
    "editors",
    "academic",
    "services",
    "company",
    "miscellaneous"
]


def _scrape_adventar():
    """ ADVENTERから
        参加登録中のカレンダーのタイトルと年月日を取得して返す関数
    """
    html = urllib.request.urlopen(ADVENTAR_URL).read()
    soup = BeautifulSoup(html)

    # デザイン変更で動かなくなる可能性がある
    registrations = []
    for data in soup.find_all("span"):
        date = data.parent.find("span").string[:10]  # '2016-12-05（月）'から曜日を削る
        title = data.parent.find("a").string
        registrations.append({"title": title, "date": date})

    return registrations


def _scrape_qiita_advent_calendar():
    """ Qiita Advent Calendarから
        参加登録中のカレンダーのタイトルと年月日を取得して返す関数
    """
    # 公開されている全てのカレンダーのURLをリストに集約
    urls = []
    for category in QIITA_CATEGORIES:
        html = urllib.request.urlopen(
            "http://qiita.com/advent-calendar/{}/categories/{}".format(YEAR, category)
        ).read()
        soup = BeautifulSoup(html)

        target_xml = soup.select("[class~=adventCalendarList_calendarTitle]")
        for target in target_xml:
            title = target.find_all("a")[-1].string
            url = "http://qiita.com{}".format(target.find_all("a")[-1]["href"])
            urls.append(url)

    registrations = []
    # 自分が登録してるカレンダーだけを探して日付とタイトルを辞書に格納
    for url in urls:
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html)

        title = soup.title.string

        # 特定のユーザ名がauthorの日付を探す
        target_xml = soup.select("[class~=adventCalendarCalendar_day]")
        for idx, target in enumerate(target_xml):
            # 参加登録されていない空き日は飛ばす
            if not target.img:  # imgのaltでユーザ名を取得...
                continue
            user_name = target.img["alt"]
            if user_name in QIITA_TARGET_USERS:
                date = "{}-12-{}".format(YEAR, idx+1)
                registrations.append({"title": title, "date": date})

    return registrations


def main():
    """ アドベントカレンダーの登録情報をjsonに保存する関数
        Viewのリフレッシュボタンで実行される
    """
    # 登録したカレンダー情報を辞書に格納
    registrations = []
    # 同じカレンダーに複数登録する場合はdateをリストにしたほうが良さそう
    registrations = _scrape_adventar()
    registrations += _scrape_qiita_advent_calendar()

    # 毎回読み込みすると重くて辛いのでjsonに最新のデータを持たせておく
    # View側にリフレッシュボタンを設ける
    filepath = os.path.join(os.path.realpath('./'), 'registrations.json')
    os.remove(filepath)
    with open(filepath, 'a') as f:
        json.dump(registrations, f, indent=4)
