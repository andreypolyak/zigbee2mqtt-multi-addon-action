import json
import hashlib
import os
from github import Github, GithubException


TOKEN = os.environ["INPUT_GITHUB_TOKEN"]
ADDON_NAMES = os.environ["INPUT_ADDON_NAMES"]
LOCAL_REPO = os.environ["GITHUB_REPOSITORY"]


def get_addon_state(addon_name, latest_version):
  directory = f"zigbee2mqtt-{build_postfix(addon_name)}"
  try:
    raw_config = local_repo.get_contents(f"{directory}/config.json")
  except GithubException:
    print(f"{addon_name} is missing")
    return "missing"
  config = json.loads(raw_config.decoded_content)
  version = config["version"]
  if latest_version != version:
    print(f"{addon_name} is outdated (version {version}, latest version {latest_version})")
    return "outdated"
  print(f"{addon_name} is up to date")
  return "current"


def get_z2m_config():
  config = json.loads(get_z2m_file("config.json"))
  return config


def get_z2m_file(file):
  raw_file = z2m_repo.get_contents(f"zigbee2mqtt/{file}")
  file = raw_file.decoded_content
  return file


def build_addon_config(config, addon_name):
  addon_config = config.copy()
  slug_postfix = build_postfix(addon_name)
  slug = config["slug"]
  addon_config["slug"] = f"{slug}_{slug_postfix}"
  description = config["description"]
  addon_config["description"] = f"{description} ({addon_name})"
  name = config["name"]
  addon_config["name"] = f"{name} {addon_name}"
  return addon_config


def build_postfix(addon_name):
  return addon_name.lower().replace(" ", "_").replace(".", "_").replace("-", "_")


def update_addon(addon_name, addon_config):
  directory = f"zigbee2mqtt-{build_postfix(addon_name)}"
  message = f"Update config.json for {addon_name} addon"
  content = json.dumps(addon_config, indent=True)
  sha = local_repo.get_contents(f"{directory}/config.json").sha
  local_repo.update_file(f"{directory}/config.json", message, content, sha)


def create_addon(addon_name, addon_config):
  directory = f"zigbee2mqtt-{build_postfix(addon_name)}"
  message = f"Create config.json for {addon_name} addon"
  content = json.dumps(addon_config, indent=True)
  local_repo.create_file(f"{directory}/config.json", message, content)
  for file in ["DOCS.md", "README.md", "icon.png", "logo.png"]:
    content = get_z2m_file(file)
    message = f"Create {file} for {addon_name} addon"
    local_repo.create_file(f"{directory}/{file}", message, content)


def create_repository():
  try:
    repository = local_repo.get_contents("repository.json")
  except GithubException:
    message = "Create repository.json"
    content = json.dumps({"name": "Zigbee2mqtt Multi Add-on Repository"}, indent=True)
    local_repo.create_file("repository.json", message, content)


def build_addon_names_list():
  addon_names = ADDON_NAMES.split(",")
  clean_addon_names = []
  for addon_name in addon_names:
    clean_addon_names.append(addon_name.strip())
  return clean_addon_names


def get_local_repo():
  g = Github(TOKEN)
  repo = g.get_repo(LOCAL_REPO)
  return repo


def get_z2m_repo():
  g = Github(TOKEN)
  repo = g.get_repo("zigbee2mqtt/hassio-zigbee2mqtt")
  return repo


def main():
  addon_names = build_addon_names_list()
  updated_addons = []
  created_addons = []
  results = ""

  config = get_z2m_config()
  latest_version = config["version"]

  for addon_name in addon_names:
    state = get_addon_state(addon_name, latest_version)
    addon_config = build_addon_config(config, addon_name)
    if state == "current":
      continue
    elif state == "outdated":
      update_addon(addon_name, addon_config)
      updated_addons.append(addon_name)
    elif state == "missing":
      create_addon(addon_name, addon_config)
      created_addons.append(addon_name)
  create_repository()
  if len(created_addons) > 0:
    results += f"Created addons: {created_addons}. "
  if len(updated_addons) > 0:
    results += f"Updated addons: {updated_addons}. "
  if results == "":
    results = "No changes. "
  results = results[:-1]
  print(results)


local_repo = get_local_repo()
z2m_repo = get_z2m_repo()
main()

