pip install scikit-learn numpy pandas
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# ----------- 1. نموذج تعلم آلي مبسط لتوقع درجة الحرارة المثلى ----------
# بيانات تدريبية بسيطة لمحاكاة العلاقة بين عدد الجماهير والحرارة المثلى
X_train = np.array([1000, 5000, 10000, 20000, 30000]).reshape(-1, 1)  # عدد الجماهير
y_train = np.array([24, 23, 22, 21, 20])  # درجة الحرارة المثلى

model_temp = LinearRegression()
model_temp.fit(X_train, y_train)

# ----------- 2. دالة لمحاكاة قراءة البيانات من المستشعرات ----------
def read_sensors():
    return {
        'temperature': np.random.uniform(20, 35),      # درجة الحرارة داخل الملعب
        'humidity': np.random.uniform(40, 80),         # نسبة الرطوبة
        'light_level': np.random.uniform(200, 1000),   # شدة الإضاءة (لومين)
        'airflow': np.random.uniform(0.5, 3.0),         # قوة التهوية (م/ث)
        'crowd_count': np.random.randint(1000, 30000)  # عدد الجماهير الحالي
    }

# ----------- 3. نظام اتخاذ القرار والتحكم الذكي ----------
def control_environment(data):
    decisions = []

    predicted_temp = model_temp.predict([[data['crowd_count']]])[0]
    print(f"\n📊 بيانات المستشعرات: {data}")
    print(f"🤖 الحرارة المتوقعة المثلى للجمهور: {predicted_temp:.1f}°C")

    # التحكم في التكييف
    if data['temperature'] > predicted_temp + 1:
        decisions.append(" تفعيل التكييف (تبريد إضافي)")
    elif data['temperature'] < predicted_temp - 1:
        decisions.append(" تقليل التكييف / تفعيل تدفئة")
    else:
        decisions.append(" درجة الحرارة ضمن المستوى المثالي")

    # التحكم في الرطوبة
    if data['humidity'] > 65:
        decisions.append(" تفعيل مزيل الرطوبة")
    elif data['humidity'] < 40:
        decisions.append(" تفعيل جهاز ترطيب الهواء")
    else:
        decisions.append(" الرطوبة ضمن النطاق الطبيعي")

    # التحكم في الإضاءة
    if data['light_level'] < 400:
        decisions.append(" زيادة الإضاءة الاصطناعية")
    elif data['light_level'] > 900:
        decisions.append(" تقليل الإضاءة الاصطناعية")
    else:
        decisions.append(" الإضاءة مناسبة")

    # التهوية
    if data['airflow'] < 1.0:
        decisions.append(" زيادة سرعة التهوية")
    else:
        decisions.append(" التهوية جيدة")

    return decisions

# ----------- 4. المحاكي الرئيسي للنظام ----------
def run_system():
    for cycle in range(3):  # محاكاة 3 دورات قراءة وتحكم
        data = read_sensors()
        decisions = control_environment(data)
        print("\n📡 الإجراءات المتخذة:")
        for action in decisions:
            print("→", action)
        print("-" * 40)

# ----------- 5. تشغيل النظام ----------
if __name__ == "__main__":
    print(" بدء نظام التحكم الذكي في بيئة الملعب...\n")
    run_system()
