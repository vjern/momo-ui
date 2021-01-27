# Web UI

A way to rapidly produce simple interactive UIs for any code.

```py
from WebUI import WebUI, widgets


app = WebUI()


def bmi(height: float, weight: float) -> float:
return weight / (height ** 2)


@app.page('/', 'My BMI')
def bmi(page):

    # Let's create an UI to compute one's BMI

    # Create height & weight input
    height_inp = wui.input('My height')
    weight_inp = wui.input('My weight')
    # Create button 'Send'
    send = wui.button('Compute my BMI')
    # Create inputs area
    inputs = [
        [height_inp],
        [weight_inp],
        [send]
    ]
    # Create output area
    output = wui.div()
    # organise 
    layout = [[inputs, output]]
    # Associate action [call <function> then store output in <output area>]
    send.action = wui.Call(
        f=bmi,
        args={'height': height_inp.value, 'weight': weight_inp.value},
        store_output=output
    )

    return layout
```

