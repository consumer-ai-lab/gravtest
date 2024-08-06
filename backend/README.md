# WCL Test Application: NodeJS Backend

## Run backend
Move to required directory `backend/`

- Install dependencies
```bash
npm install
```

- Start server
```bash
npm run start
```

## Tests

We perform load testing to make sure our backend will hold well in practical use case.

There are two major scenarios where our application might fail:
1. Our node server, with overload of concurrent users
2. Mongo DB with concurrent read/write access

Thus we will run two tests as of now,
1. Basic request test on node, to check if our nodejs backend can handle that many users.
2. Read/write on mongoDB to check if mongo DB can handle these many requests

We are not taking into account AWS S3 stress as it is only required at the end of test and is very stable.

Current Stress requirement: (2023)
 - Total users: 160/batch, thus we will be testing for 200 requests per second.

### Populating mongoDB

- We are putting fake data in mongoDB, `load-test-table` we will put `500` records there, to do so we will be using `scripts/populate-mongodb.js`. (we only do this once)
- To test `read/write` we will use `scripts/fake-id.js` to get fake id for virtual user to access and update
- We will request on `/load-test` to read and write on these records and load test mongoDB

### Load testing

- Move to required directory `backend/tests/`
- we will be using `Artillery` module for load testing our backend application.
- Article link: [a-guide-to-load-testing-nodejs-apis-with-artillery](https://blog.appsignal.com/2021/11/10/a-guide-to-load-testing-nodejs-apis-with-artillery.html)

- Install `Artillery`
```bash
npm install -g artillery@latest
```

- Check version
```bash
artillery -V
```

- In the `tests/` folder, we have different test files for different cases.
- In the `package.json`, we have scripts to run different `.yml` files that will run load-tests and store it's result in specified `.json` file, the command format is as follows
```bash
artillery run test-file-path.yml --output output-file-path.json
```

- To run load test of any kind check out `package.json` and run `npm run your-test-name`
```bash
npm run basic-test
```

## Making Docker file

Move to required directory

- Build Image
```bash
docker build --tag YOUR-USER-NAME/wcl_backend:v1 .
```

v1 is for versions

- Run Image at port 5000
```bash
docker run -d -p 5000:5000 YOUR-USER-NAME/wcl_backend
```

- Check images
```bash
docker ps
```

- Stop once done
```bash
docker stop YOUR-USER-NAME/wcl_backend
```

- Upload image to docker hub
```bash
docker push YOUR-USER-NAME/wcl_backend
```

## Deploying backend to AWS EC2

1. Login to your EC2 terminal
2. Install docker (if not done already) on EC2: [how-to-install-docker-on-aws-ec2-ubuntu](https://linux.how2shout.com/how-to-install-docker-on-aws-ec2-ubuntu-22-04-or-20-04-linux/)

- Pull image from docker hub
```bash
docker pull YOUR-USER-NAME/wcl_backend
```

- Run Image at port 5000
```bash
docker run -d -p 5000:5000 YOUR-USER-NAME/wcl_backend
```

- See container logs
```bash
docker logs -f container_id
```

- Enter into Container terminal
```bash
docker exec -it container_id /bin/sh
```

Note: Add network security group to open up port to public