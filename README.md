# Backend-Practice

A simple API to manage a weekly schedule of custom events

## Events

**URI**: `/event/<event_name>`

**GET**: Returns event details

**POST**: Create a new event
Expected args:
```javascript
{
    "days": [
        <string>,   // One or many of Sun, Mon, Tue, Wed, Thu, Fri, Sat
        ...
    ],
    "from_time": "HH:MM:SS",
    "to_time": "HH:MM:SS",
    "description": <string> // Optional
}
```

**PUT**: Update an existing event
Expected args: (Only include fields to update)
```javascript
{
    "days": [
        <string>,   // One or many of Sun, Mon, Tue, Wed, Thu, Fri, Sat
        ...
    ],
    "from_time": "HH:MM:SS",
    "to_time": "HH:MM:SS",
    "description": <string>
}
```

**DELETE**: Delete the named event

## Schedule

**URI**: `/schedule/<owner>`

**GET**: Returns full schedule

**PUT**: Add or remove an event to/from the owner's schedule
```javascript
{
    "event_name": <string>,
    "action": "ADD" or "REMOVE"
}
```
