
# VWA+Wazuh (Mini Lab SOC)
## Requirements
Here are the minimum requirements for running Kahyangan:
- Processor AMD Ryzen 3
- RAM 6 GB
- SSD DDR 3
- [Docker](https://docs.docker.com/get-docker/)
- [Docker compose](https://docs.docker.com/compose/install/)

## Installation
### Running Containers

Navigate to `/wazuh-docker/single-node` folder.

Type `docker-compose -f generate-indexer-certs.yml run --rm generator` to generate an SSL Certificate for Wazuh.

Then, run all the services by typing the following commands in the terminal.

```shell
docker compose build
docker compose up
```

![](https://i.imgur.com/wo3RDGs.png)

Access [https://localhost:5601](https://localhost:5601) to access Wazuh.

If it appears like the following image, wait for a while and refresh it.

![](https://i.imgur.com/LUlqo7n.png)

After that, we will get a page like this.

![](https://i.imgur.com/aEatVzi.png)

On this page, we can log in using the username credentials `admin` and password `SecretPassword`.

After logging in using the credentials above, we will be directed to a page like this.

![](https://i.imgur.com/7aRgoMW.png)

We can use Wazuh by looking at the reference as follows [https://documentation.wazuh.com/current/user-manual/index.html](https://documentation.wazuh.com/current/user-manual/index.html)

We can also see the services available by accessing [http://localhost:80](http://localhost:80) as shown below.

![](https://i.imgur.com/CCGDYwD.png)

There are 4 vulnerable web app services that can be attacked with certain attack techniques, namely SQL Injection, SSTI, LFI, and PHP Arbitary File Upload. We will use these four web apps to test the Wazuh that we have installed.

### Discord Bot Integration

To integrate a Discord bot, we need to turn off the container first using the `docker compose down --volumes` command.

After that, we can edit the file `/config/wazuh_cluster/wazuh_manager.conf` as follows.

![](https://i.imgur.com/kdP9YBj.png)

You need to add your `hook_url` there.

```xml
  <integration>
    <name>custom-discord.py</name>
    <hook_url>https://webhooks</hook_url>
    <level>7</level>
    <alert_format>json</alert_format>
  </integration>
```

Then, run the container again with the `docker compose up --build` command. After running, we will get an alert like the following on our Discord server.

![](https://i.imgur.com/4HyzKhh.png)

For a more detailed explanation, see the following website [https://eugenio-chaves.github.io/blog/2022/creating-a-custom-wazuh-integration/](https://eugenio-chaves.github.io/blog/2022/creating-a-custom-wazuh-integration/) .

## Topology

![](https://i.imgur.com/B0Q5JIk.png)

## Services

### Web apps

These web apps are web applications that we create to test the alerting system within Wazuh that we installed. We can access this application at [http://localhost](http://localhost) or we can also access it through the `attacker PC` at the url [http://apps.proxy/](http://apps.proxy/).

We intentionally make this web service vulnerable to various kinds of attacks to be an asset for this lab. The attacks that we can exploit from these services are:

1.  Server-Side Template Injection
2.  PHP Arbitary File Upload
3.  SQL Injection
4.  and Local File Inclusion

### Wazuh Services

The Wazuh Services is the place where our Wazuh services run. The services included are:

-   Wazuh Dashboard
-   Wazuh Indexer
-   Wazuh Manager

### Attacker PC

The Attacker PC is a container that we will use to simulate attacks on our services. This is where we will test the alerting system of Wazuh as an attacker/red teamer.

We have also provided some exploit scripts on this PC, which can be checked in the `/exploit` folder. There are several exploits for Web Apps services that we can run.

Here is an example of an exploitation script that we can run on the attacker machine to attack the `php_arbitary_file_upload` service on the web service.

![](https://i.imgur.com/enJ7yKb.png)