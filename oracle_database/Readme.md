# Download tools on your server
    ./oracle-instantclient-basic-21.6.0.0.0-1.el8.x86_64.rpm
    ./oracle-instantclient-sqlplus-21.6.0.0.0-1.el8.x86_64.rpm

# Install

    $ rpm -ivh oracle-instantclient11.2-basic-11.2.0.2.0.x86_64.rpm
    $ rpm -ivh oracle-instantclient11.2-sqlplus-11.2.0.2.0.x86_64.rpm

# Set environment variables in your ~/.bash_profile

    ORACLE_HOME=/usr/lib/oracle/11.2/client64
    PATH=$ORACLE_HOME/bin:$PATH
    LD_LIBRARY_PATH=$ORACLE_HOME/lib
    export ORACLE_HOME
    export LD_LIBRARY_PATH
    export PATH

Reload your .bash_profile by simply typing source ~/.bash_profile (suggested by jbass) or Log-out user and log-in again.

# Run
Now you're ready to use SQL*Plus and connect your server. Type in :

    $ sqlplus "username/pass@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.2.1)(PORT=1521))(CONNECT_DATA=(SID=YOURSID)))"


References: https://stackoverflow.com/questions/23488394/how-to-install-sql-plus-client-in-linux