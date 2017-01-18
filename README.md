# Hack-CLI

Use this CLI to interact with the ACM Hack API.

To install it, clone this repository and run

```BASH
$ python setup.py install
```

Then run the CLI

```BASH
$ acm help
```

By default, the CLI will use the API on the production server. If you want to switch to testing mode (use the server on `http://localhost:5000`), you can do that by setting the `use_local` property:

```BASH
$ acm cli set use_local 1
```

To switch to the remote dev server on `http://hack-ucla-dev.herokuapp.com`, 

```BASH
$ acm cli set use_dev 1
```

To revert to the production server,

```bash
$ acm cli set use_local 0
$ acm cli set use_dev 0
```

