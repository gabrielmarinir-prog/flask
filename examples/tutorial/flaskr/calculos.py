@bp.route('/painel', methods=('GET', 'POST'))
def painel():
    resultado_irpf = None
    resultado_rescisao = None

    if request.method == 'POST':
        tipo_calculo = request.form.get('tipo_calculo')

        if tipo_calculo == 'irpf':
            salario_bruto = float(request.form.get('salario_bruto', 0))
            resultado_irpf = calcular_irpf(salario_bruto)

        elif tipo_calculo == 'rescisao':
            salario_base = float(request.form.get('salario_base', 0))
            meses_trabalhados = int(request.form.get('meses_trabalhados', 0))
            resultado_rescisao = calcular_decimo_terceiro_proporcional(salario_base, meses_trabalhados)

    return render_template(
        'calculos/index.html',
        resultado_irpf=resultado_irpf,
        resultado_rescisao=resultado_rescisao
    )