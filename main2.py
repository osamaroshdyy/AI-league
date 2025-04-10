import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from streamlit_autorefresh import st_autorefresh
import time
import os

# ---------- إعداد النموذج التنبؤي ----------
X_train = np.array([1000, 5000, 10000, 20000, 30000]).reshape(-1, 1)
y_train = np.array([24, 23, 22, 21, 20])
model_temp = LinearRegression()
model_temp.fit(X_train, y_train)

# ---------- محاكاة بيانات المستشعرات ----------
def read_sensors():
    return {
        'temperature': round(np.random.uniform(20, 35), 2),
        'humidity': round(np.random.uniform(40, 80), 2),
        'light_level': round(np.random.uniform(200, 1000), 2),
        'airflow': round(np.random.uniform(0.5, 3.0), 2),
        'crowd_count': np.random.randint(1000, 30000)
    }

# ---------- اتخاذ القرار ----------
def control_environment(data):
    predicted_temp = model_temp.predict([[data['crowd_count']]])[0]
    decisions = []

    if data['temperature'] > predicted_temp + 1:
        decisions.append(" تفعيل التكييف (تبريد إضافي)")
    elif data['temperature'] < predicted_temp - 1:
        decisions.append(" تقليل التكييف / تفعيل تدفئة")
    else:
        decisions.append(" درجة الحرارة ضمن المستوى المثالي")

    if data['humidity'] > 65:
        decisions.append(" تفعيل مزيل الرطوبة")
    elif data['humidity'] < 40:
        decisions.append(" تفعيل جهاز ترطيب الهواء")
    else:
        decisions.append(" الرطوبة ضمن النطاق الطبيعي")

    if data['light_level'] < 400:
        decisions.append(" زيادة الإضاءة الاصطناعية")
    elif data['light_level'] > 900:
        decisions.append(" تقليل الإضاءة الاصطناعية")
    else:
        decisions.append(" الإضاءة مناسبة")

    if data['airflow'] < 1.0:
        decisions.append(" زيادة التهوية")
    else:
        decisions.append(" التهوية جيدة")

    return decisions, predicted_temp

# ---------- حفظ سجل الأحداث ----------
def save_log(data, decisions):
    log = pd.DataFrame({
        "temperature": [data["temperature"]],
        "humidity": [data["humidity"]],
        "crowd": [data["crowd_count"]],
        "actions": [", ".join(decisions)],
        "timestamp": [pd.Timestamp.now()]
    })
    file_exists = os.path.isfile("system_log.csv")
    log.to_csv("system_log.csv", mode='a', header=not file_exists, index=False)

# ---------- واجهة المستخدم ----------
st.set_page_config(page_title="لوحة تحكم بيئة الملعب", layout="wide")
st.title(" لوحة تحكم بيئة الملعب الذكية بالذكاء الاصطناعي")

# تحديث تلقائي كل 10 ثواني
st_autorefresh(interval=10000, key="auto_refresh")

sensor_data = read_sensors()
decisions, predicted_temp = control_environment(sensor_data)
save_log(sensor_data, decisions)

col1, col2 = st.columns(2)

with col1:
    st.subheader(" بيانات المستشعرات")
    st.metric("عدد الجماهير", sensor_data['crowd_count'])
    st.metric("درجة الحرارة", f"{sensor_data['temperature']} °C")
    st.metric("الرطوبة", f"{sensor_data['humidity']} %")
    st.metric("الإضاءة", f"{sensor_data['light_level']} لومين")
    st.metric("التهوية", f"{sensor_data['airflow']} م/ث")

with col2:
    st.subheader(" قرارات النظام")
    st.write(f"درجة الحرارة المثالية المتوقعة: **{predicted_temp:.1f}°C**")
    for d in decisions:
        st.success(d) if "" in d else st.warning(d) if "" in d else st.info(d)

# ---------- عرض الرسم البياني ----------
if "history" not in st.session_state:
    st.session_state["history"] = []

st.session_state["history"].append({
    "time": time.strftime("%H:%M:%S"),
    "temp": sensor_data['temperature'],
    "humidity": sensor_data['humidity']
})

st.subheader(" تغير درجة الحرارة والرطوبة")
df = pd.DataFrame(st.session_state["history"])
st.line_chart(df.set_index("time")[["temp", "humidity"]])