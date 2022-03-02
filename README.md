# Python User Agent Parser

`user_agent_parser` is a Python 3 library that provides an easy way to identify/detect devices from user agent string
* User agent is a mobile or computer
* User agent Browser name and versions
* User agent Device name

`user_agent_parser` hosted on [PyPI](http://pypi.python.org/pypi/user-agent-parser/) and can be installed as such:


    pip install install user-agent-parser

Alternatively, you can also get the latest source code from [Github](https://github.com/Purushot14/user-agent-parser) and install it manually.

```python 
from user_agent_parser import Parser
iphone_ua_str = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.90 Mobile/15E148 Safari/604.1"
parser = Parser(iphone_ua_str)

 # Calling parser
 browser, browser_version, os, os_version, device_type, device_name, device_host = parser()
 # or you can call directly properties
 parser.device_name
```
Running Tests

_____________

    python -m unittest discover


Changelog
__________

### Version 0.1.1

* Doc added

### Version 0.1

* Initial release