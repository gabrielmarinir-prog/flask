from flask import Blueprint, render_template, request

bp = Blueprint('calculos', __name__, url_prefix='/calculos')

def calcular_irpf(salario_bruto):
    if salario_bruto <= 2259.20:
        return 0.0
    elif salario_bruto <= 2826.65:
        return (salario_bruto * 0.075) - 169.44
    elif salario_bruto <= 3751.05:
        return (salario_bruto * 0.15) - 381.44
    elif salario_bruto <= 4664.68:
        return (salario_bruto * 0.225) - 662.77
    else:
        return (salario_bruto * 0.275) - 896.00

def calcular_rescisao(salario_base, meses_trabalhados):
    return (salario_base / 12) * min(meses_trabalhados, 12)

@bp.route('/painel', methods=['GET', 'POST'])
def painel():
    resultado_irpf = None
    resultado_rescisao = None

    if request.method == 'POST':
        tipo = request.form.get('tipo_calculo')
        if tipo == 'irpf':
            salario = float(request.form.get('salario_bruto', 0))
            resultado_irpf = round(max(calcular_irpf(salario), 0), 2)
        elif tipo == 'rescisao':
            salario = float(request.form.get('salario_base', 0))
            meses = int(request.form.get('meses_trabalhados', 0))
            resultado_rescisao = round(calcular_rescisao(salario, meses), 2)

    return render_template('calculos/index.html', irpf=resultado_irpf, rescisao=resultado_rescisao)