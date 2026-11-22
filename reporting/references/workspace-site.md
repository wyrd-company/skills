# A page served from this workspace

Read this when a page needs what Postplan cannot give it: scripts loaded from elsewhere, live data from this workspace, a running dev server, or more than Postplan's upload limit. The workspace's Caddy serves the page under a subdomain of the container's hostname. The [workspace standard](../../standards/references/workspace.md) describes how requests reach it.

## Serve it

1. **Put the page somewhere that outlives the session,** not under `/tmp`, such as the `briefings` folder for the task.
2. **Write a fragment** at `/etc/caddy/conf.d/<name>.caddy`, named for the report, and choose a subdomain that is not already in use there. For static files:

   ```caddy
   http://<name>.{$HOSTNAME} {
       root * /absolute/path/to/site
       file_server
   }
   ```

   For a dev server, use `reverse_proxy 127.0.0.1:<port>` in place of `root` and `file_server`.
3. **Check that the route answers.** A watcher validates the whole configuration and reloads Caddy. An invalid fragment leaves the running configuration unchanged and reports nothing, so test the route:

   ```sh
   curl -s -o /dev/null -w '%{http_code}\n' -H "Host: <name>.$HOSTNAME" http://127.0.0.1/
   ```

   Done when it prints `200`. The reload can take a few seconds.
4. **Give the reader the URL** `<name>.$HOSTNAME`, with the hostname written out in full. It reaches only people who can reach this workspace's ingress. For anyone else, use [Postplan](postplan.md).

## Clean up

The fragment and anything you started for it stay running until someone removes them. Record them with the `ledger` skill when you create them, and delete the fragment when the reader no longer needs the page.
