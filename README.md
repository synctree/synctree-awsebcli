An extended version of the EB cli to better support multiple profiles, apps, and environments. See README.rst for the upstream manual.

Hacking
---

Setup instructions:

```bash
python setup.py build
python setup.py develop # might require sudo
python setup.py develop # yes, you have to run it twice. patches welcome
ebx --help
```

Finally, create or edit your AWS credentials:

  vim ~/.aws/

```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
region = us-west-2

[profile client1]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
region = us-east-1

...
```

Note that you can use different profiles with the cli via `--profile client1`.

Each command has a `controller`, and puts the "business" logic in a corresponding `*ops` file in `operations`.