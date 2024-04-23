## Network tools

This is project with few tools used in my service-based projects in Python. Their basic description is following.

### Circuit breaker
The Circuit Breaker pattern is a software development technique used to enhance system stability and prevent cascading failures in distributed systems. It works by monitoring the number of failures that occur during interactions with a service. When the failures exceed a certain threshold, the Circuit Breaker trips, and all further calls to the service are halted for a predefined period. This stoppage prevents the system from performing actions that are likely to fail, allowing it time to recover.

### Limit call per second
For cases when some functionality (e.g. external API) should be called not more than specific number of times per some period we can limit it by this Python decorator.

### Retry
In practice 5-7% of external API calls fail due to unstable nature of Internet. To handle it correctly for cases when unexpected failure happened we can execute retry. Maybe even more than once.

### Timeout
Sometimes, we can be certain that a function should not operate for more than a specific time period. In these cases, we can prevent additional waiting time by raising an exception after the period has expired.
