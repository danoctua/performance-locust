# Locust Performance Tests

_TODO_: think about adding this to the CI, using the following article: https://docs.locust.io/en/stable/running-without-web-ui.html

## Useful links:

* About - https://docs.locust.io/en/stable/what-is-locust.html
* How to write locust files - https://docs.locust.io/en/stable/writing-a-locustfile.html
* How to run in Docker - https://docs.locust.io/en/stable/running-in-docker.html
* Running tests locally - http://0.0.0.0:8089/

## Running tests

If needed, update the `.env` file with variable that will be used to retrieve the token from the SSO depending on the environment you're running it on.

Then run with any of the below commands.
```shell
docker compose up [--scale worker=4]
```
or
```shell
make run
```
_Note: Using `--scale` option you could add more workers that will be running tests._

## Results
To see the statistic, go to the Locust local page (http://0.0.0.0:8089/) and run performance tests.
Statistics will appear on the tabs from the top.
