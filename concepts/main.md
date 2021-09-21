# Momo UI

The idea is to be able to generate functional web app components from Python. You can then call Python functions (for which POST endpoints are generated on the spot) through those components. These endpoints / functions can return JSON data or new viewports/layouts which will be translated into HTML.

## Simple Form

For example, a simple form + a button that fetches the answer to a simple function:

```py
import momo


def bmi(weight: float, height: float) -> float:
    return weight / height ** 2


# Create the form
with momo.Form() as form:
    weight = form.input('Weight')
    height = form.input('Height')
    submit = form.submit('Calculate your BMI')

# Create the output area
output = momo.div()

# Add a Javascript POST call to button.onclick
# Behind the scenes, generate a POST endpoint for bmi
# + Specify type conversions
submit.action = momo.call(bmi, {'height': height &float, 'weight': weight &float}, output)

# Lay it out more nicely
return momo.layout.Row(form, output)
```
Should get us something like:

```
| <Weight>           |  | <Output>                |
| <Height>           |
[ Calculate your BMI ]
```

## File Upload & Progress

Let's say that now we need to process a file. We'll need to be able to upload it and apply various filters as is usually available.

And since processing takes some time, we'd like to have a progress display. Let's say that's something we can express using a decorator and a parameter injection.

The wrapper also returns a view instead of just data, a HTML component which displays progress + Calls to a special endpoint to request updates on the task's progress.

```py

@viewport  # or feed an entire viewport object to it
def process(data: bytes, view):
    rows = load(data)
    count = 0
    for row in view.track_progress(rows):
        count += row
    details = [{'total': count}]
    return layout.Col(view, momo.table(details))
        

with Form() as form:
    # A drag & drop OR browse component to pick a file
    file = form.FileLoader('The file to process', types=['text/csv', 'xlsx', ...])
    form.submit('Process file')

output = div()

form.action = call(process, {'data': file}, output)

return layout.Row(form, output)
```
While the file is being processed:
```
| Upload file |  | [++++     ] 40% processed <> |
[   Process   ]  |                              |
```
And then

```
| Upload file |  | [+++++++++] 100% processed <checkmark> |
[   Process   ]  | <additional info sent by the function> |
```

## Tabs

```py
with TabGroup() as tg:
    with tg.Tab('Load data') as tab:
        with tab.Form() as form:
            ...
    with tg.Tab('Metrics') as tab:
        tab += tab.table(headers=['a', 'b'])

return tg
```

## Synced data

Something like:

```py
var = momo.Var()
label = momo.p(content=var)
```

Then you'd need to implement some kind of update/listen flow between front & back.

eg

You have a unique event matrix

* A unique event matrix endpoint to check for events
* Another endpoint to publish events
* Backend-side triggers on update
* Frontend-side triggers on update

* `GET /event/<id>` to check events about you
* `POST /event/<id>` to publish an event about you ("my value changed")

```py
class EventMatrix:
    def __init__(self):
        self.events = defaultdict(list)
    def publish(self, about: str, event: dict):  # aka POST /event/<about>
        self.events[about].append(event)
    def pull(self, about: str):  # aka GET /event/<about>
        return self.events.pop(about)
```

```py


class Page(Element):
    title: str
    body: Element
    scripts: List[Script]
    styles: List[StyleSheet]


def Call(
    f: Callable,
    args: Dict[str, Union[
        Element,  # e.g args = { weight: weight }
        ElementAttributeHook,  # e.g args = { weight: weight.value }
        Any,  # anything else as a static arg
        ]
    ],
    output: Element | None | 
)


def compute_bmi(weight: float, height: float) -> float:
    return weight / height ** 2


@app.page('/')
def home():
    with Page() as page:
        page.title = 'Home'

        with page.Panel() as panel:
            class Inputs:
                weight = panel.input(label='Your weight', placeholder='Weight', required=True)
                height = panel.input(label='Your height', placeholder='Height', required=True)
            panel.Button('Send').action = Call(compute_bmi, args=dict(height=height, weight=weight), to=)

        with page.Form() as form:
            form.input(id='weight', label='Your weight')
            form.input(id='height', label='Your height')
            form.action = compute_bmi

        return page  
```