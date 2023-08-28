from jinja2 import Environment, FileSystemLoader

clients = 0
while clients < 1:
    clients = int(input("How many clients? "))

env = Environment(loader=FileSystemLoader("templates/"))

template = env.get_template("docker-compose-clients.yaml")

filename = f"clients-docker-compose/docker-compose-{clients}-clients.yaml"
with open(filename, mode="w", encoding="utf-8") as output:
    output.write(template.render(clients=clients))
    print(f"Wrote docker compose with {clients} clients to {filename}")
