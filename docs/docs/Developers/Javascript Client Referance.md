# Javascript Client Reference

## Plan
`class: fsl.Plan(plan, options)`

A flight plan interface.
#### Parameters
##### plan
`object`

Plan data, object, as defined in Server API.

##### options
`object` `optional`

Currently there are no specific options to load to this class.

### createButton (buttonOptions)
Append a button connected to Plan.send in to a DOM object.
#### Parameters
##### buttonOptions

`object`

| Field | Type | Description |
|--|--|--|
| to | String | ID of a DOM object to append to |
| text | String | Inside text of the button |

### send (options)
Send current flight plan to server. (desktop application)

#### Parameters
##### options

`object`

| Field | Type | Description |
|--|--|--|
| caller | DOM Element | a DOM element (like button) to disable during HTTP request. It gets activated after request is over. |


## Utility
`class: fsl.Utility()`

Utily class. Might be subject to change.

### collect (collectionMapping)
Accepts collectionMapping object. Keys should be equal to flight plan fields defined in Server API.
Values can be in two formats.

Returns collected data from DOM elements.

#### Parameters
##### collectionMapping
###### Get result of a function call.
'func' field accepts a function. Function receives whole object as an argument. So you can use other fields in the object as you wish.
```
'block_time': {
    func: function,
    example: 'example'
}
```

###### Get values from DOM objects.
| field | description |
|--|--|
| selector | CSS selector. It will receive first DOM object with given CSS selector. |
| attribute | Which attribute to read from |

> Special case: 'innerHTML' can be given as 'attribute', in this case innerHTML will be read eventhough it is not an attribute.

```javascript
{
    'destination': {
        selector: '#my-div',
        attribute: 'innerHTML'
    },
    'departure': {
        selector: '#my-input',
        attribute: 'value'
    },
    'aircraft': {
        selector: 'input[name="aircraft"]:checked',
        attribute: 'value'
    }
}
```

### send (data, options):
Creates a flight plan using data, and sends it.
#### Parameters
##### data
Flight plan data. Defined in server API.
Check Plan.send() for more details.
##### options
Flight plan send options.
Check Plan.send() for more details.