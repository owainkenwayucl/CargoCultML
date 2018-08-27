# CargoCultML - a library to read XML-like files into Python

Parsing XML is extremely [dangerous](https://docs.python.org/3/library/xml.html#xml-vulnerabilities).  Even a brief look at [libraries designed to thwart some of the problems](https://pypi.org/project/defusedxml/) is liable to worry you sufficiently that if you are paranoid you might give up altogether.  The fundamental problem, I believe is that XML is *too* flexible and XML parsers are too fully featured, particularly for what most people want to use XML for.  At the other end of the spectrum, a lot of people don't use libraries at all and just write simple, buggy code to strip the data out of files encoded as XML, something I have been guilty of myself.

The plan for this project is to write a library that converts simple documents that look like XML into python data structures, much in the way the `json` libraries in Python do.  So documents like this:

```xml
<xml>
<item>
<tag x=100>Some data</tag>
<tag2>Some other data</tag2>
</item>
</xml>
```

Become *something* like: 

```python
[{'tag_name':'xml', 
  'contents':[{'tag_name':'item',
               'contents':[{'tag_name':'tag', 
                                   'x':'100', 
                            'contents':['Some data']},
                           {'tag_name':'tag2', 
                            'contents':['Some other data']}]
              }]
}]
```

*(exact details to be determined, e.g. when something becomes a list or a dict!)*

Things this library will definitely **not** do:

* Retrieve other documents either from the filesystem or over the network.
* Expand references in documents.