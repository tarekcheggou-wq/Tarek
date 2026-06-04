from flask import Flask, request, render_template_string
import os
import math

app = Flask(__name__)

# تقسيم النص لتفادي مشاكل الـ SyntaxError أثناء النسخ واللصق
HTML_PART1 = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>آلة حاسبة علمية احترافية</title><style>
:root { --bg-color: #0f172a; --calc-bg: #1e293b; --screen-bg: #0f172a; --btn-num: #334155; --btn-op: #f59e0b; --btn-sci: #475569; --text-main: #f8fafc; }
body { font-family: sans-serif; background-color: var(--bg-color); display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }
.calculator { background: var(--calc-bg); width: 100%; max-width: 450px; padding: 25px; border-radius: 24px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.3); }
h3 { color: var(--text-main); text-align: center; margin-top: 0; margin-bottom: 20px; }
.screen { background: var(--screen-bg); padding: 20px; border-radius: 16px; text-align: left; margin-bottom: 20px; border: 1px solid #334155; min-height: 90px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;}
.expression { color: #94a3b8; font-size: 1.1rem; text-align: right; min-height: 24px; word-wrap: break-word; }
.result { color: var(--text-main); font-size: 2.2rem; font-weight: bold; text-align: right; word-wrap: break-word; }
.grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; }
button { border: none; padding: 18px 10px; font-size: 1.1rem; font-weight: 600; border-radius: 12px; cursor: pointer; color: var(--text-main); transition: all 0.2s ease; }
button:hover { filter: brightness(1.2); }
.num { background-color: var(--btn-num); } .op { background-color: var(--btn-op); color: #0f172a; } .sci { background-color: var(--btn-sci); font-size: 0.95rem; }
.clear { background-color: #ef4444; grid-column: span 2; } .equal { background-color: #10b981; grid-column: span 2; color: #fff; }
</style></head><body><div class="calculator"><h3>آلة حاسبة علمية</h3><div class="screen">"""

HTML_PART2 = """<div class="expression">{{ expression if expression else "" }}</div><div class="result">{{ result if result is not none else "0" }}</div></div><form method="POST" class="grid">
<button type="submit" name="action" value="clear" class="clear">C</button><button type="submit" name="action" value="sci_sin" class="sci">sin</button><button type="submit" name="action" value="sci_cos" class="sci">cos</button><button type="submit" name="action" value="sci_tan" class="sci">tan</button>
<button type="submit" name="action" value="sci_sqrt" class="sci">√x</button><button type="submit" name="action" value="sci_pow2" class="sci">x²</button><button type="submit" name="action" value="sci_log" class="sci">log</button><button type="submit" name="action" value="sci_ln" class="sci">ln</button><button type="submit" name="action" value="op_divide" class="op">÷</button>
<button type="submit" name="action" value="num_7" class="num">7</button><button type="submit" name="action" value="num_8" class="num">8</button><button type="submit" name="action" value="num_9" class="num">9</button><button type="submit" name="action" value="sci_pi" class="sci">π</button><button type="submit" name="action" value="op_multiply" class="op">×</button>
<button type="submit" name="action" value="num_4" class="num">4</button><button type="submit" name="action" value="num_5" class="num">5</button><button type="submit" name="action" value="num_6" class="num">6</button><button type="submit" name="action" value="sci_fact" class="sci">x!</button><button type="submit" name="action" value="op_subtract" class="op">-</button>
<button type="submit" name="action" value="num_1" class="num">1</button><button type="submit" name="action" value="num_2" class="num">2</button><button type="submit" name="action" value="num_3" class="num">3</button><button type="submit" name="action" value="sci_exp" class="sci">e</button><button type="submit" name="action" value="op_add" class="op">+</button>
<button type="submit" name="action" value="num_0" class="num">0</button><button type="submit" name="action" value="num_dot" class="num">.</button><button type="submit" name="action" value="equal" class="equal">=</button>
<input type="hidden" name="current_expr" value="{{ next_expr }}"></form></div></body></html>"""

HTML_TEMPLATE = HTML_PART1 + HTML_PART2

@app.route('/', methods=['GET', 'POST'])
def calculator():
    display_expr = ""
    result = None
    current_expr = ""

    if request.method == 'POST':
        action = request.form.get('action', '')
        current_expr = request.form.get('current_expr', '')

        if action == 'clear':
            current_expr = ""
            result = 0
        elif action.startswith('num_'):
            val = action.split('_')[1]
            current_expr += '.' if val == 'dot' else val
        elif action.startswith('op_'):
            op_map = {'add': '+', 'subtract': '-', 'multiply': '*', 'divide': '/'}
            val = op_map[action.split('_')[1]]
            current_expr += f" {val} "
        elif action == 'sci_pi':
            current_expr += str(math.pi)
        elif action == 'sci_exp':
            current_expr += str(math.e)
        elif action.startswith('sci_'):
            sci_op = action.split('_')[1]
            try:
                base_val = eval(current_expr) if current_expr else 0
                if sci_op == 'sin': result = math.sin(math.radians(base_val))
                elif sci_op == 'cos': result = math.cos(math.radians(base_val))
                elif sci_op == 'tan': result = math.tan(math.radians(base_val))
                elif sci_op == 'sqrt': result = math.sqrt(base_val)
                elif sci_op == 'pow2': result = math.pow(base_val, 2)
                elif sci_op == 'log': result = math.log10(base_val)
                elif sci_op == 'ln': result = math.log(base_val)
                elif sci_op == 'fact': result = math.factorial(int(base_val))
                
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                current_expr = str(result)
            except Exception:
                result = "خطأ رياضي"
                current_expr = ""
        elif action == 'equal':
            try:
                if current_expr:
                    res = eval(current_expr)
                    result = int(res) if isinstance(res, float) and res.is_integer() else round(res, 6)
                    current_expr = str(result)
                else:
                    result = 0
            except ZeroDivisionError:
                result = "لا يمكن القسمة على 0"
                current_expr = ""
            except Exception:
                result = "خطأ في الصيغة"
                current_expr = ""

        display_expr = current_expr.replace('*', '×').replace('/', '÷')

    return render_template_string(HTML_TEMPLATE, expression=display_expr, result=result, next_expr=current_expr)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    from waitress import serve
    print(f"Starting server on port {port}...")
    serve(app, host='0.0.0.0', port=port)
