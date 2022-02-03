# Overview
This is a tiny DNS server written in Python, using [dnslib](https://pypi.org/project/dnslib/).  It will respond with the IP address of the host that queried it.  Think of it as a "what is my IP" website, but using DNS.

This can be used in two ways.  First, if you directly query (eg. dig @host-running-dns-query-me fq.dn), the A record response will be your own IP, as seen by the server running this.

Secondly, if a DNS zone is properly delegated to the host this is running on, you can query this through your normal DNS recursor (eg. dig fq.dn).  Here, the response you see will be the IP address that your *DNS recursor* queried from.

# Limitations
Does not currently support IPv6 or TCP.  I'm running this on fly.io and have been unable to get this working on TCP in addition to UDP or IPv6 so far.

# Environment Variables
- `DNS_ANSWER_FOR`: Specific FQDN to respond to.  Queries for all other FQDNs will receive an NXDOMAIN answer.
- `DNS_LISTEN_PORT`: Port to listen on.  Default 53.
- `DNS_LISTEN_ADDRESS`: IP to listen on.  Default to 0.0.0.0.

# Building Docker Image
To create a Docker container to run this locally: `make docker name=dns-query-me version=0.01`

Alternatively, to deply to the Fly.io service, see next section.

# Deploying to Fly.io
1. Follow Fly.io's [instructions](https://fly.io/docs/getting-started/installing-flyctl/) for installing their CLI tool.
2. Run `flyctl launch --dockerfile Dockerfile-fly --remote-only=false`
This creates a new application on Fly.io.  We explicitly specify the Dockerfile to use, since there's (more on that below).  And we force it to build the docker image locally on your machine, since I saw errors pulling from Docker Hub when letting it build on Fly.io.
3. flyctl will then prompt you for a few settings.  A template fly.toml configuration file is included (it specifies the port to listen on, since that's not default).  So choose yes when asked `? Would you like to copy its configuration to the new app? Yes`.
4. The Docker image will be built locally, and then deployed on fly.io.  If all goes well, at the end you should see: 
```
1 desired, 1 placed, 1 healthy, 0 unhealthy
--> v0 deployed successfully
```

5. Query your service.  `dig @name-of-your-application.fly.dev myip2.example.com`.  This queries your fly.io container for 'myip2.example.com' - which is set as the FQDN to respond to in the template fly.toml configuration file.


# Why is there a separate Dockerfile for fly.io?
fly.io requires some special options for UDP services.  To listen on UDP ports, instead of binding to all IP addresses (eg 0.0.0.0) or a specific static IP, we need to listen on the IP address that 'fly-global-services' resolves inside of our container.  Fly.io describes this [here](https://community.fly.io/t/incoming-udp-support-arriving-soon/231).

We make this work by just resolving 'fly-global-services' in a shell script, and passing that as the environment variable to the Python application.  Dockerfile-fly just tells fly.io to run this shell script instead of directly running the Python scfript.
