# FoccoERP Purchase Order Search Enhancement

## Overview
Simplify and streamline the search process for purchase orders in FoccoERP with a user-friendly web interface. Import purchase order data from XML files and perform advanced searches with various filters.

## Features
- **User Authentication**: Secure login and registration system.
- **XML Data Import**: Import purchase order data from FoccoERP XML reports.
- **Advanced Search**: Detailed searches with multiple filters.
- **Fuzzy Search**: Find purchase orders with minor spelling errors.

## Installation

### Prerequisites
- Python 3.x
- Flask
- SQLite (default database)

### Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/rtalis/foccoerp-search.git
    cd foccoerp-search
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    playwright install
    ```

3. Setup the database:
    ```bash
    python
    >>> from app import db
    >>> db.create_all()
    >>> exit()
    ```

4. Run the application:
    ```bash
    python app.py
    ```

5. Access the application: Open your browser and go to `http://127.0.0.1:5000`.

## Usage
1. **Register**: Create a new user account.
2. **Login**: Log in with your credentials.
3. **Import Data**: Upload an XML file containing purchase order data.
4. **Search**: Use the search interface to find purchase orders based on various criteria.

## Security Considerations
- **Database Permissions**: Ensure minimal required privileges.
- **SSL/TLS**: Configure for secure communication.
- **Session Security**: Uses secure cookies to protect session data.

## Backup and Restore

### Backup

Add this to your cron job
   ```bash
0 2 * * * /path/to/python /path/to/folder/app/tools/backup.py
```
## Contributions
Fork this repository, create a branch, and submit a pull request with improvements or new features.

## License
This project is licensed under the MIT License.