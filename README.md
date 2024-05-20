# Central CI

This CI tests the user flow for several designs at once, it is made to have the latest most reliable set of tool versions to use in the user flow.

Until now there are 2 designs being run: `caravel_user_project` and `openframe_timer_example`

There are 2 CIs, one that runs nightly, and updates the tool versions in `tools.json` and the design versions in `.github/scripts/designs.json`, and a bot creates a PR if there are updates to these files. The other CI runs when the bot creates the PR, which runs the full user flow.
