
# Installation:
Python 3.6+ required

### 1. Clone project
```
$ git clone https://github.com/povarok/lms.git
```

### 2. Create and activate virtual environment (optional)
```
$ cd /path/to/project/lms
$ pip3 install virtualenv
$ virtualenv -p python3.6 venv
$ source venv/bin/activate
```

### 3. Install required dependencies
```
$ pip3 install -r requirements.txt
```

### 4. ```touch .env``` in project root dir
### 5. Insert some environment vars
```text
DB_NAME=<str>
DB_USER=<str>
DB_PASSWORD=<str>
DB_HOST=<str>
DB_PORT=<int>
DEBUG=<bool>
ALLOWED_HOSTS=<str>(https://some.domain.name)
```
