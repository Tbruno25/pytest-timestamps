# pytest-timestamps

A simple plugin to view the timestamps in-line with each test.

## Installation

Use the package manager [pip](https://pypi.org/project/pip/) or [poetry](https://python-poetry.org/) to install.

```bash
pip install pytest-timestamps
```
```bash
poetry add pytest-timestamps
```

## Usage

The timestamps used depend whether Pytest is running in `verbose` mode.\
**verbose:** node\
**non verbose:** module\
![](https://i.ibb.co/0qLXFjB/Screenshot-from-2022-01-10-22-00-26.png)

Timestamps will also be added to the test report if [pytest-html](https://github.com/pytest-dev/pytest-html) is installed.



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
