import momo
from momo import layouts


app = momo.Momo()


def bmi(height: float, weight: float) -> float:
    return weight / (height ** 2)


@app.page('/')
def bmi():

    # Let's create an UI to compute one's BMI

    # Create height & weight input
    height_inp = momo.input('My height')
    weight_inp = momo.input('My weight', required=True)
    # Create button 'Send'
    send = momo.button('Compute my BMI')
    # Create inputs area
    inputs = layouts.Column(
        height_inp,
        weight_inp,
        send,
    )
    inputs.style = 'border: 1px solid gold'
    # Create output area
    output = momo.div('output', style='border: 1px solid green;')
    # organise 
    layout = layouts.Line(inputs, output)
    # Associate action [call <function> then store output in <output area>]
    # send.action = app.call(bmi, args={'height': height_inp.value, 'weight': weight_inp.value})

    return layout


if __name__ == '__main__':
    app.run(debug=True)
