Pylint-mongoengine is a pylint plugin for mongoengine and mongomotor. Inspired
by the pylint-django plugin.


Install
=======

Install it using pip:

```sh
   $ pip install pylint-mongoengine
```


Usage
=====

From the command line use the ``--load-plugins`` parameter:

```sh
   $ pylint --load-plugins=pylint_mongoengine mycode/
```

or add ``load-plugins=pylint_mongoengine`` to your pylintrc file

#### How to use in VS-Code:
Open the Command Palette (⇧⌘P), then type `Preferences: Configure Language Specific Settings`, select Python and add the following code:

```json
"python.linting.pylintArgs": [
  "--load-plugins=pylint-mongoengine"
]
```
