### Tools we'll use 
- **Python** ```3.*```
- **Django** ```2.*```
- *PostgreSQL*
- *pipenv*
    - ```Pipfile``` : All the **direct dependencies** of ur project.
    - ```Pipfile.lock``` : **All** the dependencies with *versions* & *hashes*.

### Getting Started 
- Base
    1. ```mkdir booktime && cd booktime```
    2. ```pipenv --three install Django```
    3. ```pipenv shell```  <small>( activate env )</small>
    4. ```django-admin startproject booktime .``` <small>( under ```booktime``` )</small>