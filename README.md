# ConveRT as a service
## Overview

The goal of the repo is to provide ConveRT context embeddings via HTTP API

## Running

```sh
docker run --rm -p5000:5000 ghcr.io/gaoadt/convert-as-a-service
```

## API
* `/context` - expects a list of dialogues -
* `/respons` - expects a list of responses
## Usage

Example usage
```python
import requests
res = requests.post('http://localhost:5000/context', json=[["Hey, how are you?", "fine"]])
print(res.json())
res = requests.post('http://localhost:5000/response', json=["Hey, how are you?", "fine"])
print(res.json())
```

Expected result:
```js
{'code': 0, 'data': [[0.024729499593377113, 0.01896725594997406, 0.02378075197339058, 0.04291800782084465, -0.06537788361310959  ...
{'code': 0, 'data': [[0.036538805812597275, 0.010460878722369671, -0.047986604273319244, 0.03360487148165703, -0.03292739763855  ...
```