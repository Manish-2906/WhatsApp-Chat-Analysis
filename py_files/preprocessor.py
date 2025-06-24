import pandas as pd
import re
def preprocess(data):

    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"  # Yeh pattern kisi date, time, aur dash (-) wale text ko identify karne ke liye banaya gaya hai
    messages = re.split(pattern, data)[1:]  # slicing to remove 1st empty row
    dates = re.findall(pattern, data)

    df = pd.DataFrame({"user_message": messages, "message_dates": dates})
    df["message_dates"] = pd.to_datetime(df["message_dates"], format=r"%d/%m/%y, %H:%M - ")
    df.rename(columns={"message_dates": "date"}, inplace=True)

    users = []
    messages = []
    for message in df[
        "user_message"]:
        entry = re.split(r"([\w\W]+?):\s", message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append("group notification")
            messages.append(entry[0])



    df["user"] = users
    df["message"] = messages
    df.drop(columns=["user_message"], inplace=True)

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute
    return df







