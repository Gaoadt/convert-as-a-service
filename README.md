# ConveRT as a service
## Overview

The goal of the repo is to provide ConveRT context embeddings via HTTP API

## Running

```sh
docker run --rm -p5000:5000 ghcr.io/gaoadt/convert-as-a-service
```

## Usage

Example usage
```python
import requests
res = requests.post('http://localhost:5000/convert', json=[["Hey, how are you?", "fine"]])
print(res.json())
```

Expected result:
```js
{'code': 0, 'data': [[0.024729499593377113, 0.01896725594997406, 0.02378075197339058, 0.04291800782084465, -0.06537788361310959  ...
```