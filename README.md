# zigbee2mqtt-multi-addon-action

Use it to create and maintain repository with multiple Zigbee2mqtt Home Assistant add-ons.

## Setup

1. Create new empty public Github repository
2. Click on the "Actions" tab in the tab bar
3. Press the "New workflow" button
4. Press the "Skip this and set up a workflow yourself →" link
5. Replace the sample code with the following code and replace "addon 1, addon 2" with any addon names that you want to use separated with a comma (example: "Living Room, Bedroom, Garage"):

```YAML
name: Multiple Zigbee2mqtt Home Assistant add-ons

on:
  schedule:
    - cron: '*/30 * * * *' # every 30 minutes
  workflow_dispatch: # on button click

jobs:
  sync:

    runs-on: ubuntu-latest

    steps:
      - uses: andreypolyak/zigbee2mqtt-multi-addon-action@v1.0
        with:
          addon_names: "addon 1, addon 2"
          github_token: ${{ github.token }}
```

6. Press the "Start commit" button, then "Commit new file"
7. Click on the "Actions" tab in the tab bar once again
8. Select the "Multiple Zigbee2mqtt Home Assistant add-ons" workflow from the side panel
9. Press the "Run workflow" button and then once again "Run workflow" button
10. Wait for workflow run completion
11. Add your repository to add-on repositories in Home Assistant Supervisor

## Usage

This action will automatically run every 30 minutes and check if any updates to the original Zigbee2mqtt are available. If they would be found action will update version in your repository accordingly.

To create new Zigbee2mqtt add-ons after initial setup open your workflow (.github/workflows/main.yml by default) and change the addon_names variable. Don't forget to separate add-on names with a comma.
