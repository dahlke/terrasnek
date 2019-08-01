# terrasnek

_A Python Client for the Terraform Enterprise API._

### Usage Example:

For more details on using each endpoint, checkout the [`test`](./test) directory.

```
from terrasnek.api import TFE
import os

TFE_TOKEN = os.getenv("TFE_TOKEN", None)

if __name__ == "__main__":
    api = TFE(TFE_TOKEN)
    api.set_organization("YOUR_ORGANIZATION")
```


## Contributing

### Building Test Data

```
cd test/testdata/terraform/
tar -zcvf terrasnek_unittest_config_version.tar.gz src/*
```

### Running Tests

```
source test/secrets/secrets.sh
python3 -m unittest test/*.py
```

##### Example Test Output
```
.............................
----------------------------------------------------------------------
Ran 29 tests in 230.332s

OK

```




_[Project Asana Board](https://app.asana.com/0/1128022822619695/1128022822619711)_