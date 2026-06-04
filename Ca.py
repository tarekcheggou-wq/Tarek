from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>آلة حاسبة بسيطة</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f9; }
        .calculator { display: inline-block; padding: 20px; border: 1px solid #ccc; background: #fff; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }
        input, select, button { margin: 10px; padding: 10px; font-size: 16px; width: 80%; border-radius: 5px; border: 1px solid #ccc; box-sizing: border-box; }
        button { background-color: #28a745; color: white; cursor: pointer; border: none; font-weight: bold; }
        button:hover { background-color: #218838; }
        .result { font-size: 20px; font-weight: bold; color: #333; margin-top: 15px; padding: 10px; background-color: #e9ecef; border-radius: 5px; }
    </style>
</head>
<body>

<div class="calculator">
    <h2>آلة حاسبة أونلاين</h2>
    <form method="POST">
        <input type="number" step="any" name="num1" placeholder="العدد الأول" required>
        <select name="operation">
            <option value="add">جمع (+)</option>
            <option value="subtract">طرح (-)</option>
            <option value="multiply">ضرب (×)</option>
            <option value="divide">قسمة (÷)</option>
        </select>
        <input type="number" step="any" name="num2" placeholder="العدد الثاني" required>
        <button type="submit">احسب</button>
    </form>

    {% if result is not none %}
        <div class="result">النتيجة: {{ result }}</div>
    {% endif %}
</div>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    if request.method == 'POST':
        try:
            num1 = request.form.get('num1', type=float)
            num2 = request.form.get('num2', type=float)
            operation = request.form.get('operation')

            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                if num2 != 0:
                    result = num1 / num2
                else:
                    result = "خطأ: لا يمكن القسمة على صفر!"
        except Exception as e:
            result = f"خطأ في الإدخال: {str(e)}"
                
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    # استدعاء سيرفر الإنتاج خفيف الوزن Waitress
    from waitress import serve
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting server on port {port}...")
    serve(app, host='0.0.0.0', port=port)
