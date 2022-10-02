# Укоротитель ссылок YaCut

YaCut project is the web-links cutting service. Its key features:
- short links generation (by user / offered by the service) and
connection to initial long links,
- redirection to initial addres when accessing short links.

Also there is API available for everyone.
<details><summary><h4> API request examples </h4></summary>

- Short link generation: 
    ```SQL
    POST /api/id/
    {
      "url": "string",
      "custom_id": "string"
    }
    ```

- Get original link by specified short id:
    ```SQL
    GET /api/id/{short_id}/
    ```

</details>

## Technologies
- Python 3.7
- Flask 2.0.2
- REST API
- SQLAlchemy
- HTML

## Project installation and local launch
<details><summary> Instructions </summary>

- Clone the repository follow it via the command line:

    ```bash
    git clone https://github.com/photometer/yacut
    cd yacut
    ```

- Create and activate virtual environment:

    * For Linux/MacOS
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

    * For windows
        ```bash
        python -m venv venv
        source venv/scripts/activate
        ```

- Install necessary requirements:

    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

- Don't forget to creaet `.env` file and fill it up:

    ```
    DATABASE_URI=<dialect+driver://username:password@host:port/database>
    FLASK_APP=yacut
    FLASK_ENV=development
    SECRET_KEY=<Your_secret_key>
    ```

- Create database file and tables in it:

    ```bash
    flask shell
    >>> from yacut import db
    >>> db.create_all()
    ```

- Launch locally:

    ```bash
    flask run
    ```

</details>

## Author
Liza Androsova :dizzy:
