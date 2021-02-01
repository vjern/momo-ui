import logging

import momo
from momo import layout
from flask import request


app = momo.Momo()


def bmi(height: float, weight: float) -> float:
    return weight / (height ** 2)


@app.page('/')
def bmi_page():

    # Let's create an UI to compute one's BMI

    # Create height & weight input
    with momo.Form() as f:
        height = f.input('My height', required=True)
        weight = f.input('My weight', required=True)
    # Create button 'Send'
        submit = f.button('Compute my BMI')
    # Create inputs area
    inputs = layout.Column(
        height,
        weight,
        submit,
    )
    # inputs.style = 'border: 1px solid gold'
    # Create output area
    output = momo.div('output\noutput\noutput')
    # organise 
    l = layout.Line(inputs, output)
    # Associate action [call <function> then store output in <output area>]

    submit.props['onclick'] = app.call(
        bmi,
        args={'height': height & float, 'weight': weight & float},
        output=output
    )

    return l


# @app.app.route('/bmi', methods=['POST'])
# def bmi_endpoint():
#     return {'result': bmi(**request.json)}


app = app.app

if __name__ == '__main__':
    app.run(debug=True)
