https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/apache-spark-tips

# Apache Spark Tips

## Tips On Spark Stand-Alone Usage

[Apache Spark standalone](https://spark.apache.org/downloads.html) is installed on `erdos`

, and it does not include Hadoop. It is installed with MySQL to allow multiple users to start `spark-shell`

or `pyspark`

. The instructions are slightly different if a user is logging in remotely vs. on the computer locally, where you can just log in with your credentials. In order to get the web UI remotely you will need some X11 forwarding client such as XQuartz on Mac or MobaXterm on PC. On a Windows PC, you can also use Putty but it requires another application called [Xming](https://sourceforge.net/projects/xming/).

If you're off campus start [Mobaxterm](http://mobaxterm.mobatek.net/download-home-edition.html) (PC) or [XQuartz](https://www.xquartz.org/) (Mac). Enter the command `ssh -Y <your-username>@erdos.dsm.fordham.edu`

in the shell provided. If you're using the Departmental computer lab on campus, simply open a terminal window.

- Type
`cd /var/lib/spark`

- Type
`spark-shell (or pyspark)`


Wait a few seconds, You may see some warnings such as the below which are safe to ignore (warnings that result from symbolic links):

`Setting default log level to "ERROR". To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel). Spark context Web UI available at http://127.0.0.1:4040 Spark context available as 'sc' (master = local[*], app id = local-1501096915756). Spark session available as 'spark'. Welcome to`


____ __

/ __/__ ___ _____/ /__

_\ \/ _ \/ _ `/ __/ '_/

/___/ .__/\_,_/_/ /_/\_\ version 2.2.0

/_/

`Using Scala version 2.11.8 (OpenJDK 64-Bit Server VM, Java 1.8.0_131) Type in expressions to have them evaluated. Type :help for more information. `


Note the Web UI IP address (bolded above). It will have a port number, with the first in use being **4040**.

- If you would like to view the Web UI, you will need to start Chrome or Firefox in another ssh session and quit the current session and start the browser. Type
`google‑chrome &`

, which is how to start with the former and`firefox &`

for the latter. Note the ampersand puts the command in the background. If you are on a slower connection, e.g., wireless, the browser responsiveness will vary. - To quit Spark, just press
`ctrl-D`

or type`:q`

.

This is also installed in both JMH302 and LL612 labs. The only differences are that Lincoln Center uses NIS (Network Information Systems) login and Rose Hill has a local “student” account and the IP addresses of each instance. Note that the JMH302 lab is only accessible from the outside world if you SSH into`storm`

and then`puppet`

. In both labs, running “pyspark” is also available. Additionally, Pycharm is installed in both labs. - Notes for sys admins:
- When upgrading Spark on
`erdos`

, which uses MySQL to allow multiple concurrent connections, the following 3 configuration files should be copied from the old installation's`~/spark/conf`

directory:`spark-defaults.conf, spark-env.sh, hive-site.xml`

. - The lab in JMH302 (and sobolev) do(es) not use MySQL. No need to copy anything from the old directory.
- There are some environment variables in
`/etc/profile.d/spark.sh`

and the path to`SPARK_EXAMPLES_JAR`

should be updated. - logging levels can be adjusted in the
`log4j.properties`

file, e.g., replace`warning`

with`error`

. `erdos`

has Hive installed and the Spark directory is`/usr/local/share`

.- If you see any errors like
`java.io.FileNotFoundException: derby.log (Permission denied)`

, delete the 2`.lck`

files in the metastore directory.

- When upgrading Spark on