# Vulnerable Code Samples: SQL

Secure-code-review training examples (60 samples). Each sample is vulnerable code, the vulnerability class, and references.

## Sample 1 — Hardcoded Credentials

- **Language**: SQL
- **Vulnerability**: Hardcoded Credentials
- **Description**: Embedding sensitive credentials directly in the query.

```
SELECT * FROM users WHERE username = 'admin' AND password = 'secret123';
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-798: https://cwe.mitre.org/data/definitions/798.html

## Sample 2 — Insecure View

- **Language**: SQL
- **Vulnerability**: Insecure View
- **Description**: Creating views without proper access controls.

```
CREATE VIEW user_data AS SELECT * FROM users;
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 3 — SQL Injection

- **Language**: SQL
- **Vulnerability**: SQL Injection
- **Description**: Dynamic SQL query with unescaped input.

```
DECLARE @query NVARCHAR(100);
SET @query = N'SELECT * FROM users WHERE id = ' + @input;
EXEC sp_executesql @query;
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 4 — Excessive Privileges

- **Language**: SQL
- **Vulnerability**: Excessive Privileges
- **Description**: Granting excessive permissions to a user.

```
GRANT ALL PRIVILEGES ON database.* TO 'user'@'localhost';
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-732: https://cwe.mitre.org/data/definitions/732.html

## Sample 5 — Insecure Temporary Table

- **Language**: SQL
- **Vulnerability**: Insecure Temporary Table
- **Description**: Creating temporary tables without access controls.

```
CREATE TEMPORARY TABLE temp_data (id INT, data VARCHAR(100));
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-732: https://cwe.mitre.org/data/definitions/732.html

## Sample 6 — Insecure Backup

- **Language**: SQL
- **Vulnerability**: Insecure Backup
- **Description**: Storing database backups without encryption.

```
BACKUP DATABASE mydb TO DISK = 'mydb.bak';
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-312: https://cwe.mitre.org/data/definitions/312.html

## Sample 7 — Insecure Dynamic Query

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Query
- **Description**: Using dynamic SQL with unescaped input.

```
SET @sql = CONCAT('SELECT ', @column, ' FROM users');
PREPARE stmt FROM @sql;
EXECUTE stmt;
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 8 — Insecure Trigger

- **Language**: SQL
- **Vulnerability**: Insecure Trigger
- **Description**: Trigger executing unvalidated actions.

```
CREATE TRIGGER update_log AFTER INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO log (data) VALUES (NEW.data);
END;
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 9 — Insecure Function

- **Language**: SQL
- **Vulnerability**: Insecure Function
- **Description**: Creating a function with excessive privileges.

```
CREATE FUNCTION dangerous_func() RETURNS TEXT AS $$ SELECT password FROM users; $$ LANGUAGE SQL;
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-732: https://cwe.mitre.org/data/definitions/732.html

## Sample 10 — Insecure Stored Procedure

- **Language**: SQL
- **Vulnerability**: Insecure Stored Procedure
- **Description**: Stored procedure with excessive privileges.

```
CREATE PROCEDURE unsafe_proc @input NVARCHAR(100)
AS
BEGIN
    EXEC('SELECT * FROM users WHERE name = ''' + @input + '''')
END;
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 11 — Insecure Role Assignment

- **Language**: SQL
- **Vulnerability**: Insecure Role Assignment
- **Description**: Assigning overly permissive roles.

```
CREATE ROLE admin;
GRANT ALL ON DATABASE mydb TO admin;
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-732: https://cwe.mitre.org/data/definitions/732.html

## Sample 12 — Hardcoded Credentials

- **Language**: SQL
- **Vulnerability**: Hardcoded Credentials
- **Description**: Embedding sensitive credentials directly in the query.

```
SELECT * FROM users WHERE username = 'admin' AND password = 'secret123';
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-798: https://cwe.mitre.org/data/definitions/798.html

## Sample 13 — Insecure View

- **Language**: SQL
- **Vulnerability**: Insecure View
- **Description**: Creating views without proper access controls.

```
CREATE VIEW user_data AS SELECT * FROM users;
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 14 — SQL Injection

- **Language**: SQL
- **Vulnerability**: SQL Injection
- **Description**: Dynamic SQL query with unescaped input.

```
DECLARE @query NVARCHAR(100);
SET @query = N'SELECT * FROM users WHERE id = ' + @input;
EXEC sp_executesql @query;
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 15 — Excessive Privileges

- **Language**: SQL
- **Vulnerability**: Excessive Privileges
- **Description**: Granting excessive permissions to a user.

```
GRANT ALL PRIVILEGES ON database.* TO 'user'@'localhost';
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-732: https://cwe.mitre.org/data/definitions/732.html

## Sample 16 — Insecure Temporary Table

- **Language**: SQL
- **Vulnerability**: Insecure Temporary Table
- **Description**: Creating temporary tables without access controls.

```
CREATE TEMPORARY TABLE temp_data (id INT, data VARCHAR(100));
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-732: https://cwe.mitre.org/data/definitions/732.html

## Sample 17 — Insecure Backup

- **Language**: SQL
- **Vulnerability**: Insecure Backup
- **Description**: Storing database backups without encryption.

```
BACKUP DATABASE mydb TO DISK = 'mydb.bak';
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-312: https://cwe.mitre.org/data/definitions/312.html

## Sample 18 — Insecure Dynamic Query

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Query
- **Description**: Using dynamic SQL with unescaped input.

```
SET @sql = CONCAT('SELECT ', @column, ' FROM users');
PREPARE stmt FROM @sql;
EXECUTE stmt;
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 19 — Insecure Trigger

- **Language**: SQL
- **Vulnerability**: Insecure Trigger
- **Description**: Trigger executing unvalidated actions.

```
CREATE TRIGGER update_log AFTER INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO log (data) VALUES (NEW.data);
END;
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 20 — Insecure Function

- **Language**: SQL
- **Vulnerability**: Insecure Function
- **Description**: Creating a function with excessive privileges.

```
CREATE FUNCTION dangerous_func() RETURNS TEXT AS $$ SELECT password FROM users; $$ LANGUAGE SQL;
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-732: https://cwe.mitre.org/data/definitions/732.html

## Sample 21 — Insecure Stored Procedure

- **Language**: SQL
- **Vulnerability**: Insecure Stored Procedure
- **Description**: Stored procedure with excessive privileges.

```
CREATE PROCEDURE unsafe_proc @input NVARCHAR(100)
AS
BEGIN
    EXEC('SELECT * FROM users WHERE name = ''' + @input + '''')
END;
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 22 — Insecure Role Assignment

- **Language**: SQL
- **Vulnerability**: Insecure Role Assignment
- **Description**: Assigning overly permissive roles.

```
CREATE ROLE admin;
GRANT ALL ON DATABASE mydb TO admin;
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-732: https://cwe.mitre.org/data/definitions/732.html

## Sample 23 — Insecure Data Masking

- **Language**: SQL
- **Vulnerability**: Insecure Data Masking
- **Description**: Failing to mask sensitive data in query results.

```
SELECT username, credit_card FROM users;
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-200: https://cwe.mitre.org/data/definitions/200.html

## Sample 24 — Insecure Audit Logging

- **Language**: SQL
- **Vulnerability**: Insecure Audit Logging
- **Description**: Failing to log sensitive operations.

```
INSERT INTO users (username) VALUES ('newuser');
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-778: https://cwe.mitre.org/data/definitions/778.html

## Sample 25 — Insecure Column Encryption

- **Language**: SQL
- **Vulnerability**: Insecure Column Encryption
- **Description**: Storing sensitive data without encryption.

```
ALTER TABLE users ADD credit_card VARCHAR(16);
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-311: https://cwe.mitre.org/data/definitions/311.html

## Sample 26 — Insecure Data Retention

- **Language**: SQL
- **Vulnerability**: Insecure Data Retention
- **Description**: Retaining sensitive data without expiration policies.

```
INSERT INTO logs (user_id, data) VALUES (123, 'sensitive data');
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-285: https://cwe.mitre.org/data/definitions/285.html

## Sample 27 — Insecure Schema Modification

- **Language**: SQL
- **Vulnerability**: Insecure Schema Modification
- **Description**: Allowing unvalidated schema changes.

```
ALTER TABLE users ADD COLUMN data VARCHAR(100);
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-285: https://cwe.mitre.org/data/definitions/285.html

## Sample 28 — Insecure Transaction Handling

- **Language**: SQL
- **Vulnerability**: Insecure Transaction Handling
- **Description**: Failing to rollback transactions on error.

```
BEGIN TRANSACTION;
INSERT INTO users (name) VALUES ('test');
-- No ROLLBACK on error
```

**References**:
- OWASP: https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/
- CWE-390: https://cwe.mitre.org/data/definitions/390.html

## Sample 29 — Insecure Dynamic Table Name

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Table Name
- **Description**: Using user input in table names for queries.

```
SELECT * FROM @table_name WHERE id = 1;
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 30 — Insecure Dynamic Column Name

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Column Name
- **Description**: Using user input in column names for queries.

```
SELECT @column_name FROM users;
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 31 — Insecure Dynamic Index Creation

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Index Creation
- **Description**: Creating indexes with user-controlled names.

```
CREATE INDEX @index_name ON users(id);
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 32 — Insecure View Definition

- **Language**: SQL
- **Vulnerability**: Insecure View Definition
- **Description**: Creating views exposing sensitive columns.

```
CREATE VIEW user_view AS SELECT id, password FROM users;
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-200: https://cwe.mitre.org/data/definitions/200.html

## Sample 33 — Insecure Dynamic Constraint

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Constraint
- **Description**: Creating constraints with user-controlled names.

```
ALTER TABLE users ADD CONSTRAINT @constraint_name UNIQUE (email);
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 34 — Insecure Dynamic Trigger

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Trigger
- **Description**: Creating triggers with user-controlled logic.

```
CREATE TRIGGER @trigger_name AFTER INSERT ON users FOR EACH ROW BEGIN INSERT INTO logs(data) VALUES (@input); END;
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 35 — Insecure Dynamic Role Creation

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Role Creation
- **Description**: Creating roles with user-controlled privileges.

```
CREATE ROLE @role_name WITH LOGIN PASSWORD 'pass';
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 36 — Insecure Dynamic Sequence Creation

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Sequence Creation
- **Description**: Creating sequences with user-controlled names.

```
CREATE SEQUENCE @sequence_name;
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 37 — Insecure Dynamic Partition Creation

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Partition Creation
- **Description**: Creating partitions with user-controlled names.

```
ALTER TABLE users PARTITION BY RANGE (@partition_name);
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 38 — Insecure Dynamic Function Creation

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Function Creation
- **Description**: Creating functions with user-controlled logic.

```
CREATE FUNCTION @func_name() RETURNS INT AS BEGIN RETURN @input; END;
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 39 — Insecure Dynamic Schema Creation

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Schema Creation
- **Description**: Creating schemas with user-controlled names.

```
CREATE SCHEMA @schema_name;
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 40 — Insecure Dynamic User Creation

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic User Creation
- **Description**: Creating users with user-controlled privileges.

```
CREATE USER @user_name WITH PASSWORD 'pass' @privileges;
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 41 — Insecure Dynamic Privilege Grant

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Privilege Grant
- **Description**: Granting privileges with user-controlled scope.

```
GRANT @privilege ON @table TO @user;
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 42 — Insecure Dynamic Audit Log

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Audit Log
- **Description**: Configuring audit logs with user-controlled settings.

```
ALTER SYSTEM SET audit_trail = @setting;
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-778: https://cwe.mitre.org/data/definitions/778.html

## Sample 43 — Insecure Dynamic Backup Configuration

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Backup Configuration
- **Description**: Configuring backups with user-controlled settings.

```
BACKUP DATABASE @db TO DISK = @path;
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 44 — Insecure Dynamic Statistics Collection

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Statistics Collection
- **Description**: Collecting statistics with user-controlled parameters.

```
ANALYZE @table_name;
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 45 — Insecure Dynamic Transaction Isolation

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Transaction Isolation
- **Description**: Setting transaction isolation levels with user input.

```
SET TRANSACTION ISOLATION LEVEL @level;
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 46 — Insecure Dynamic Replication Configuration

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Replication Configuration
- **Description**: Configuring replication with user-controlled settings.

```
CHANGE MASTER TO MASTER_HOST=@host, MASTER_USER=@user;
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 47 — Insecure Dynamic Collation Setting

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Collation Setting
- **Description**: Setting collation with user-controlled values.

```
ALTER TABLE users ALTER COLUMN name SET DATA TYPE VARCHAR(50) COLLATE @collation;
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 48 — Insecure Dynamic Compression Setting

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Compression Setting
- **Description**: Configuring compression with user-controlled settings.

```
SET compression = @method;
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 49 — Insecure Dynamic Connection Parameter

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Connection Parameter
- **Description**: Setting connection parameters with user input.

```
SET @parameter = @value;
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 50 — Insecure Dynamic Encryption Setting

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Encryption Setting
- **Description**: Configuring encryption with user-controlled settings.

```
SET encryption = @method;
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 51 — Insecure Dynamic Session Configuration

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Session Configuration
- **Description**: Configuring session parameters with user input.

```
SET SESSION @parameter = @value;
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 52 — Insecure Dynamic Logging Configuration

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Logging Configuration
- **Description**: Configuring logging with user-controlled settings.

```
SET log_destination = @destination;
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-778: https://cwe.mitre.org/data/definitions/778.html

## Sample 53 — Insecure Dynamic Tablespace Creation

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Tablespace Creation
- **Description**: Creating tablespaces with user-controlled paths.

```
CREATE TABLESPACE @name LOCATION @path;
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 54 — Insecure Dynamic Role Creation

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Role Creation
- **Description**: Creating roles with user-controlled privileges.

```
CREATE ROLE @role_name WITH @privileges;
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 55 — Insecure Dynamic Trigger Creation

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Trigger Creation
- **Description**: Creating triggers with user-controlled logic.

```
CREATE TRIGGER @name @action ON @table FOR EACH ROW @body;
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 56 — Insecure Dynamic Constraint Creation

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Constraint Creation
- **Description**: Creating constraints with user-controlled names.

```
ALTER TABLE users ADD CONSTRAINT @constraint_name CHECK (@condition);
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 57 — Insecure Dynamic Index Creation

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Index Creation
- **Description**: Creating indexes with user-controlled names.

```
CREATE INDEX @index_name ON @table (@column);
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 58 — Insecure Dynamic View Creation

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic View Creation
- **Description**: Creating views with user-controlled queries.

```
CREATE VIEW @view_name AS @query;
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 59 — Insecure Dynamic Partition Creation

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Partition Creation
- **Description**: Creating partitions with user-controlled names.

```
ALTER TABLE users PARTITION BY RANGE (@column) (PARTITION @partition_name VALUES LESS THAN (@value));
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 60 — Insecure Dynamic Sequence Creation

- **Language**: SQL
- **Vulnerability**: Insecure Dynamic Sequence Creation
- **Description**: Creating sequences with user-controlled parameters.

```
CREATE SEQUENCE @sequence_name START WITH @start INCREMENT BY @increment;
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html
