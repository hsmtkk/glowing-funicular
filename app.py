import datetime
import json

import requests
import streamlit as st
import pandas as pd

import config

API_URL = "http://127.0.0.1:8000"


def main():
    page = st.sidebar.selectbox("Choose your page", ["users", "rooms", "bookings"])
    page_map = {"users": show_users, "rooms": show_rooms, "bookings": show_bookings}
    page_map[page]()


def show_users():
    st.title("ユーザー登録")

    with st.form(key="user"):
        username: str = st.text_input("ユーザー名", max_chars=config.USERNAME_MAX)
        data = {"username": username}
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        url = API_URL + "/users"
        res = requests.post(url, data=json.dumps(data))
        if res.status_code == 200:
            st.success("ユーザー登録完了")
        st.json(res.json())


def show_rooms():
    st.title("会議室登録")

    with st.form(key="room"):
        room_name: str = st.text_input("会議室名", max_chars=config.ROOM_NAME_MAX)
        capacity: int = st.number_input("定員", step=1)
        data = {"room_name": room_name, "capacity": capacity}
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        url = API_URL + "/rooms"
        res = requests.post(url, data=json.dumps(data))
        if res.status_code == 200:
            st.success("会議室登録完了")
        st.json(res.json())


def show_bookings():
    st.title("会議室予約画面")

    url = API_URL + "/users"
    res = requests.get(url)
    users = res.json()
    users_dict = {}
    for u in users:
        users_dict[u["username"]] = u["user_id"]

    url = API_URL + "/rooms"
    res = requests.get(url)
    rooms = res.json()
    rooms_dict = {}
    for r in rooms:
        rooms_dict[r["room_name"]] = {
            "room_id": r["room_id"],
            "capacity": r["capacity"],
        }

    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ["会議室名", "定員", "会議室ID"]
    st.write("## 会議室一覧")
    st.table(df_rooms)

    url = API_URL + "/bookings"
    res = requests.get(url)
    bookings = res.json()
    df_bookings = pd.DataFrame(bookings)

    users_id = {}
    for u in users:
        users_id[u["user_id"]] = u["username"]

    rooms_id = {}
    for r in rooms:
        rooms_id[r["room_id"]] = {
            "room_name": r["room_name"],
            "capacity": r["capacity"],
        }

    to_username = lambda x: users_id[x]
    to_room_name = lambda x: rooms_id[x]["room_name"]
    to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime(
        "%Y/%m/%d %H:%M"
    )

    df_bookings["user_id"] = df_bookings["user_id"].map(to_username)
    df_bookings["room_id"] = df_bookings["room_id"].map(to_room_name)
    df_bookings["start_datetime"] = df_bookings["start_datetime"].map(to_datetime)
    df_bookings["end_datetime"] = df_bookings["end_datetime"].map(to_datetime)

    df_bookings = df_bookings.rename(
        columns={
            "user_id": "予約者名",
            "room_id": "会議室名",
            "booked_num": "予約人数",
            "start_datetime": "開始時刻",
            "end_datetime": "終了時刻",
            "booking_id": "予約番号",
        }
    )

    st.write("## 予約一覧")
    st.table(df_bookings)

    with st.form(key="booking"):
        username: str = st.selectbox("予約者名", users_dict.keys())
        room_name: str = st.selectbox("会議室名", rooms_dict.keys())
        booked_num: int = st.number_input("予約人数", step=1, min_value=1)
        date = st.date_input("日付を入力", min_value=datetime.date.today())
        start_time = st.time_input("開始時刻", value=datetime.time(hour=9, minute=0))
        end_time = st.time_input("終了時刻", value=datetime.time(hour=20, minute=0))
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        user_id: int = users_dict[username]
        room_id: int = rooms_dict[room_name]["room_id"]
        capacity: int = rooms_dict[room_name]["capacity"]

        data = {
            "user_id": user_id,
            "room_id": room_id,
            "booked_num": booked_num,
            "start_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute,
                second=start_time.second,
            ).isoformat(),
            "end_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute,
                second=end_time.second,
            ).isoformat(),
        }

        if booked_num <= capacity:
            url = API_URL + "/bookings"
            res = requests.post(url, data=json.dumps(data))
            if res.status_code == 200:
                st.success("予約完了")
            st.json(res.json())
        else:
            st.error(f"{room_name}の定員は{capacity}名です。{capacity}名以下の予約人数のみ受け付けます。")


if __name__ == "__main__":
    main()
